#!/.venv/bin/python

from typing import Optional
from time import sleep

import docker

from haystack.document_stores import ElasticsearchDocumentStore
from haystack.utils import convert_files_to_dicts, launch_es

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


def main():
    path = 'data/text'
    container_name = 'elasticsearch'

    if is_container_running(container_name=container_name):
        print(f'Container {container_name} is already running')
    else:
        # Launch ElasticSearch document store
        launch_es()
        sleep(15)

    # Create Document Store connection
    document_store = create_es_connection()

    # Preprocess documents
    dicts = convert_files_to_dicts(dir_path=path, split_paragraphs=True)

    # Write docs to document store
    document_store.write_documents(dicts)


if __name__ == "__main__":
    main()