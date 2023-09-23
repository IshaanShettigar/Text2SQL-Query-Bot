from flask import Flask, jsonify, make_response
import mysql.connector
from mysql.connector import errorcode

class mysql_DDL:
    def __init__(self, database_url, database_name):
        self.database_url = database_url
        self.database_name = database_name

    def connection(self):
        try:
            conn = mysql.connector.connect(host='your_host', user='your_user', password='your_password', database=self.database_name)
            cur = conn.cursor()

            cur.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = %s
            """, (self.database_name,))
            tables = [table[0] for table in cur.fetchall()]
            ddl_statements = []

            for table in tables:
                cur.execute("""
                    SELECT column_name, data_type, character_maximum_length
                    FROM information_schema.columns
                    WHERE table_name = %s AND table_schema = %s
                """, (table, self.database_name,))
                columns = cur.fetchall()

                columns_sql_list = []
                for column in columns:
                    column_name, data_type, char_max_len = column
                    if data_type == 'varchar':
                        data_type = f"{data_type}({char_max_len})"
                    columns_sql_list.append(f"{column_name} {data_type}")

                cur.execute("""
                    SELECT kcu.column_name
                    FROM information_schema.table_constraints tc
                    JOIN information_schema.key_column_usage kcu
                    ON tc.constraint_name = kcu.constraint_name
                    WHERE tc.table_name = %s AND tc.table_schema = %s AND tc.constraint_type = 'PRIMARY KEY'
                """, (table, self.database_name,))
                primary_keys = [row[0] for row in cur.fetchall()]
                if primary_keys:
                    columns_sql_list.append(f"PRIMARY KEY ({', '.join(primary_keys)})")

                columns_sql = ",\n    ".join(columns_sql_list)
                ddl_statements.append(f"CREATE TABLE {table} (\n    {columns_sql}\n);")

            cur.close()
            conn.close()
            return jsonify({"status": "Success", "message": ddl_statements})

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                return make_response(jsonify({"status": "Error", "message": "Something is wrong with your user name or password"}), 500)
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                return make_response(jsonify({"status": "Error", "message": "Database does not exist"}), 500)
            else:
                return make_response(jsonify({"status": "Error", "message": str(err)}), 500)
        except Exception as e:
            return make_response(jsonify({"status": "Error", "message": str(e)}), 500)
