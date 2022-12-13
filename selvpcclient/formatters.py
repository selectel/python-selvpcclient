from selvpcclient.util import sort_list_of_dicts


def format_servers(val):
    return "\n".join([s["id"] for s in val["servers"]])


def join_by_key(key):
    def formatter(val):
        for index in range(len(val[key])):
            if val[key][index] is None:
                val[key][index] = ""
        return "\n".join(val[key])

    return formatter


def reformat_limits(quotas):
    result = []
    for resource, quota in quotas.items():
        if quota[0].get("zone"):
            quota = sort_list_of_dicts(quota, "zone")
        result.append({
            "resource": resource,
            "value": [str(q["value"]) for q in quota],
            "zone": [q["zone"] if q.get("zone") else str() for q in quota]
        })
    return result


def reformat_quotas(quotas):
    result = []
    for resource, quota in quotas.items():
        quota = sort_list_of_dicts(quota, "zone")
        result.append({
            "resource": resource,
            "zone": [q["zone"] or str() for q in quota],
            "value": [str(q["value"]) for q in quota],
        })
    return result


def reformat_quotas_with_usages(quotas):
    result = []
    for resource, quota in quotas.items():
        quota = sort_list_of_dicts(quota, "zone")
        result.append({
            "resource": resource,
            "zone": [q["zone"] or str() for q in quota],
            "value": [str(q["value"]) for q in quota],
            "used": [str(q["used"]) for q in quota],
        })
    return result
