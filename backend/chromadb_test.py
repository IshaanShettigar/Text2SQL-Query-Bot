import chromadb
from chromadb.utils import embedding_functions


import json
import pandas as pd

client = chromadb.PersistentClient(path='/chromastore')


# collection = client.create_collection(name="thrombosis_collection")


# 1155 1157 1159 1172 1176 1177 1178 1188 1196 1197 1198 1199 1204 1206

with open('C:/Users/Ishaan/Documents/Text to SQL/dev_20230613/dev.json','r') as file:
    data = json.load(file)
    df = pd.DataFrame(data)

# Filter the DataFrame based on db_id and difficulty
    filtered_df = df[(df['db_id'] == 'thrombosis_prediction') & (df['difficulty'] == 'simple')]


import sqlite3

# Replace 'your_database_file.db' with the path to your SQLite database file
database_file = "C:/Users/Ishaan/Documents/Text to SQL/dev_20230613/dev_databases/thrombosis_prediction/thrombosis_prediction.sqlite"

conn = sqlite3.connect(database_file)
cursor = conn.cursor()

# to get the DDL statements
# cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table';")
# table_info = cursor.fetchall()

# Iterate through the table_info result and print CREATE statements
# for table_name, create_statement in table_info:
#     print(f"Table Name: {table_name}")
#     print("Create Statement:")
#     print(create_statement)
#     print("\n")




# # Print the number of tables and their names
# print(f"Number of tables: {len(table_names)}")
# print("Table names:")
# for table_name in table_names:
#     print(table_name)
print("Ground truth\nSELECT Symptoms FROM Examination WHERE Diagnosis = 'SLE' GROUP BY Symptoms ORDER BY COUNT(Symptoms) DESC LIMIT 1;")
cursor.execute("SELECT Symptoms FROM Examination WHERE Diagnosis = 'SLE' GROUP BY Symptoms ORDER BY COUNT(Symptoms) DESC LIMIT 1;")
res = cursor.fetchall()
print(res)

q = "select ID from Laboratory where FG < 150 or FG > 450"
print("NSQL 350M\n",q)
cursor.execute(q)
res = cursor.fetchall()
print(res)
# for r in res:
#     print(r)

# cursor.execute("SELECT * FROM Patient")
# print(cursor.fetchall())

# cursor.execute("SELECT * FROM Laboratory")
# print(cursor.fetchall())

cursor.close()
conn.close()


"""
CREATE TABLE Examination
(
    ID                 INTEGER          null,
    `Examination Date` DATE         null,
    `aCL IgG`          REAL        null,
    `aCL IgM`          REAL        null,
    ANA                INTEGER          null,
    `ANA Pattern`      TEXT null,
    `aCL IgA`          INTEGER          null,
    Diagnosis          TEXT null,
    KCT                TEXT null,
    RVVT              TEXT null,
    LAC                TEXT null,
    Symptoms           TEXT null,
    Thrombosis         INTEGER          null,
    foreign key (ID) references Patient (ID)
            on update cascade on delete cascade
)


Table Name: Patient
Create Statement:
CREATE TABLE Patient
(
    ID           INTEGER default 0 not null
        primary key,
    SEX          TEXT  null,
    Birthday     DATE          null,
    Description  DATE          null,
    `First Date` DATE          null,
    Admission    TEXT  null,
    Diagnosis    TEXT  null
)


Table Name: Laboratory
Create Statement:
CREATE TABLE Laboratory
(
    ID        INTEGER  default 0            not null,
    Date      DATE default '0000-00-00' not null,
    GOT       INTEGER                       null,
    GPT       INTEGER                        null,
    LDH       INTEGER                        null,
    ALP       INTEGER                        null,
    TP        REAL             null,
    ALB       REAL             null,
    UA        REAL             null,
    UN        INTEGER                       null,
    CRE       REAL             null,
    `T-BIL`   REAL             null,
    `T-CHO`   INTEGER                       null,
    TG        INTEGER                       null,
    CPK       INTEGER                       null,
    GLU       INTEGER                       null,
    WBC       REAL             null,
    RBC       REAL             null,
    HGB       REAL             null,
    HCT       REAL             null,
    PLT       INTEGER                       null,
    PT        REAL             null,
    APTT      INTEGER                       null,
    FG        REAL             null,
    PIC       INTEGER                       null,
    TAT       INTEGER                       null,
    TAT2      INTEGER                       null,
    `U-PRO`   TEXT              null,
    IGG       INTEGER                       null,
    IGA       INTEGER                       null,
    IGM       INTEGER                       null,
    CRP       TEXT              null,
    RA        TEXT              null,
    RF        TEXT              null,
    C3        INTEGER                       null,
    C4        INTEGER                       null,
    RNP       TEXT              null,
    SM        TEXT              null,
    SC170     TEXT              null,
    SSA       TEXT              null,
    SSB       TEXT              null,
    CENTROMEA TEXT              null,
    DNA       TEXT              null,
    `DNA-II`  INTEGER                       null,
    primary key (ID, Date),
        foreign key (ID) references Patient (ID)
            on update cascade on delete cascade
)
"""

# SQL_gen(ddl,"For patient with albumin level lower than 3.5, list their ID, sex and diagnosis.")
# SQL_gen(ddl,"For patients with a mild degree of thrombosis, list their ID, sex and diseases the patient is diagnosed with.")
# get_external_knowledge("For patients with a  severe degree of thrombosis, list their ID, sex and dieseas the patient is diagnosed with.")


# def scehma_linking(ddl,question):
#     model_name = "C:/Users/Ishaan/Documents/Text to SQL/Text2SQL-Query-Bot/backend/350Model"

#     tokenizer = AutoTokenizer.from_pretrained(model_name)
#     model = AutoModelForCausalLM.from_pretrained(model_name)

#     prompt = f"""{ddl} 
#     -- Using the tables above can you tell me which tables and columns are required to execute the natural language question below?
#     -- {question}
#     The tables are """
#     input_ids = tokenizer(prompt, return_tensors="pt").input_ids
#     generated_ids = model.generate(input_ids, max_length=1000)
#     output = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
#     output = output.split('SQL:')[-1]
#     print(output.strip())
#     return(output.strip())

# scehma_linking(ddl,"For patients with a mild degree of thrombosis, list their ID, sex and diseases the patient is diagnosed with.")

def PaLMSQL_gen(ddl_statement, question):
 pass