import unittest
import subprocess
import time
import sys
import os
from apf.consumers import AVROFileConsumer
FILE_PATH = os.path.dirname(__file__)
STEP_PATH = os.path.join(FILE_PATH,"..")
sys.path.append(STEP_PATH)
from xmatch_step import XmatchStep

class StepTest(unittest.TestCase):
    container_name = "test_postgres"
    container = None

    def test_execute(self):
        DB_CONFIG = {}
        CONSUMER_CONFIG={
            "DIRECTORY_PATH": os.path.join(FILE_PATH, "examples/avro_test"),
            "NUM_MESSAGES": 5
        }
        PRODUCER_CONFIG={
            "CLASS": 'apf.producers.GenericProducer'
        }
        XMATCH_CONFIG = {
        			"CATALOG" : {
        						"name" : "allwise",
        						"columns" : [
        								'AllWISE',
        								'RAJ2000',
        								'DEJ2000',
        								'W1mag',
        								'W2mag',
        								'W3mag',
        								'W4mag',
        								'e_W1mag',
        								'e_W2mag',
        								'e_W3mag',
        								'e_W4mag',
        								'Jmag',
        								'e_Jmag',
        								'Hmag',
        								'e_Hmag',
        								'Kmag',
        								'e_Kmag'
        						]
        			}
        }
        step = XmatchStep(consumer=AVROFileConsumer(CONSUMER_CONFIG),
                          config={
                            "DB_CONFIG": DB_CONFIG,
                            "PRODUCER_CONFIG":PRODUCER_CONFIG,
                            "STEP_VERSION": "test",
                            "XMATCH_CONFIG": XMATCH_CONFIG
                          }
                )
        step.start()