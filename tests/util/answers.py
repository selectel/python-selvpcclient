from tests.util.params import LOGO_BASE64

ACCOUNT_INFO = {
    "account": {
        "enabled": True,
        "locked": False,
        "locks": [],
        "name": "fake_domain",
        "onboarding": False
    }
}

PROJECTS_LIST = {
    'projects': [{
        "id": "15c578ea47a5466db2aeb57dc8443676",
        "name": "pr1",
        "url": "http://11111.selvpc.ru",
        "enabled": True,
        "theme": {
            "color": "",
            "logo": "",
            "brand_color": "",
        }
    }, {
        "id": "2c578ea47a5466db2aeb57dc8443676",
        "name": "pr2",
        "url": "http://11111.selvpc.ru",
        "enabled": True,
        "theme": {
            "color": "",
            "logo": "",
            "brand_color": "",
        }
    }]
}

PROJECTS_CREATE = {
    'project': {
        "id": "15c578ea47a5466db2aeb57dc8443676",
        "name": "project1",
        "url": "http://11111.selvpc.ru",
        "enabled": True,
        "custom_url": "",
        "theme": {
            "color": "",
            "logo": "",
            "brand_color": "",
        }
    }
}

PROJECTS_SET = {
    'project': {
        "id": "15c578ea47a5466db2aeb57dc8443676",
        "name": "project1",
        "url": "http://11111.selvpc.ru",
        "enabled": True,
        "custom_url": "www.customhost.no",
        "theme": {
            "color": "",
            "logo": "",
            "brand_color": "",
        }
    }
}

PROJECTS_SET_WITHOUT_CNAME = PROJECTS_CREATE

PROJECTS_SHOW = {
    'project': {
        "id": "f5c578ea47a5466db2aeb57dc8443676",
        "name": "pr1",
        "url": "http://11111.selvpc.ru",
        "enabled": True,
        "quotas": {
            "compute_cores": [
                {
                    "region": "ru-1",
                    "zone": "ru-1a",
                    "value": 10,
                    "used": 1
                },
                {
                    "region": "ru-1",
                    "zone": "ru-1b",
                    "value": 10,
                    "used": 0
                }
            ],
            "compute_ram": [
                {
                    "region": "ru-1",
                    "zone": "ru-1a",
                    "value": 1024,
                    "used": 512
                },
                {
                    "region": "ru-1",
                    "zone": "ru-1b",
                    "value": 2048,
                    "used": 0
                }
            ]
        },
        "theme": {
            "color": "",
            "logo": "",
            "brand_color": "",
        }
    }
}

PROJECTS_SHOW_ROLES = {
    'roles': [{
        "project_id": "1_7354286c9ebf464d86efc16fb56d4fa3",
        "user_id": "5900efc62db34decae9f2dbc04a8ce0f"
    }, {
        "project_id": "2_7354286c9ebf464d86efc16fb56d4fa3",
        "user_id": "5900efc62db34decae9f2dbc04a8ce0f"
    }]
}

PROJECT_CUSTOMIZE = {
    'theme': {
        "color": "00ffee",
        "logo": LOGO_BASE64,
        "brand_color": "00ffee",
    }
}

CUSTOMIZATION_CREATE = PROJECT_CUSTOMIZE

CUSTOMIZATION_SHOW = PROJECT_CUSTOMIZE

CUSTOMIZATION_UPDATE = {
    'theme': {
        "color": "00eeff",
        "logo": LOGO_BASE64,
        "brand_color": "00ffee",
    }
}

CUSTOMIZATION_NO_THEME = {
    "theme": {"color": "", "logo": "", "brand_color": ""}
}

