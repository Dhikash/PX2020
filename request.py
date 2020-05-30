import json
import os
import sys
import time
from os.path import expanduser as ospath
# import fcntl

response = requests.get("https://opensky-network.org/api/states/all?lamin=-35&lomin=149&lamax=-32.5&lomax=153")