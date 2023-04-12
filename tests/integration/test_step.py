import pytest
import unittest

from xmatch_step import XmatchStep
from db_plugins.db.sql.models import Object, Step
from cds_xmatch_client import XmatchClient
from schema_old import SCHEMA
from unittest import mock
from tests.data.messages import (
    generate_input_batch,
    get_default_object_values,
    get_fake_xmatch,
    get_fake_empty_xmatch,
)

CONSUMER_CONFIG = {
    "CLASS": "apf.consumers.KafkaConsumer",
    "PARAMS": {
        "bootstrap.servers": "server",
        "group.id": "group_id",
        "auto.offset.reset": "beginning",
        "enable.partition.eof": False,
    },
    "TOPICS": ["topic"],
    "consume.messages": "1",
    "consume.timeout": "10",
}

PRODUCER_CONFIG = {
    "TOPIC": "test",
    "PARAMS": {
        "bootstrap.servers": "localhost:9092",
    },
    "SCHEMA": SCHEMA,
}

XMATCH_CONFIG = {
    "CATALOG": {
        "name": "allwise",
        "columns": [
            "AllWISE",
            "RAJ2000",
            "DEJ2000",
            "W1mag",
            "W2mag",
            "W3mag",
            "W4mag",
            "e_W1mag",
            "e_W2mag",
            "e_W3mag",
            "e_W4mag",
            "Jmag",
            "e_Jmag",
            "Hmag",
            "e_Hmag",
            "Kmag",
            "e_Kmag",
        ],
    }
}


@pytest.mark.usefixtures("psql_service")
class StepXmatchTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # this step only for setup db
        cls.step_config = {
            "CONSUMER_CONFIG": CONSUMER_CONFIG,
            "PRODUCER_CONFIG": PRODUCER_CONFIG,
            "STEP_METADATA": {
                "STEP_VERSION": "xmatch",
                "STEP_ID": "xmatch",
                "STEP_NAME": "xmatch",
                "STEP_COMMENTS": "xmatch",
            },
            "XMATCH_CONFIG": XMATCH_CONFIG,
            "RETRIES": 3,
            "RETRY_INTERVAL": 1,
        }
        producer = mock.MagicMock()
        cls.step = XmatchStep(
            config=cls.step_config, producer=producer, insert_metadata=False
        )
        cls.batch = generate_input_batch(20)

    @classmethod
    def tearDownClass(cls):
        cls.step.driver.drop_db()
        cls.step.driver.session.close()

    def setUp(self):
        self.step.driver.create_db()
        array = [
            get_default_object_values(i) for i, x in enumerate(self.batch)
        ]
        self.step.driver.query(Object).bulk_insert(array)

    def tearDown(self):
        self.step.driver.session.close()
        self.step.driver.drop_db()

    def test_insert_step_metadata(self):
        self.step.insert_step_metadata()
        self.assertEqual(len(self.step.driver.query(Step).all()), 1)

    @mock.patch.object(XmatchClient, "execute")
    def test_execute(self, mock_xmatch: mock.Mock):
        mock_xmatch.return_value = get_fake_xmatch(self.batch)
        self.step.execute(self.batch)

    @mock.patch.object(XmatchClient, "execute")
    def test_execute_empty_xmatch(self, mock_xmatch: mock.Mock):
        mock_xmatch.return_value = get_fake_empty_xmatch(self.batch)
        self.step.execute(self.batch)

    def test_insert_metadata(self):
        self.step.insert_step_metadata()
