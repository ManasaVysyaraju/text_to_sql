# Text-to-SQL Query System with CSV and MySQL

This is a Flask-based REST API that converts natural language questions into SQL queries using the Google Gemini model. It can query data from either a MySQL database or a CSV file, depending on the type of question asked.

## Features

- Convert English questions into SQL queries using Google Gemini AI.
- Query data from both MySQL databases and CSV files.
- CORS support for cross-origin requests.
- Easily configurable environment variables for MySQL and Google API keys.

## Installation

### Prerequisites
- Python 3.8 or higher
- Flask
- MySQL
- Google Generative AI (Gemini) API key
- A CSV file (e.g., `sales_inventory.csv`)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ManasaVysyaraju/text_to_sql.git
   cd text_to_sql
