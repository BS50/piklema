import os
import re
import json
import random
import pytz
from datetime import datetime
import time
from dotenv import load_dotenv
from piklema.constants import input_data_list
from piklema.util import create_redis_client

load_dotenv()


def generate_data(data):
    data["timestamp"] = str(datetime.now(pytz.timezone("Europe/Moscow")))
    probability = round(random.random(), 1)
    if 0.4 < probability <= 0.6:
        data["device_id"] = 1000
    elif 0.6 < probability <= 0.8:
        for key, value in data.items():
            if re.fullmatch(r'tag_\d*', f"{key}"):
                data[key] = 5000
                break
    elif 0.8 < probability <= 1:
        data["tag_100"] = 150
    return data


with create_redis_client(os.getenv("REDIS_HOST_LOCAL")) as redis_db:
    while True:
        data = input_data_list[random.randint(0, len(input_data_list) - 1)]
        generated_data = generate_data(data)
        redis_db.rpush("data", json.dumps(generated_data))
        print(f"Data from the device with id = {generated_data['device_id']} is written to redis")
        time.sleep(2)
