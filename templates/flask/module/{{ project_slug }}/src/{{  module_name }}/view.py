# Views for {{ module_name }} module
from .model import {{ module_camel_case }}


def {{ module_name }}_view(model: {{ module_camel_case }}):
    return {
        "id": model.id
    }

