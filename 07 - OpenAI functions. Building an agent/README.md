# DatabaseGPT

DatabaseGPT is a Python application designed to facilitate natural language querying of an SQLite database. By combining
OpenAI's GPT model with database schema parsing and SQL query generation, it allows users to ask database-related
questions and receive meaningful responses.

## Features

- Parses the SQLite database schema for table and column information.
- Allows natural language queries to be converted into SQL queries using GPT.
- Executes the SQL queries on the provided SQLite database and returns results.
- Handles retry logic and query correction for robust execution.
- Color-coded terminal-based conversation display using the `termcolor` package.

## Requirements

- Python 3.7+
- An OpenAI API key (stored as an environment variable `OPENAI_API_KEY`)
- SQLite database file (e.g., `db/movies.sqlite`)

## Installation

1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set the OpenAI API key as an environment variable:
    ```bash
    export OPENAI_API_KEY="your_openai_api_key"
    ```

4. Place your SQLite database file in the `db/` directory (default: `db/movies.sqlite`).

## Customization

- **Database File**: Update the `DATABASE` variable in `main.py` to point to your SQLite database.
- **Model**: Change the `MODEL` variable in `main.py` to use a different GPT model (e.g., `gpt-4`).
- **User Messages**: Modify the `USER_MESSAGE` variable in `main.py` to test different queries.

## Usage

1. Run the application:
    ```bash
    python main.py
    ```

2. The application will:
    - Parse the database schema.
    - Use OpenAI's GPT model to generate SQL queries based on user input.
    - Execute the SQL queries on the database and display results.

3. Example user message:
    ```
    Hi, what are the highest-rated movies among teenagers?
    ```

   The assistant will generate an appropriate SQL query, execute it, and return the results.

## Code Structure

### Key Components

#### `Conversation`

This class manages the conversation history and displays messages in a color-coded format based on the role (`system`,
`user`, `assistant`, or `function`).

#### `database_schema.py`

This module parses the SQLite database schema to extract table and column information and formats it for display or use
in SQL generation.

#### `ask_database`

This function takes an SQL query as input, executes it on the SQLite database, and returns the results.

#### `chat_completion_with_function_execution`

This function communicates with OpenAI's API to generate SQL queries based on user input and handles function calls for
database querying.

### Files

- `conversation.py`: Manages and displays the conversation.
- `database_schema.py`: Contains functions to parse and format the database schema.
- `main.py`: The entry point of the application.
- `requirements.txt`: Lists the required Python libraries.

## Key Logic Flow

1. **Schema Parsing**: The database schema is parsed to retrieve table and column names, which are passed to the GPT
   model to assist in query generation.
2. **GPT Query Generation**: GPT generates SQL queries based on user input and the schema.
3. **Query Execution**: The SQL query is executed, and results are returned.
4. **Error Handling**: If a query fails, the application attempts to regenerate and retry it.

## Example Output

### Terminal Display

```plaintext
system: You are DatabaseGPT, a helpful assistant who gets answers to user questions from the Database. Provide as many details as possible to your users. Begin!

user: Hi, what are the highest-rated movies among teenagers?

assistant: Based on the database, the highest-rated movies among teenagers are...
```

## Dependencies

- `openai`: For GPT API integration.
- `termcolor`: For color-coded terminal output.
- `sqlite3`: For database interaction.
- `tenacity`: For retry logic.
- `requests`: For making HTTP requests to OpenAI's API.

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key is required to make requests to GPT.
-

## Troubleshooting

1. **OpenAI API Key Error**:
   Ensure your OpenAI API key is correctly set as an environment variable.

2. **Database Connection Issues**:
   Ensure the SQLite database file exists and the path is correct.

3. **Query Errors**:
   If GPT generates an incorrect query, the retry logic will attempt to fix it. Check the logs for details.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

Feel free to extend or modify this application as per your needs. Happy querying!****