LIMITS_SHOW = {
    'quotas': {
        "compute_cores": [
            {
                "zone": "ru-1a",
                "value": 10
            },
        ],
        "compute_ram": [
            {
                "zone": "ru-1a",
                "value": 1024
            },
            {
                "zone": "ru-1b",
                "value": 2048
            }
        ],
        "volume_gigabytes_fast": [
            {
                "zone": "ru-1a",
                "value": 100
            },
            {
                "zone": "ru-1b",
                "value": 100
            }
        ],
        "volume_gigabytes_universal": [
            {
                "zone": "ru-1a",
                "value": 100
            },
            {
                "zone": "ru-1b",
                "value": 100
            }
        ],
        "volume_gigabytes_basic": [
            {
                "zone": "ru-1a",
                "value": 100
            },
            {
                "zone": "ru-1b",
                "value": 100
            }
        ],
        "image_gigabytes": [
            {
                "zone": None,
                "value": 10
            },
        ],
        "network_floatingips": [
            {
                "zone": None,
                "value": 5
            }
        ],
        "network_subnets_29": [
            {
                "zone": None,
                "value": 1
            }
        ],
        "license_windows_2012_standard": [
            {
                "zone": None,
                "value": 1
            }
        ]
    }
}

QUOTAS_SET = {
    "quotas": {
        "volume_gigabytes_basic": [
            {
                "zone": "ru-1b",
                "value": 0
            },
            {
                "zone": "ru-1a",
                "value": 0
            },
            {
                "zone": "ru-2a",
                "value": 0
            }
        ],
        "compute_cores": [
            {
                "zone": "ru-1b",
                "value": 1
            },
            {
                "zone": "ru-1a",
                "value": 2
            },
            {
                "zone": "ru-2a",
                "value": 1
            }
        ],
        "volume_gigabytes_universal": [
            {
                "zone": "ru-1b",
                "value": 0
            },
            {
                "zone": "ru-1a",
                "value": 0
            },
        ],
        "compute_ram": [
            {
                "zone": "ru-1b",
                "value": 512
            },
            {
                "zone": "ru-1a",
                "value": 1536
            },
        ],
        "volume_gigabytes_fast": [
            {
                "zone": "ru-1b",
                "value": 5
            },
            {
                "zone": "ru-1a",
                "value": 20
            },
        ],
        "image_gigabytes": [
            {
                "zone": None,
                "value": 0
            },
            {
                "zone": None,
                "value": 0
            }
        ]
    }
}

QUOTAS_SHOW = {
    'quotas': {
        "compute_cores": [
            {
                "zone": "ru-1a",
                "value": 10,
                "used": 0
            },
            {
                "zone": "ru-1b",
                "value": 10,
                "used": 0
            }
        ],
        "compute_ram": [
            {
                "zone": "ru-1a",
                "value": 1024,
                "used": 0
            },
            {
                "zone": "ru-1b",
                "value": 2048,
                "used": 0
            }
        ],
        "volume_gigabytes_fast": [
            {
                "zone": "ru-1a",
                "value": 100,
                "used": 0
            },
            {
                "zone": "ru-1b",
                "value": 100,
                "used": 0
            }
        ],
        "network_subnets_29_vrrp": [
            {
                "used": 0,
                "value": 0,
                "zone": None
            }
        ],
    }
}

USERS_LIST = {
    'users': [{
        "id": "f9fd1d3167ba4641a3190b4848382216",
        "name": "user1",
        "enabled": True
    }, {
        "id": "1d3161d317ba4641a3190b4848382216",
        "name": "user2",
        "enabled": True
    }]
}

USERS_CREATE = {
    'user': {
        "id": "f9fd1d3167ba4641a3190b4848382216",
        "name": "user",
        "enabled": True
    }
}

USERS_ROLE_SHOW = {
    'roles': [{
        "project_id": "1_7354286c9ebf464d86efc16fb56d4fa3",
        "user_id": "5900efc62db34decae9f2dbc04a8ce0f"
    }, {
        "project_id": "1_7354286c9ebf464d86efc16fb56d4fa3",
        "user_id": "5900efc62db34decae9f2dbc04a8ce0f"
    }]
}

USERS_EMPTY = {
  "field": "user_id",
  "error": "invalid_id"
}

USERS_SET = USERS_CREATE

USERS_SHOW = USERS_CREATE

