LOGO_BASE64 = "0JzQvtGPINGA0LDQsdC+0YLQsCwg0Lgg0L/RgNCw0LLQuNC70LA="

LOGO_BASE64_SHORTEN = "0JzQvtGPINGA0LD ... NCw0LLQuNC70LA="

floatingips = {
    "floatingips": [
        {
            "region": "ru-1",
            "quantity": 4
        }
    ]
}

licenses = {
    "licenses": [
        {
            "region": "ru-1",
            "quantity": 4,
            "type": "license_windows_2012_standard"
        },
        {
            "region": "ru-2",
            "quantity": 1,
            "type": "license_windows_2012_standard"
        }
    ]
}

subnets = {
    "subnets": [
        {
            "region": "ru-1",
            "quantity": 4,
            "type": "ipv4",
            "prefix_length": 29
        }
    ]
}

quotas = {
    "compute_cores": [
        {
            "region": "ru-1",
            "zone": "ru-1a",
            "value": 10
        }
    ],
    "compute_ram": [
        {
            "region": "ru-1",
            "zone": "ru-1a",
            "value": 1024
        },
        {
            "region": "ru-1",
            "zone": "ru-1b",
            "value": 2048
        }
    ]
}

roles = {
    "roles": [
        {
            "project_id": "7354286c9ebf464d86efc16fb56d4fa3",
            "user_id": "5900efc62db34decae9f2dbc04a8ce0f"
        },
        {
            "project_id": "7354286c9ebf464d86efc16fb56d4fa3",
            "user_id": "5900efc62db34decae9f2dbc04a8ce0f"
        }
    ]
}

vrrp = {
    "vrrp_subnet": {
        "type": "ipv4",
        "prefix_length": 29,
        'quantity': 3,
        "regions": [
            "ru-1",
            "ru-2"
        ]
    }
}

keypair = {
    "keypair": {
        "user_id": "b832ef...94469d",
        "name": "my_key_name",
        "public_key": "ssh ... name@name"
    }

}
