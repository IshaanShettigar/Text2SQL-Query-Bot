from transformers import AutoTokenizer, AutoModelForCausalLM
import chromadb
from chromadb.utils import embedding_functions


def SQL_gen(ddl_statement,question):
    model_name = "C:/Users/Ishaan/Documents/Text to SQL/Text2SQL-Query-Bot/backend/350Model"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    external_knowledge = get_external_knowledge(question=question)

    prompt = f"""{ddl_statement}
    -- Use this information \n{external_knowledge}
    -- Using valid SQLite, answer the following questions for the tables provided above.
    -- {question}
    SQL: """

    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    generated_ids = model.generate(input_ids, max_length=2000)
    output = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    output = output.split('SQL:')[-1]
    print(output)
    # print(output.strip())
    return(output.strip())


# SQL_gen("CREATE TABLE constructors (     constructor_id integer,     name character varying(100),     nationality character varying(100),     PRIMARY KEY (constructor_id) );CREATE TABLE circuits (     circuit_id integer,     altitude integer,     location character varying(50),     latitude character varying(10),     longitude character varying(10),     country character varying(50),     name character varying(100),     PRIMARY KEY (circuit_id) );CREATE TABLE drivers (     driver_id integer,     number integer,     code character,     forename character varying(20),     surname character varying(20),     dob character varying(20),     nationality character varying(50),     PRIMARY KEY (driver_id) );CREATE TABLE races (     race_id integer,     round integer,     circuit_id integer,     year character varying(10),     name character varying(50),     date_time character varying(25),     PRIMARY KEY (race_id) );CREATE TABLE driverstandings (     driverstandings_id integer,     race_id integer,     driver_id integer,     points integer,     position integer,     wins integer,     PRIMARY KEY (driverstandings_id) );CREATE TABLE laptimes (     race_id integer,     driver_id integer,     lap integer,     position integer,     time character varying(25),     PRIMARY KEY (race_id, driver_id, lap) );CREATE TABLE qualifying (     qualifying_id integer,     race_id integer,     driver_id integer,     constructor_id integer,     position integer,     q1 character varying(25),     q2 character varying(25),     q3 character varying(25),     PRIMARY KEY (qualifying_id) );CREATE TABLE constructorstandings (     constructorstandings_id integer,     race_id integer,     constructor_id integer,     position integer,     wins integer,     points character varying(10),     PRIMARY KEY (constructorstandings_id) );","Give me the location of circuits.")


def get_external_knowledge(question):
    client = chromadb.PersistentClient(path='/chromastore')
    collection = client.get_collection(name="thrombosis_collection")
    ans = collection.query(
        query_texts=[question],
        n_results=1
    )

    ans = ans["documents"][0][0].split(',')
    finalStr = f"original_column_name: {ans[0]}\ncolumn_description: {ans[2]}\ndata_format: {ans[3]}\nvalue_description: {ans[4]}\n"
    # return ans["documents"][0][0]
    print(finalStr)
    return finalStr


# Thrombosis Prediction Test
ddl = """
CREATE TABLE Examination
(
    ID                 INTEGER          null,
    Examination Date DATE         null,
    aCL IgG          REAL        null,
    aCL IgM          REAL        null,
    ANA                INTEGER          null,
    ANA Pattern      TEXT null,
    aCL IgA          INTEGER          null,
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