TOKENS_CREATE = {
    'token': {
        'id': "a9a81014462d499d9d55d3402991f224"
    }
}

LICENSES_LIST = {
    'licenses': [{
        "id": 0,
        "region": "ru-1",
        "type": "license_windows_2012_standard",
        "project_id": "e7081cb46966421fb8b3f3fd9b4db75b",
        "servers": [
            {
                "id": "177b0416-2830-4557-898a-581c1147f0ff",
                "updated": "2016-01-01T00:00:00Z",
                "status": "PAUSED",
                "name": "s1"
            }
        ],
        "status": "ACTIVE"
    }, {
        "id": 1,
        "region": "ru-2",
        "type": "license_windows_2012_standard",
        "project_id": "xxxx1cb46966421fb8b3f3fd9b4db75b",
        "servers": [
            {
                "id": "177b0416-2830-4557-898a-581c1147f0ff",
                "updated": "2016-01-01T00:00:00Z",
                "status": "PAUSED",
                "name": "s1"
            }
        ],
        "status": "ACTIVE"
    }]
}

LICENSES_SHOW = {
    "license": {
        "id": 420,
        "region": "ru-1",
        "type": "license_windows_2012_standard",
        "project_id": "e7081cb46966421fb8b3f3fd9b4db75b",
        "servers": [
            {
                "id": "177b0416-2830-4557-898a-581c1147f0ff",
                "updated": "2016-01-01T00:00:00Z",
                "status": "PAUSED",
                "name": "s1"
            }
        ],
        "status": "ACTIVE"
    }
}

LICENSES_CREATE = {
    'licenses': [{
        "id": 1,
        "region": "ru-1",
        "type": "license_windows_2012_standard",
        "project_id": "e7081cb46966421fb8b3f3fd9b4db75b",
        "servers": [
            {
                "id": "177b0416-2830-4557-898a-581c1147f0ff",
                "updated": "2016-01-01T00:00:00Z",
                "status": "PAUSED",
                "name": "s1"
            }
        ],
        "status": "ACTIVE"
    }, {
        "id": 2,
        "region": "ru-2",
        "type": "license_windows_2012_standard",
        "project_id": "e7081cb46966421fb8b3f3fd9b4db75b",
        "servers": [
            {
                "id": "177b0416-2830-4557-898a-581c1147f0ff",
                "updated": "2016-01-01T00:00:00Z",
                "status": "PAUSED",
                "name": "s1"
            }
        ],
        "status": "ACTIVE"
    }]
}

ROLES_LIST = {
    'roles': [{
        "project_id": "1_7354286c9ebf464d86efc16fb56d4fa3",
        "user_id": "1900efc62db34decae9f2dbc04a8ce0f"
    }, {
        "project_id": "1_7354286c9ebf464d86efc16fb56d4fa3",
        "user_id": "5900efc62db34decae9f2dbc04a8ce0f"
    }]
}

ROLES_ADD = {
    'role': {
        "project_id": "1_7354286c9ebf464d86efc16fb56d4fa3",
        "user_id": "5900efc62db34decae9f2dbc04a8ce0f"
    }
}

FLOATINGIP_LIST = {
    "floatingips": [
        {
            "status": "ACTIVE",
            "tenant_id": "a2e6dd715ca24681b9b335d247b83d16",
            "servers": [
                {
                    "status": "ACTIVE",
                    "updated": "2016-01-01T00:00:00Z",
                    "id": "dc113178-b573-4459-bdde-272ec18140f3",
                    "name": "Raya"
                }
            ],
            "fixed_ip_address": "192.168.0.4",
            "floating_ip_address": "12.34.56.78",
            "project_id": "a2e6dd715ca24681b9b335d247b83d16",
            "port_id": "dc801110-94f2-4fdd-b71a-74e2d3d8bfd0",
            "id": "0d987b46-bad5-41b7-97e3-bac9974aa97a",
            "region": "ru-1"
        },
        {
            "status": "ACTIVE",
            "tenant_id": "xxxxdd715ca24681b9b335d247b83d16",
            "servers": [
                {
                    "status": "ACTIVE",
                    "updated": "2016-01-01T00:00:00Z",
                    "id": "dc113178-b573-4459-bdde-272ec18140f3",
                    "name": "Raya"
                }
            ],
            "fixed_ip_address": "192.168.0.4",
            "floating_ip_address": "12.34.56.78",
            "project_id": "xxxxdd715ca24681b9b335d247b83d16",
            "port_id": "dc801110-94f2-4fdd-b71a-74e2d3d8bfd0",
            "id": "0d987b46-bad5-41b7-97e3-bac9974aa97a",
            "region": "ru-2"
        }
    ]
}

