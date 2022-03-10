# HOA Question-Answer System

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

## Launching the HOA QA Service

1. Run the `haystack-qs.py` script

    ```bash
    python3 haystack-qs.py
    ```

2. This will take a few seconds to initialize. Once it is ready, you should see **Enter your query:** appear in the terminal window. Now you can ask the service anything pertaining to the HOA guidelines listed the [included pdf](https://github.com/kmcleste/hoa-answers/blob/main/data/hoa-rules.pdf).
   - Note: Make sure you ask questions in the form of a complete sentence. Keyword input will not return a response.

## Things to Keep in Mind

- This entire system is built upon compounding errors.
- Each page of the pdf was converted to an image, each image was then converted to text using pdf2text and pytesseract.
- No further processing was done on the document.
- This is not meant to be treated as "the truth and nothing but the truth". Rather, it can be used to get a general idea of policies listed in the document.
