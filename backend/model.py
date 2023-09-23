from transformers import AutoTokenizer, AutoModelForCausalLM

def SQL_gen(ddl_statement,question):
    model_name = "C:/Users/Ishaan/Documents/Text to SQL/Text2SQL-Query-Bot/backend/350Model"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    prompt = f"""{ddl_statement}
    -- Using valid SQLite, answer the following questions for the tables provided above.
    -- {question}
    SQL: """

    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    generated_ids = model.generate(input_ids, max_length=500)
    output = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    output = output.split('SQL:')[-1]
    print(output.strip())
    return(output.strip())


# SQL_gen("CREATE TABLE constructors (     constructor_id integer,     name character varying(100),     nationality character varying(100),     PRIMARY KEY (constructor_id) );CREATE TABLE circuits (     circuit_id integer,     altitude integer,     location character varying(50),     latitude character varying(10),     longitude character varying(10),     country character varying(50),     name character varying(100),     PRIMARY KEY (circuit_id) );CREATE TABLE drivers (     driver_id integer,     number integer,     code character,     forename character varying(20),     surname character varying(20),     dob character varying(20),     nationality character varying(50),     PRIMARY KEY (driver_id) );CREATE TABLE races (     race_id integer,     round integer,     circuit_id integer,     year character varying(10),     name character varying(50),     date_time character varying(25),     PRIMARY KEY (race_id) );CREATE TABLE driverstandings (     driverstandings_id integer,     race_id integer,     driver_id integer,     points integer,     position integer,     wins integer,     PRIMARY KEY (driverstandings_id) );CREATE TABLE laptimes (     race_id integer,     driver_id integer,     lap integer,     position integer,     time character varying(25),     PRIMARY KEY (race_id, driver_id, lap) );CREATE TABLE qualifying (     qualifying_id integer,     race_id integer,     driver_id integer,     constructor_id integer,     position integer,     q1 character varying(25),     q2 character varying(25),     q3 character varying(25),     PRIMARY KEY (qualifying_id) );CREATE TABLE constructorstandings (     constructorstandings_id integer,     race_id integer,     constructor_id integer,     position integer,     wins integer,     points character varying(10),     PRIMARY KEY (constructorstandings_id) );","Give me the location of circuits.")