FLOATINGIP_ADD = {
    "floatingips": [
        {
            "status": "ACTIVE",
            "tenant_id": "a2e6dd715ca24681b9b335d247b83d16",
            "servers": [
                {
                    "status": "ACTIVE",
                    "updated": "2016-01-01T00:00:00Z",
                    "id": "dc113178-b573-4459-bdde-272ec18140f3",
                    "name": "Raya"
                }
            ],
            "fixed_ip_address": "192.168.0.4",
            "floating_ip_address": "12.34.56.78",
            "project_id": "a2e6dd715ca24681b9b335d247b83d16",
            "port_id": "dc801110-94f2-4fdd-b71a-74e2d3d8bfd0",
            "id": "0d987b46-bad5-41b7-97e3-bac9974aa97a",
            "region": "ru-1"
        }
    ]
}

FLOATINGIP_SHOW = {
    "floatingip": {
        "status": "ACTIVE",
        "servers": [
            {
                "status": "ACTIVE",
                "updated": "2016-01-01T00:00:00Z",
                "id": "dc113178-b573-4459-bdde-272ec18140f3",
                "name": "Raya"
            }
        ],
        "floating_ip_address": "12.34.56.78",
        "project_id": "a2e6dd715ca24681b9b335d247b83d16",
        "id": "0d987b46-bad5-41b7-97e3-bac9974aa97a",
        "region": "ru-1"
    }
}

SUBNET_LIST = {
    "subnets": [
        {
            "id": 20,
            "region": "ru-1",
            "cidr": "192.168.5.32/29",
            "enabled": True,
            "network_id": "70e73ef1-bade-4377-a52c-4a8cff843170",
            "project_id": "e7081cb46966421fb8b3f3fd9b4db75b",
            "status": "ACTIVE",
            "subnet_id": "61053c51-93f4-4d64-9a94-d4f88d1ee88f",
            "servers": [
                {
                    "id": "177b0416-2830-4557-898a-581c1147f0ff",
                    "updated": "2016-01-01T00:00:00Z",
                    "status": "PAUSED",
                    "name": "s1"
                }
            ]
        }, {
            "id": 21,
            "region": "ru-2",
            "cidr": "192.168.5.32/29",
            "enabled": True,
            "network_id": "70e73ef1-bade-4377-a52c-4a8cff843170",
            "project_id": "xxxxcb46966421fb8b3f3fd9b4db75b",
            "status": "ACTIVE",
            "subnet_id": "61053c51-93f4-4d64-9a94-d4f88d1ee88f",
            "servers": [
                {
                    "id": "177b0416-2830-4557-898a-581c1147f0ff",
                    "updated": "2016-01-01T00:00:00Z",
                    "status": "PAUSED",
                    "name": "s1"
                }
            ]
        }
    ]
}

