from flask import Flask, jsonify, make_response
import psycopg2

class postgres_connect:
    def __init__(self,query,database_url,database_name):
        self.query = query
        self.database_url = database_url
        self.database_name = database_name
    def connection(self):
        try:
            conn_string = self.database_url
            conn = psycopg2.connect(conn_string)
            cur = conn.cursor()

            if self.query == "None":
                cur.execute("SELECT * FROM circuits")
            elif "create" in self.query:
                return make_response(jsonify({"status": "Error", "message": "Create not allowed"}),500)
            elif any(word in self.query for word in ("insert", "update", "delete")):
                cur.execute(self.query)
                conn.commit()
                cur.execute("SELECT * FROM circuits")
            else:
                cur.execute(self.query)

            if cur.description is not None:
                col_names = [desc[0] for desc in cur.description]
                
            rows = cur.fetchall()
            x = [col_names]+rows

            cur.close()
            conn.close()
            return jsonify({"status": "Success", "message": x})
                
        except psycopg2.Error as e:     
            return make_response(jsonify({"status": "Error", "message": str(e)}),500)
        except Exception as e:
            return make_response(jsonify({"status": "Error", "message": str(e)}),500)