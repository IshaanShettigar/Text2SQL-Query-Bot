from flask import Flask, jsonify, make_response
import pymysql

# Define a class that will handle connecting to an MYSQL database
class mysql_connect:
    def __init__(self,query,database_url,server_name,database_name,username,password):
        # Set the values for the various connection and query details
        self.database_url = database_url
        self.query = query
        self.server_name = server_name
        self.database_name = database_name
        self.username = username
        self.password = password

    # Function to create the connection to the database and execute the query
    def connection(self):
        try:
            # If no database_url is provided, use the individual components
            if self.database_url == "None":
                host = self.server_name
                user = self.username
                password = self.password
                db = self.database_name

            # Parse the database URL to get the individual components
            else:
                host = self.database_url.split("@")[1].split("/")[0]
                user = self.database_url.split("@")[0].split(":")[0]
                password = self.database_url.split("@")[0].split(":")[1]
                db = self.database_url.split("/")[1]

            col_names = []

            # Establish the database connection
            conn = pymysql.connect(host=host, user=user, password=password, db=db)
            cur = conn.cursor()

            # Depending on the query, execute different database commands
            if self.query == "None":
                cur.execute("SELECT * FROM circuits")
            elif "create" in self.query:
                # If the query contains "create", return an error message
                return make_response(jsonify({"status": "Error", "message": "Create not allowed"}),500)
            elif any(word in self.query for word in ("insert", "update", "delete")):
                # If the query contains "insert", "update", or "delete", execute the query
                cur.execute(self.query)
                conn.commit()
                cur.execute("SELECT * FROM circuits")
            else:
                cur.execute(self.query)

            # Retrieving the column names from the query results
            if cur.description is not None:
                col_names = [desc[0] for desc in cur.description]

            # Fetch all the results, convert the tuples to lists, and prepend the column names
            x = cur.fetchall()
            x = [list(i) for i in x]
            x = [col_names]+x

            # Close the cursor and the connection
            cur.close()
            conn.close()
            
            return jsonify({"status": "Success", "message": x})

        # Handle different types of errors
        except pymysql.Error as e:    
            return make_response(jsonify({"status": "Error", "message": str(e)}),500)
        except Exception as e:
            return make_response(jsonify({"status": "Error", "message": str(e)}),500)