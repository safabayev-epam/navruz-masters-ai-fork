# MovieGPT: ChatGPT-Powered Movie Assistant

MovieGPT is an AI-powered web application that uses OpenAI's GPT model combined with a database and external tools to provide insights about movies. Whether you want a movie recommendation, database information, or a link to an IMDb page, MovieGPT has you covered.

---

## Features

- **AI-Powered Chat**: Powered by OpenAI's GPT models for natural conversations about movies.
- **Database Integration**: Queries a SQLite database for detailed movie information.
- **IMDb Link Fetching**: Automatically retrieves IMDb links for specific movies upon request.
- **Streamlit Interface**: User-friendly, interactive UI.

---

## How it Works

1. **Database Queries**:
    - MovieGPT uses a SQLite database (`movies_2.sqlite`) to fetch relevant information.
    - It dynamically generates SQL queries based on user interaction and the database structure.

2. **External Tool Integrations**:
    - IMDb link retrieval is managed via a custom utility (`ImdbMovieLinkFetcher`).
    - Functions like `ask_database` and `get_movie_link` are used for seamless integration.

3. **Robust Error Handling**:
    - Improves failed queries dynamically by asking GPT to resolve issues.

4. **Conversation Management**:
    - Maintains conversation history using Streamlit's session state for a natural chat experience.

---

## Installation

Before running this application, ensure all dependencies are installed and properly set up.

### Prerequisites

1. **Python**: Ensure you have Python 3.7 or higher installed.
2. **Libraries**: Install the required Python libraries using the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```
3. **SQLite**: Ensure `movies_2.sqlite` is present in the project directory.

### Clone the Repository

```bash
git clone https://github.com/your-repo-url/MovieGPT
cd MovieGPT
```

---

## Running the Application

Run the following command to start the Streamlit application:

```bash
streamlit run main.py
```

Once the app is running, open your browser and navigate to `http://localhost:8501`.

---

## Project Structure

- **`main.py`**: Entry point of the application. Contains the Streamlit interface and chatbot logic.
- **`tools`**: Utility functions for database interaction and IMDb link fetching.
    - `movie_search_utils.py`: Utility class to fetch IMDb links.
    - `database_interaction.py`: Handles database schema retrieval and SQL execution.
- **`conversation.py`**: Manages system and user conversation history in a structured format.
- **`movies_2.sqlite`**: SQLite database containing movie-related data.

---

## Key Components

### Functions

1. **`chat_completion_request()`**:
    - Sends chat-based API requests to the OpenAI GPT model.
    - Supports both standard messages and tool integrations.

2. **`try_ask_database()`**:
    - Handles dynamic SQL generation and execution.
    - Automatically fixes SQL errors using model suggestions.

3. **`get_imdb_link()`**:
    - Fetches IMDb links using the movie title.

4. **`call_function()`**:
    - Routes tool calls (`ask_database`, `get_movie_link`) for execution.

### Streamlit Features

- Chat interface enabling users to ask about movies.
- Displays conversation history.
- Dynamically updates assistant responses.

---

## Example Use Cases

1. **Ask for IMDb Link**:
    - Input: "Find me the link to the movie Inception."
    - Output: MovieGPT provides the exact IMDb link.

2. **Fetch Database Information**:
    - Input: "How many movies are in the database?"
    - Output: MovieGPT queries the SQLite database and displays the result.

3. **Recommendations**:
    - Input: "Can you suggest action movies?"
    - Output: MovieGPT retrieves possible action movies from the database.

---

## Error Handling

- **SQL Errors**:
  Automatically resolves malformed SQL queries with retries.
- **External API Errors**:
  Logs errors and ensures smooth fallback mechanisms.

---

## Requirements

- **Libraries**:
    - `streamlit`
    - `sqlite3`
    - `openai`
    - `logging`

Install them using the `pip install` command.

---

## Developers

Feel free to extend the application by adding new tools or modifying database schemas. Refer to the `main.py` file for key functionalities.

---

## Contribution

Contributions are welcome! Please fork the repository and submit a pull request for any changes.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.# masters-ai