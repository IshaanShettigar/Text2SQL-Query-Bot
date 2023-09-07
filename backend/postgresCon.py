from flask import Flask, jsonify, make_response
import psycopg2

# Define a class that will handle connecting to an PostgreSQL database
class postgress_connect:
    def __init__(self,query,database_url,server_name,database_name,username,password):
        self.query = query
        self.database_url = database_url
        self.server_name = server_name
        self.database_name = database_name
        self.username = username
        self.password = password
    def connection(self):
        try:
            if self.database_url == "None":
                conn_string= f"host={self.server_name} dbname={self.database_name} user={self.username} password={self.password} sslmode=require"
            else:
                conn_string = self.database_url

            # Establish the database connection
            conn = psycopg2.connect(conn_string)
            cur = conn.cursor()

            # Depending on the query, execute different database commands
            if self.query == "None":
                cur.execute("SELECT * FROM circuits")
            elif "create" in self.query:
                # If the query contains "create", return an error message
                return make_response(jsonify({"status": "Error", "message": "Create not allowed"}),500)
            elif any(word in self.query for word in ("insert", "update", "delete")):
                cur.execute(self.query)
                conn.commit()
                cur.execute("SELECT * FROM circuits")
            else:
                cur.execute(self.query)

            # Retrieving the column names from the query results
            if cur.description is not None:
                col_names = [desc[0] for desc in cur.description]
                
            # Fetch all the results, convert the tuples to lists, and prepend the column names
            rows = cur.fetchall()
            x = [col_names]+rows

            # Close the cursor and the connection
            cur.close()
            conn.close()
            return jsonify({"status": "Success", "message": x})
                
        # Handle different types of errors
        except psycopg2.Error as e:     
            return make_response(jsonify({"status": "Error", "message": str(e)}),500)
        except Exception as e:
            return make_response(jsonify({"status": "Error", "message": str(e)}),500)