# ForgeIt
Templated based, configurable project generator CLI tool.

## Prerequisites
Set up `FORGE_CONFIG_PATH` environment variable. It must target to the configuration JSON file.

### Configuration file example
```json
{
    "path": "Path where templates are located, if not present this file path is used. Ex: templates",
    "templates": [
        {
            "name": "template name",
            "description": "Description for the template",
            "src": "path to the folder containing the template file structure relative to this file ex: (templates/data)",
            "variables": {
                "variable_name_1": "type, ex(str)",
                "variable_name_2": "str"
            },
            "exclude": [
                "file matching pattern to exclue from rendering",
                "test_**.py",
                "test/**.py"
            ],
            "processors": {
                "processed_var_name": {
                    "var": "variable_name_1",
                    "name": "processor name, ex: camel -> Camel case proccesor"
                },
                "proccessed_var_name2": {
                    "var": "variable_name_2",
                    "name": "camel"
                }
            }
        }
    ]
}
```
### Templates folder structure
```
|--templates
|  |--api # Template structure (ex: REST API)
|  |  |--src
|  |  |  |--app.py
|  |  |  |--config.py
|  |  |  |--models.py
|  |  |  |--routes.py
|  |  |  |--controllers.py
|  |--cli # ex: CLI app
|  |  |--src
|  |  |  |--cli.py
|  |  |  |--app.py
|  |--forge.json # template configuration file
```
### Installation
1. Clone this repository
```shell
git clone <this repo>
```
2. Activate a virtual environment *(optional)*
```shell
# Unix
python3 -m venv venv
cd venv
source venv/bin/activate
```
```shell
# Windows
python -m venv venv
venv/Scripts/activate
```
3. Install the package `build`
```shell
pip install build
python -m build
```

4. Install the built package `forgeit`
```shell
pip install dist/<generated package>.tar.gz
# or
pip install dist/<generated package>.whl
```
### Variable types
When you define the variables for a template, you must declare their types in order to the tool to parse it.
- `str` for strings
- `list` for lists (each element will be parsed as string)
- `float` for float point numbers
- `int` for integers
- `bool` for booleans