from flask import Flask, request, jsonify, send_from_directory
import mysql.connector
import os
from dotenv import load_dotenv
import google.generativeai as genai

app = Flask(__name__)

# Load all the environment variables
load_dotenv()

# Configure GenAI Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to Load Google Gemini Model and provide queries as response
def get_gemini_response(question, prompt):
    # Create a model instance with 'gemini'
    model = genai.GenerativeModel('models/gemini-1.0-pro-latest')
    # Generate response using the model
    response = model.generate_content([prompt[0], question])
    sql_query = response.text.strip().strip("`")  

    return sql_query

# Function to retrieve query from the MySQL database
def read_sql_query(sql, db_config):
    try:
        # Connect to MySQL database using the credentials
        conn = mysql.connector.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"]
        )
        cur = conn.cursor()

        # Execute the SQL query
        cur.execute(sql)
        rows = cur.fetchall()

        # Close the connection
        cur.close()
        conn.close()

        return rows

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

# Define Your Prompt
prompt = [
    """
You are an expert in converting English questions into SQL queries! The system has access to multiple predefined tables, such as `users` and `orders`, each containing various fields. The `users` table includes columns like `username`, `product`, `amount`, and `date`, while the `orders` table includes `order_id`, `user_id`, `order_date`, and `total_amount`. For example, if the question is "Show me all transactions in the last month," the SQL command should be something like `SELECT * FROM orders WHERE order_date >= CURDATE() - INTERVAL 1 MONTH;`. For a question like "List all users who purchased a specific product," the SQL command should be something like `SELECT * FROM users WHERE product = 'Product_Name';`. Ensure the SQL code is concise, without any special characters or the word "sql". The system should determine the correct table based on the query and return the appropriate SQL.
    """
]
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_from_directory('.', 'web.html')

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    question = data.get('question')
    
    if not question:
        return jsonify({"error": "No question provided"}), 400

    sql_query = get_gemini_response(question, prompt)
    print("Generated SQL Query:", sql_query)

    db_config = {
        "host": os.getenv("DB_HOST"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME")
    }

    response = read_sql_query(sql_query, db_config)

    return jsonify({
        "question": question,
        "sql_query": sql_query,
        "results": response
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
