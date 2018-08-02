from selvpcclient.util import sort_list_of_dicts


def format_servers(val):
    return "\n".join([s["id"] for s in val["servers"]])


def join_by_key(key):
    def formatter(val):
        return "\n".join(val[key])

    return formatter


def reformat_quotas(quotas):
    result = []
    for resource, quota in quotas.items():
        quota = sort_list_of_dicts(quota, "region")
        result.append({
            "resource": resource,
            "region": [q["region"] for q in quota],
            "zone": [q["zone"] or str() for q in quota],
            "value": [str(q["value"]) for q in quota]
        })
    return result


def reformat_quotas_with_usages(val):
    result = []
    for project, quotas in val.items():
        for resource, quota in quotas.items():
            quota = sort_list_of_dicts(quota, "zone")
            result.append({
                "project_id": project,
                "resource": resource,
                "region": [q["region"] for q in quota],
                "zone": [q["zone"] or str() for q in quota],
                "value": [str(q["value"]) for q in quota],
                "used": [str(q["used"]) for q in quota],
            })
    return result
