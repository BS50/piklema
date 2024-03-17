import re
import os
import json
import time
from json import JSONDecodeError
from dotenv import load_dotenv
import django
import yaml
import logging.config
from piklema.util import create_redis_client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from piklema.models import TagValue, Tag
from piklema.device_data_validator import DeviceDataValidator, DeviceNotFoundException, TagValueException, \
    TagNotFoundException, DeviceData

load_dotenv()


def create_tag_values(logger, device_data: DeviceData):
    for tag_obj in device_data.tag_values:
        tag = Tag.objects.get(name=tag_obj.name)
        TagValue.objects.create(
            tag_id=tag.pk,
            value=tag_obj.value,
            timestamp=device_data.timestamp,
            version=device_data.version
        )
        logger.info(f"Tag values with the name {tag.name} for the device with id = {device_data.device_id} saved")


def convert_data(row_device_data) -> DeviceData:
    device_data = {"tag_values": []}
    for key, value in row_device_data.items():
        if re.fullmatch(r'tag_\d*', f"{key}"):
            device_data["tag_values"].append({"name": key, "value": value})
        else:
            device_data[key] = value
    return DeviceData(**device_data)


if __name__ == "__main__":
    with open("./piklema/logging.yml", "rb") as file:
        logging_config = yaml.safe_load(file)
    logging.config.dictConfig(logging_config)
    logger = logging.getLogger()
    with create_redis_client(os.getenv("REDIS_HOST_BACKEND")) as redis_db:
        while True:
            try:
                raw_data = redis_db.lpop("data", 1)

                if raw_data:
                    raw_device_data = json.loads(raw_data[0])
                    logger.info(f"Data from the device with id = {raw_device_data['device_id']} read from redis")
                    device_data: DeviceData = convert_data(raw_device_data)
                    DeviceDataValidator.validate(device_data)
                    logger.info(f"The data received from the device with id = {device_data.device_id} is valid")
                    create_tag_values(logger, device_data)
                    logger.info(f"All tag values for the device with id = {device_data.device_id} saved")

            except DeviceNotFoundException as e:
                logger.error(e)
            except TagValueException as e:
                logger.warning(e)
            except TagNotFoundException as e:
                logger.warning(e)
            except JSONDecodeError as e:
                logger.warning(e)
            time.sleep(0.1)
