# HOA Question-Answer System

This project functions as a proof-of-concept and its larger goal is to facilitate learning. Concepts reinforced by this project are:

- FastAPI/REST API
- Haystack Neural Search
- Streamlit Web Applications
- Docker
- Elasticsearch

## Project Setup

Pre-requisites: python3.7 or higher, docker

1. Create a new virtual environment

    ```bash
    python3 -m venv .venv
    ```

2. Activate the virtual environment

    ```bash
    source .venv/bin/activate
    ```

3. Install dependencies

    ```bash
    python3 -m pip install -r requirements.txt
    ```

## Initialize the Document Store

1. To start the docker container that will store all of our files, run the following:

    ```bash
    python3 initialize_docstore.py
    ```

    This function will also process and load our documents into the document store.

## Start the REST API

1. To start the API service. fun the following:

    ```bash
    uvicorn app:app --reload --app-dir rest_api/
    ```

## Start the Streamlit Web Interface

1. Streamlit is a lightweight package used for creating simple web applications. Run the following in a new terminal:

    ```bash
    streamlit run app-ui.py
    ```

    You should automatically be taken to a new webpage. If not, go to [http://localhost:8501](http://localhost:8501) in your browser. Here you will see a simple form to provide text input. Ask the system a question and you will receive an answer in json form. Below is an example of what you should see.

    ![Example of query and response](/images/streamlit-output-example.png)

## Things to Keep in Mind

- This entire system is built upon compounding errors.
  
- Each page of the pdf was converted to an image, each image was then converted to text using pdf2text and pytesseract.
  
- This is not meant to be treated as "definitive fact". Rather, it can be used to get a general idea of policies listed in the document.