SUBNET_ADD = {
    "subnets": [
        {
            "id": 20,
            "region": "ru-1",
            "cidr": "192.168.5.32/29",
            "enabled": True,
            "network_id": "70e73ef1-bade-4377-a52c-4a8cff843170",
            "project_id": "e7081cb46966421fb8b3f3fd9b4db75b",
            "status": "ACTIVE",
            "subnet_id": "61053c51-93f4-4d64-9a94-d4f88d1ee88f",
            "servers": [
                {
                    "id": "177b0416-2830-4557-898a-581c1147f0ff",
                    "updated": "2016-01-01T00:00:00Z",
                    "status": "PAUSED",
                    "name": "s1"
                }
            ]
        }, {
            "id": 21,
            "region": "ru-1",
            "cidr": "192.168.5.32/29",
            "enabled": True,
            "network_id": "70e73ef1-bade-4377-a52c-4a8cff843170",
            "project_id": "e7081cb46966421fb8b3f3fd9b4db75b",
            "status": "ACTIVE",
            "subnet_id": "61053c51-93f4-4d64-9a94-d4f88d1ee88f",
            "servers": [
                {
                    "id": "177b0416-2830-4557-898a-581c1147f0ff",
                    "updated": "2016-01-01T00:00:00Z",
                    "status": "PAUSED",
                    "name": "s1"
                }
            ]
        }
    ]
}

SUBNET_SHOW = {
    "subnet": {
        "status": "ACTIVE",
        "subnet_id": "6145fba6-dbe2-47af-bad2-6d1dcese5996",
        "region": "ru1",
        "servers": [
            {
                "id": "177b0416-2830-4557-898a-581c1147f0ff",
                "updated": "2016-01-01T00:00:00Z",
                "status": "PAUSED",
                "name": "s1"
            }
        ],
        "network_id": "47e4a3e8-a2c0-400c-a20c-2b3bf2f8b681",
        "cidr": "192.168.5.0/29",
        "project_id": "7810f45ae1be4a1f8ab3e95aef2e3ddd",
        "id": 420,
    }
}

CAPABILITIES_LIST = {
    "capabilities": {
        "licenses": [
            {
                "availability": [
                    "ru-1",
                    "ru-2"
                ],
                "type": "license_windows_2012_standard"
            }
        ],
        "regions": [
            {
                "description": "Moscow",
                "is_default": True,
                "name": "ru-2",
                "zones": [
                    {
                        "description": "Berzarina-1 (ru-2a)",
                        "enabled": True,
                        "is_default": True,
                        "is_private": False,
                        "name": "ru-2a"
                    }
                ]
            },
            {
                "description": "Saint Petersburg",
                "is_default": False,
                "name": "ru-1",
                "zones": [
                    {
                        "description": "Dubrovka-1 (ru-1a)",
                        "enabled": True,
                        "is_default": False,
                        "is_private": False,
                        "name": "ru-1a"
                    },
                    {
                        "description": "Dubrovka-2 (ru-1b)",
                        "enabled": True,
                        "is_default": True,
                        "is_private": False,
                        "name": "ru-1b"
                    }
                ]
            }
        ],
        "resources": [
            {
                "name": "network_floatingips",
                "quota_scope": None,
                "quotable": False,
                "unbillable": False,
            },
            {
                "name": "volume_gigabytes_universal",
                "quota_scope": "zone",
                "quotable": True,
                "unbillable": True,
            },
            {
                "name": "volume_gigabytes_basic",
                "quota_scope": "zone",
                "quotable": True,
                "unbillable": False,
            },
            {
                "name": "compute_ram",
                "quota_scope": "zone",
                "quotable": True,
                "unbillable": False,
            },
            {
                "name": "volume_gigabytes_fast",
                "quota_scope": "zone",
                "quotable": True,
                "unbillable": False,
            },
            {
                "name": "license_windows_2012_standard",
                "quota_scope": None,
                "quotable": False,
                "unbillable": False,
            },
            {
                "name": "image_gigabytes",
                "quota_scope": "region",
                "quotable": True,
                "unbillable": False,
            },
            {
                "name": "network_subnets_29",
                "quota_scope": None,
                "quotable": False,
                "unbillable": False,
            },
            {
                "name": "compute_cores",
                "quota_scope": "zone",
                "quotable": True,
                "unbillable": False,
            },
            {
                "name": "network_subnets_25",
                "quota_scope": None,
                "quotable": False,
                "unbillable": True,
            }
        ],
        "subnets": [
            {
                "availability": [
                    "ru-1",
                    "ru-2"
                ],
                "prefix_length": "29",
                "type": "ipv4"
            }
        ],
        "traffic": {
            "granularities": [
                {
                    "granularity": 3600,
                    "timespan": 96
                },
                {
                    "granularity": 1,
                    "timespan": 32
                },
                {
                    "granularity": 86400,
                    "timespan": 1825
                }
            ]
        }
    }
}

