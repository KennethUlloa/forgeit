import jsonschema


template_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Template Definition Schema",
    "type": "object",
    "required": ["name", "label", "variables", "content"],
    "properties": {
        "name": {"type": "string"},
        "label": {"type": "string"},
        "description": {"type": "string"},
        "variables": {
            "type": "object",
            "additionalProperties": {"$ref": "#/definitions/variable"},
        },
        "content": {"type": "object", "patternProperties": {".+": {"type": "string"}}},
        "subtemplates": {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "required": ["label", "variables", "content"],
                "properties": {
                    "label": {"type": "string"},
                    "description": {"type": "string"},
                    "variables": {
                        "type": "object",
                        "additionalProperties": {"$ref": "#/definitions/variable"},
                    },
                    "content": {
                        "type": "object",
                        "patternProperties": {".+": {"type": "string"}},
                    },
                },
            },
        },
    },
    "definitions": {
        "baseVariable": {
            "type": "object",
            "required": ["type", "label"],
            "properties": {
                "type": {"type": "string"},
                "label": {"type": "string"},
                "default": {},
            },
        },
        "stringVariable": {
            "allOf": [
                {"$ref": "#/definitions/baseVariable"},
                {
                    "properties": {
                        "type": {"const": "string"},
                        "min_length": {"type": "integer"},
                        "max_length": {"type": "integer"},
                        "regex": {"type": "string"},
                        "password": {"type": "boolean"},
                        "choices": {"type": "array", "items": {"type": "string"}},
                    }
                },
            ]
        },
        "integerVariable": {
            "allOf": [
                {"$ref": "#/definitions/baseVariable"},
                {
                    "properties": {
                        "type": {"const": "integer"},
                        "min_value": {"type": "integer"},
                        "max_value": {"type": "integer"},
                    }
                },
            ]
        },
        "floatVariable": {
            "allOf": [
                {"$ref": "#/definitions/baseVariable"},
                {
                    "properties": {
                        "type": {"const": "float"},
                        "min_value": {"type": "number"},
                        "max_value": {"type": "number"},
                    }
                },
            ]
        },
        "booleanVariable": {
            "allOf": [
                {"$ref": "#/definitions/baseVariable"},
                {"properties": {"type": {"const": "boolean"}}},
            ]
        },
        "objectVariable": {
            "allOf": [
                {"$ref": "#/definitions/baseVariable"},
                {
                    "required": ["props"],
                    "properties": {
                        "type": {"const": "object"},
                        "props": {
                            "type": "object",
                            "additionalProperties": {"$ref": "#/definitions/variable"},
                        },
                    },
                },
            ]
        },
        "listVariable": {
            "allOf": [
                {"$ref": "#/definitions/baseVariable"},
                {
                    "required": ["item_attributes"],
                    "properties": {
                        "type": {"const": "list"},
                        "item_attributes": {"$ref": "#/definitions/variable"},
                        "size": {"type": "integer"},
                        "continue_prompt": {"type": "string"},
                        "continue_default": {"type": "boolean"},
                    },
                },
            ]
        },
        "variable": {
            "oneOf": [
                {"$ref": "#/definitions/stringVariable"},
                {"$ref": "#/definitions/integerVariable"},
                {"$ref": "#/definitions/floatVariable"},
                {"$ref": "#/definitions/booleanVariable"},
                {"$ref": "#/definitions/objectVariable"},
                {"$ref": "#/definitions/listVariable"},
            ]
        },
    },
}


def validate_template(template_data: dict):
    jsonschema.validate(template_data, template_schema)
