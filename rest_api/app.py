__author__ = "Kyle McLester"
__version__ = "1.0"
__status__ = "Prototype"
__date__ = "2022/03/10"

from fastapi import FastAPI
from pydantic import BaseModel, validator

from haystack import __version__
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import ElasticsearchRetriever
from haystack.pipelines import ExtractiveQAPipeline
from haystack.nodes import FARMReader, TransformersReader
from haystack.utils import print_answers

def create_es_connection():
    # Connect to ElasticSearch
    document_store = ElasticsearchDocumentStore(
        host="localhost",
        username="",
        password="",
        index="document",
    )
    return document_store

def create_retriever(document_store):
    return ElasticsearchRetriever(document_store=document_store)

def create_reader(model: str, gpu: bool):
    return FARMReader(model_name_or_path=model, use_gpu=gpu, context_window_size=450)

def create_prediction(pipe, query: str):
    prediction = pipe.run(query=query, params={
        "Retriever":{
            "top_k":10
        }, 
        "Reader":{
            "top_k": 3
        }
    })
    return prediction

app = FastAPI(title="HOA Haystack API")

document_store = create_es_connection()
retriever = create_retriever(document_store)
reader = create_reader(model='deepset/roberta-base-squad2', gpu=False)
pipe = ExtractiveQAPipeline(reader, retriever)

@app.get("/")
def root() -> dict:
    """
    Returns authors, current version, project status, and the most recent modified date as a json-blob.
    """
    return {
        "author": __author__,
        "version": __version__,
        "status": __status__,
        "date modified": __date__
    }

@app.get("/haystack-version/")
def haystack_version() -> dict:
    """
    Returns the current version of Haystack used in the QA System
    """
    return {"version": __version__}

class Query(BaseModel):
    query: str

    @validator("query")
    def validate_query_length(cls, value):
        # Validation check to make sure user does not enter a single keyword as input 
        if len(value) <= 25:
            raise ValueError(f"Query expected to have length >= 25, recieved {len(value)}")
        return value

@app.post("/haystack-query/")
def haystack_query(query: Query) -> dict:
    """
    Takes a `query` dictionary/json as input and passes the paramters to the Haystack pipe function.
    Haystack then returns a list with the answer, confidence score, and meta data. If multiple answers
    returned, they will be converted into a dictionary and returned to the user as a json-blob.
    """
    question = query.query

    # Runs a query on document store and returns the top-k answers
    prediction = create_prediction(pipe=pipe, query=question)
    resp = {}
    # Answers objects must be converted to a dictonary to display correctly
    for idx, answer in enumerate(prediction['answers']):
        resp[idx] = answer.to_dict()
    return resp