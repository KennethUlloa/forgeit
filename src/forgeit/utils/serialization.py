import importlib
import json
import pickle
from functools import lru_cache

types = {
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
    "dict": dict,
    "list": list,
    "tuple": tuple,
    "set": set
}


@lru_cache()
def _load_module(module_path: str):
    print("Importing module", module_path)
    return importlib.import_module(module_path)

@lru_cache()
def get_symbol(name: str):
    parts = name.split(".")
    symbol_name = parts[-1]
    print("Importing symbol", symbol_name)
    if symbol_name in types:
        return types[symbol_name]
    
    module_path = ".".join(parts[:-1])
    module = _load_module(module_path)
    return getattr(module, symbol_name)

def parse_data(data):
    """
    Parses object notation dictionaries to their equivalent classes/types
    """
    if isinstance(data, dict):
        if len(data) == 1:
            name = list(data.keys())[0]
            if name.startswith("$"):
                type_ = get_symbol(name.removeprefix("$"))
                value = parse_data(data[name])
                return type_(**value) if isinstance(value, dict) \
                    else type_(*value) if isinstance(value, (list)) \
                        else type_
        return {k: parse_data(v) for k, v in data.items()}
    if isinstance(data, list):
        return [parse_data(v) for v in data]
    return data


def save_binary(obj, filename: str):
    with open(filename, "wb") as f:
        pickle.dump(obj, f)


def load_binary(filename):
    with open(filename, "rb") as f:
        return pickle.load(f, encoding="utf-8")


def load_json(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        return parse_data(json.load(f))