import logging
import os
import pytest
from apf.producers import KafkaProducer
from confluent_kafka.admin import AdminClient, NewTopic
from tests.data.schemas.input_schema import SCHEMA
from tests.data.messages import generate_input_batch

@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    return os.path.join(
        str(pytestconfig.rootdir), "tests/integration", "docker-compose.yml"
    )


def is_kafka_responsive(url):
    client = AdminClient({"bootstrap.servers": url})
    future = client.create_topics(
        [
            NewTopic("correction", num_partitions=1),
            NewTopic("xmatch", num_partitions=1),
            NewTopic("w_object", num_partitions=1),
        ]
    )
    for topic, future in future.items():
        try:
            future.result()
        except Exception as e:
            logging.error("Can't create topic %s: %s", topic, e)
            return False

    return True


@pytest.fixture(scope="session")
def kafka_service(docker_ip, docker_services):
    """Ensure that Kafka service is up and responsive."""
    port = docker_services.port_for("kafka", 9092)
    server = "{}:{}".format(docker_ip, port)
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: is_kafka_responsive(server)
    )
    produce_messages("correction")
    return server

def produce_messages(topic):
    producer = KafkaProducer({
        "PARAMS": { "bootstrap.servers": "localhost:9092" },
        "TOPIC": topic,
        "SCHEMA": SCHEMA
    })

    messages = generate_input_batch(20)
    producer.set_key_field("aid")
    
    for message in messages:
        producer.produce(message)