VRRP_ADD = {
    "vrrp_subnets":
        [{
            "status": "DOWN",
            "cidr": "78.155.195.8/29",
            "project_id": "b63ab68796e34858befb8fa2a8b1e12a",
            "id": 6,
            "subnets": [
                {
                    "network_id": "827fe85f-a379-4f28-a426-2ddf7ddab6a2",
                    "subnet_id": "6595e66c-b14e-4167-9a48-6be6fb407c63",
                    "region": "ru-1"
                },
                {
                    "network_id": "68b6a3e0-d016-4248-b8de-03cb20cacb2c",
                    "subnet_id": "9e8cf4bb-a385-401d-bda4-395f3985ead1",
                    "region": "ru-2"
                }
            ],
        }]
}

VRRP_SHOW = {
    "vrrp_subnet": {
        "status": "DOWN",
        "subnets": [
            {
                "network_id": "1eb0e13d-0ce6-4c00-99e8-45e4787766fd",
                "subnet_id": "053f7817-6804-4fad-8f6b-0d1edef074ed",
                "region": "ru-1"
            },
            {
                "network_id": "74694b81-4203-4599-ae71-029182f9cef9",
                "subnet_id": "cc1d50b9-4890-4173-a750-4537c1f747a2",
                "region": "ru-2"
            }
        ],
        "servers": [],
        "cidr": "78.155.195.0/29",
        "project_id": "b63ab68796e34858befb8fa2a8b1e12a",
        "id": 2,
        "master_region": "ru-1",
        "slave_region": "ru-2"
    }
}

VRRP_LIST = {
    "vrrp_subnets": [
        {
            "status": "DOWN",
            "subnets": [],
            "servers": [],
            "cidr": "78.155.196.0/29",
            "project_id": "x63ab68796e34858befb8fa2a8b1e12a",
            "id": 3,
            "master_region": "ru-1",
            "slave_region": "ru-2"
        },
        {
            "status": "DOWN",
            "subnets": [],
            "servers": [],
            "cidr": "78.155.195.0/29",
            "project_id": "b63ab68796e34858befb8fa2a8b1e12a",
            "id": 2,
            "master_region": "ru-1",
            "slave_region": "ru-2"
        }
    ]
}

QUOTAS_PARTIAL = {
    "quotas": {
        "compute_ram": [
            {
                "zone": "ru-1b",
                "value": 2048
            }
        ],
    },
    "error": {
        "message": "Multi-Status",
        "code": 207,
        "errors": [
            {
                "resource": "image_gigabytes",
                "zone": "ru-1a",
                "message": "Internal Server Error",
                "code": 500
            }
        ]
    }
}

FLOATING_IPS_PARTIAL = {
    "floatingips": {
        "fail": [
            {
                "region": "ru-2",
                "quantity": 1
            }
        ],
        "ok": [
            {
                "status": "DOWN",
                "floating_ip_address": "12.34.56.77",
                "project_id": "a2e6dd715ca24681b9b335d247b83d16",
                "id": "0d987b46-bad5-41b7-97e3-bac9974aa97a",
                "region": "ru-1"
            },
            {
                "status": "DOWN",
                "floating_ip_address": "12.34.56.78",
                "project_id": "a2e6dd715ca24681b9b335d247b83d16",
                "id": "0d987b46-bad5-41b7-97e3-bac9974aa97b",
                "region": "ru-1"
            }
        ],
        "error": "multi_status"
    }
}

