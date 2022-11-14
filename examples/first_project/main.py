import logging
import os

from selvpcclient.client import Client, setup_http_client
from selvpcclient.httpclient import RegionalHTTPClient

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

#
# Keystone identity URL
# You can get actual api URL here
# https://support.selectel.ru/vpc/docs
#
IDENTITY_URL = os.getenv('OS_AUTH_URL', 'https://api.selvpc.ru/identity/v3')

REGION = "ru-2"
ZONE = "ru-2c"

http_client = setup_http_client(api_url=VPC_URL, api_token=VPC_TOKEN)
regional_http_client = RegionalHTTPClient(http_client=http_client,
                                          identity_url=IDENTITY_URL)

selvpc = Client(client=http_client, regional_client=regional_http_client)

project = selvpc.projects.create(name="Awesome Projectq12")
logging.info(
    "Project '%s' has been created with id '%s'", project.name, project.id)

project_limits = selvpc.quotas.get_project_limits(project_id=project.id,
                                                  region=REGION)

logging.info(f"Project limits received. "
             f"Limits for resource `compute_cores` in region `{REGION}`: "
             f"{project_limits.compute_cores}")

quotas = {
    "quotas": {
        "compute_cores": [
            {
                "zone": ZONE,
                "value": 1
            }
        ],
        "compute_ram": [
            {
                "zone": ZONE,
                "value": 512
            }
        ],
        "volume_gigabytes_fast": [
            {
                "zone": ZONE,
                "value": 5
            }
        ]
    }
}

project.update_quotas(region=REGION, quotas=quotas)
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
