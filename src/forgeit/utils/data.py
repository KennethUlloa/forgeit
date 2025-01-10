def read(key_path: str):
    def resolve(data: dict):
        val = data.copy()
        for fragment in key_path.strip(".").split("."):
            val = val[fragment]
        return val
    return resolve

def clone(d):
    new = {}
    for k, v in d.items():
        new[k] = clone(v) if isinstance(v, dict) else v
    return new

def save(key_path: str, value):
    def resolve(data: dict):
        keys = key_path.strip(".").split(".")
        current_dict = data
        for key in keys[:-1]:
            current_dict = current_dict.setdefault(key, {})
        current_dict[keys[-1]] = value
        return data
    return resolve