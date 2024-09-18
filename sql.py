from dotenv import load_dotenv
import streamlit as st
import os
import mysql.connector
import google.generativeai as genai


load_dotenv()


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(question, prompt):
   
    model = genai.GenerativeModel('models/gemini-1.0-pro-latest')
    response = model.generate_content([prompt[0], question])
    sql_query = response.text.strip().strip("`")  

    return sql_query


def read_sql_query(sql, db_config):
    try:
        conn = mysql.connector.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"]
        )
        cur = conn.cursor()

        
        cur.execute(sql)
        rows = cur.fetchall()

        cur.close()
        conn.close()

        for row in rows:
            print(row)

        return rows

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

prompt = [
    """
You are an expert in converting English questions into SQL queries! The system has access to multiple predefined tables, such as `users` and `orders`, each containing various fields. The `users` table includes columns like `username`, `product`, `amount`, and `date`, while the `orders` table includes `order_id`, `user_id`, `order_date`, and `total_amount`. For example, if the question is "Show me all transactions in the last month," the SQL command should be something like `SELECT * FROM orders WHERE order_date >= CURDATE() - INTERVAL 1 MONTH;`. For a question like "List all users who purchased a specific product," the SQL command should be something like `SELECT * FROM users WHERE product = 'Product_Name';`. Ensure the SQL code is concise, without any special characters or the word "sql". The system should determine the correct table based on the query and return the appropriate SQL.    
    """
]

st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question = st.text_input("Input: ", key="input")

submit = st.button("Ask the question")

db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

if submit:
    sql_query = get_gemini_response(question, prompt)
    print(sql_query)

    response = read_sql_query(sql_query, db_config)

    st.subheader("The Response is")
    for row in response:
        st.write(row)
