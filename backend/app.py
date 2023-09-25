from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
import configparser

from postgresCon import postgres_connect
from mysqlCon import mysql_connect
from postgresDDL import postgres_DDL
from mysqlDDL import mysql_DDL

import model

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

configfile = "databases.cfg"
config = configparser.ConfigParser()

# Connect to database and retrieve DDL statements
def connect_DDL(database_url, database_name, database_type):
    try:
        if not (database_url and database_name):
            raise ValueError("Missing required parameters")

        if database_type == "postgres":
            p = postgres_DDL(database_url, database_name)
            result = p.connection()
            ddl_statements = result.get('message', [])
            return ddl_statements

        elif database_type == "mysql":
            p = mysql_DDL(database_url, database_name)
            result = p.connection()
            ddl_statements = result.get('message', [])
            return ddl_statements
    
    except Exception as e:
        raise Exception("Could not connect to database. Reason: " + str(e))


# Generate SQL from question and DDL statements
@app.route('/generate_SQL', methods=['POST'])
@cross_origin()
def generate_sql():
    try:
        data = request.get_json(force=True)
        database_url = data.get('database_url')
        database_name = data.get('database_name')
        database_type = data.get('database_type')
        question = data.get('question')

        ddl_statement = connect_DDL(database_url, database_name, database_type)
        DDL_string = ""
        for i in ddl_statement:
            DDL_string += i.replace("\n", " ")

        # return(DDL_string)
        if not (DDL_string and question):
            return jsonify({"status": "Error", "message": "Missing required parameters"}), 400
        
        sql = model.SQL_gen(DDL_string,question)
        return jsonify({"status": "Success", "sql": sql}), 200

    except Exception as e:
        return jsonify({"status": "Error", "message": "Could not generate SQL. Reason: " + str(e)}), 500

# Connect to database and retrieve data with generated SQL
@app.route('/retrieve_data', methods=['POST'])
@cross_origin()
def connect_data():
    try:
        data_collect = request.get_json(force=True)
        database_url = data_collect.get('database_url')
        query = data_collect.get('query')
        database = data_collect.get('database_type')
        database_name = data_collect.get('database_name')
        
        if not (database_url and query and database and database_name):
            return jsonify({"status": "Error", "message": "Missing required parameters"}), 400

        if database == "postgres":
            p = postgres_connect(query,database_url,database_name)
            return p.connection()

        elif database == "mysql":
            m = mysql_connect(query,database_url,database_name)
            return m.connection()
    
    except Exception as e:
        return jsonify({"status": "Error", "message": "Could not connect to database. Reason: " + str(e)}), 500


# Add new database to the config file
@app.route('/addDB', methods=['POST'])
@cross_origin()
def addDatabase():
    data = json.loads(request.get_data())

    if data['database_name'] in config:
        return jsonify({"status": "Error", "message": "Database with this name already exists."}), 400

    # Add new database details to the config
    config[data['database_name']] = {
        'database_type': data['database_type'],
        'database_url': data['database_url'],
        'database_name': data['database_name']
    }

    with open(configfile, 'w') as cfg:
        config.write(cfg)

    return jsonify({"status": "Success", "message": "Database details added successfully!"})


# Get all databases from the config file
@app.route("/getDB", methods=['GET'])
@cross_origin()
def getDatabase():
    try:
        databases = []
        for section in config.sections():
            database = {
                'name': section,
                'type': config[section]['database_type'],
                'url': config[section]['database_url'],
                'database_name': config[section]['database_name']
            }
            databases.append(database)
        
        return jsonify({'status': 'Success', 'databases': databases}), 200
    except Exception as e:
        return jsonify({'status': 'Error', 'message': 'Could not retrieve databases. Reason: ' + str(e)}), 500


if __name__ == '__main__':
    config.read(configfile)
    app.run(debug=True, use_reloader=False)