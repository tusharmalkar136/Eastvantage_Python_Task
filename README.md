# FastAPI Address Book Application

This is a simple address book application built using FastAPI.

## How to Run

1. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```


2. Set up the environment variables by creating a `.env` file in the root directory with the following content:
    ```
    DATABASE_URL="mssql+pyodbc://username:password@hostname/database"
    ```

3. Run the FastAPI application using uvicorn:
    ```bash
    uvicorn Test_main:app --reload
    ```

4. Access the application in your web browser at `http://127.0.0.1:8000`.