FLOATING_IPS_PARTIAL_RESULT = [
    {
        "status": "DOWN",
        "floating_ip_address": "12.34.56.77",
        "project_id": "a2e6dd715ca24681b9b335d247b83d16",
        "id": "0d987b46-bad5-41b7-97e3-bac9974aa97a",
        "region": "ru-1"
    },
    {
        "status": "DOWN",
        "floating_ip_address": "12.34.56.78",
        "project_id": "a2e6dd715ca24681b9b335d247b83d16",
        "id": "0d987b46-bad5-41b7-97e3-bac9974aa97b",
        "region": "ru-1"
    }
]

LICENSES_PARTIAL = {
    'licenses':
        {
            "fail": [
                {
                    "quantity": 1,
                    "region": "ru-2",
                    "type": "license_windows_2012_standard"
                }
            ],
            "ok": [
                {
                    "id": 1,
                    "region": "ru-1",
                    "type": "license_windows_2012_standard",
                    "project_id": "e7081cb46966421fb8b3f3fd9b4db75b",
                    "status": "DOWN"
                }
            ],
            "error": "multi_status"
        }
}

LICENSES_PARTIAL_RESULT = [
    {
        "id": 1,
        "region": "ru-1",
        "type": "license_windows_2012_standard",
        "project_id": "e7081cb46966421fb8b3f3fd9b4db75b",
        "status": "DOWN"
    }
]

ROLES_PARTIAL = {
    'roles': {
        "fail": [{
            "project_id": "1_7354286c9ebf464d86efc16fb56d4fa3",
            "user_id": "1900efc62db34decae9f2dbc04a8ce0f"

        }],
        "ok": [
            {
                "project_id": "1_7354286c9ebf464d86efc16fb56d4fa3",
                "user_id": "5900efc62db34decae9f2dbc04a8ce0f"
            }
        ],
        "error": "multi_status"
    }
}

ROLES_PARTIAL_RESULT = [
    {
        "project_id": "1_7354286c9ebf464d86efc16fb56d4fa3",
        "user_id": "5900efc62db34decae9f2dbc04a8ce0f"
    }
]

SUBNETS_PARTIAL = {
    "subnets": {
        "fail": [
            {
                "region": "ru-2",
                "prefix_length": 29,
                "quantity": 1,
                "type": "ipv4"
            }
        ],
        "ok": [
            {
                "status": "DOWN",
                "subnet_id": "6145fba6-dbe2-47af-bad2-6d1dcese5996",
                "region": "ru-1",
                "network_id": "47e4a3e8-a2c0-400c-a20c-2b3bf2f8b681",
                "cidr": "192.168.5.0/29",
                "project_id": "7810f45ae1be4a1f8ab3e95aef2e3ddd",
                "id": 420
            }
        ],
        "error": "multi_status"
    }
}

SUBNETS_PARTIAL_RESULT = [
    {
        "status": "DOWN",
        "subnet_id": "6145fba6-dbe2-47af-bad2-6d1dcese5996",
        "region": "ru-1",
        "network_id": "47e4a3e8-a2c0-400c-a20c-2b3bf2f8b681",
        "cidr": "192.168.5.0/29",
        "project_id": "7810f45ae1be4a1f8ab3e95aef2e3ddd",
        "id": 420
    }
]

KEYPAIR_LIST = {
    "keypairs": [
        {
            "name": "User_1",
            "public_key": "ssh-rsa ... user@name",
            "regions": [
                "ru-1"
            ],
            "user_id": "88ad5569d8c64f828ac3d2efa4e552dd"
        },
        {
            "name": "User_2",
            "public_key": "ssh-rsa ... user@name",
            "regions": [
                "ru-2"
            ],
            "user_id": "88ad5569d8c64f828ac3d2efa4e552dd"
        }
    ]
}

KEYPAIR_ADD = {
    "keypair": [
        {
            "name": "MOSCOW_KEY",
            "region": "ru-1",
            "user_id": "88ad5569d8c64f828ac3d2efa4e552dd"
        },
        {
            "name": "MOSCOW_KEY",
            "region": "ru-2",
            "user_id": "88ad5569d8c64f828ac3d2efa4e552dd"
        }
    ]
}
