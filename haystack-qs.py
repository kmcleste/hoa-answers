import os
import re
import logging
from typing import Optional

import docker

from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import ElasticsearchRetriever
from haystack.pipelines import ExtractiveQAPipeline
from haystack.nodes import FARMReader, TransformersReader
from haystack.utils import print_answers, convert_files_to_dicts, launch_es

def is_container_running(container_name: str) -> Optional[bool]:
    """Verify the status of a container by it's name

    :param container_name: the name of the container
    :return: boolean or None
    """
    RUNNING = "running"
    # Connect to Docker using the default socket or the configuration
    # in your environment
    docker_client = docker.from_env()
    # Or give configuration
    # docker_socket = "unix://var/run/docker.sock"
    # docker_client = docker.DockerClient(docker_socket)

    try:
        container = docker_client.containers.get(container_name)
    except docker.errors.NotFound as exc:
        print(f"Check container name!\n{exc.explanation}")
    else:
        container_state = container.attrs["State"]
        return container_state["Status"] == RUNNING

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
    return FARMReader(model_name_or_path=model, use_gpu=gpu)

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


def main():
    logger = logging.getLogger(__name__)
    path = '/Users/kmclester/Documents/hoa-topics/text'
    container_name = 'elasticsearch'

    if is_container_running(container_name=container_name):
        print(f'Container {container_name} is already running')
    else:
        # Launch ElasticSearch document store
        launch_es()

    # Create Document Store connection
    document_store = create_es_connection()

    # Preprocess documents
    dicts = convert_files_to_dicts(dir_path=path, split_paragraphs=True)

    # Write docs to document store
    document_store.write_documents(dicts)

    retriever = create_retriever(document_store)
    reader = create_reader(model='deepset/roberta-base-squad2', gpu=False)
    pipe = ExtractiveQAPipeline(reader, retriever)

    stop = False
    while stop == False:
        query = input("Enter your query: ")
        if query == '/stop':
            stop = True
        else:
            prediction = create_prediction(pipe=pipe, query=query)
            print_answers(prediction, details='minimum')


if __name__ == "__main__":
    main()