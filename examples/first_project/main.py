import logging
import os

from selvpcclient.client import Client, setup_http_client

logging.basicConfig(level=logging.INFO)

#
# You can create and get api token here
# https://support.selectel.ru/keys
#
VPC_TOKEN = os.getenv('SEL_TOKEN', None)

#
# You can get actual api URL here
# https://support.selectel.ru/vpc/docs
#
VPC_URL = "https://api.selectel.ru/vpc/resell"

REGION = "ru-2"
ZONE = "ru-2a"

http_client = setup_http_client(api_url=VPC_URL, api_token=VPC_TOKEN)
selvpc = Client(client=http_client)

project = selvpc.projects.create(name="Awesome Projectq12")
logging.info(
    "Project '%s' has been created with id '%s'", project.name, project.id)

quotas = {
    "quotas": {
        "compute_cores": [
            {
                "region": REGION,
                "zone": ZONE,
                "value": 1
            }
        ],
        "compute_ram": [
            {
                "region": REGION,
                "zone": ZONE,
                "value": 512
            }
        ],
        "volume_gigabytes_fast": [
            {
                "region": REGION,
                "zone": ZONE,
                "value": 5
            }
        ]
    }
}

project.update_quotas(quotas)
logging.info("Project quotas has been set")

floating_ips = {
    "floatingips": [
        {
            "region": REGION,
            "quantity": 1
        }
    ]
}

ip = project.add_floating_ips(floating_ips)[0]
logging.info("IP %s has been added", ip.floating_ip_address)
