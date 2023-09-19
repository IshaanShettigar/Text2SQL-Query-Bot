from flask import Flask, request
from flask_cors import CORS, cross_origin
import json

# Import modules to connect to databases
from postgresCon import postgress_connect
from mysqlCon import mysql_connect

# Setup Flask app and configure CORS
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Route for handling database connections
@app.route('/connect', methods=['POST'])
@cross_origin()
def connect():
    # Get incoming request data
    data_collect = json.loads(request.get_data())

    # Get database details from request data
    database_url = data_collect['database_url']
    query = data_collect['query']
    database = data_collect['database_type']
    server_name = data_collect['server_address']
    database_name = data_collect['database_name']
    username = data_collect['username']
    password = data_collect['password']

    # Connect to the appropriate database based on request data
    if database == "postgres":
        p = postgress_connect(query,database_url,server_name,database_name,username,password)
        return p.connection()

    elif database == "mysql":
        m = mysql_connect(query,database_url,server_name,database_name,username,password)
        return m.connection()

    elif database == "mssql":
        ms = mssql_connect(query,database_url,server_name,database_name,username,password)
        return ms.connection()

# Start Flask app
if __name__ == '__main__':
    app.run(debug=True)