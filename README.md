# Text2SQL-Query-Bot
This project aims to create a bot that harnesses the power of LLM's like Llama 2 to convert **natural language queries to SQL queries**. 
We aim to achieve state-of-the-art scores against the latest benchmarks such as [Spider](https://yale-lily.github.io/spider) and [BIRD](https://arxiv.org/pdf/2305.03111.pdf). We will explore the technique of "In-context learning". 

## Challenges 
We will assume we are working with **Llama 2 13billion**. In order to achieve better performance we have to provide the LLM with all the information it needs to process a particular query (Schema linking information). We need to include the **schema information** in the prompt. We need to specify what values can occur in each column and what they mean so the model can understand the natural language query and map it to the corresponding value in the column of the database table. For example: Type 1 diabetes mellitus might be abbreviated to **T1D** in the database. 
We also need to give the LLM access to **external knowledge** such as:
1. **Numerical reasoning**
2. **Special domain knowledge**:
Example query: Find the patients who have an abnormal level of blood pressure.
Explanation: The LLM should know what level of BP is considered normal, it should correlate this to the correct unit representation in the column of the database table. 
3. **Synonym knowledge**
4. **Value illustration** as mentioned above.

## Methods
1. Zeroshot Inference
2. Oneshot Inference (pre-determined/static examples)
3. Fewshot inference (pre-determined/static examples)
4. Oneshot inference




## References
1. Can LLM Already Serve as A Database Interface? A BIg Bench for Large-Scale Database Grounded Text-to-SQLs ([link](https://arxiv.org/pdf/2305.03111.pdf))
2. DIN-SQL: Decomposed In-Context Learning of Text-to-SQL with Self-Correction ([link](https://arxiv.org/pdf/2304.11015.pdf))
3. SQL-PALM: IMPROVED LARGE LANGUAGE MODEL ADAPTATION FOR TEXT-TO-SQL ([link](https://arxiv.org/abs/2306.00739))
