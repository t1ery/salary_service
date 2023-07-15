# Salary Service
This is a simple REST API service for viewing current salary and the date of the next raise. Each employee can only see their own salary. To ensure security, the service uses a token-based authentication system.

## Installation
1. Clone the repository.
2. Install `Poetry`, a dependency management tool for Python: `pip install poetry`
3. Install the required dependencies by running: `poetry install`
4. Create a `PostgreSQL` database and configure the connection in `database.py`.
5. Run the `create_table()` function from `database.py` to set up the database table.

## Usage
1. Activate the `Poetry` virtual environment by running: `poetry shell`
2. Start the server by running: `python main.py`
3. Access the API documentation at http://localhost:8000/docs in your browser.
4. Use the `/login` endpoint to obtain a token by providing your login and password.
5. Copy the obtained token.
6. Access the `/salary` endpoint and fill in the token field in the form to view your salary information and the date of the next raise.

## Running Tests
1. Make sure the server is not running.
2. Run the tests using the following command: `pytest test_main.py`
3. The tests are located in test_main.py and cover various scenarios, including login, token retrieval, and salary information retrieval.