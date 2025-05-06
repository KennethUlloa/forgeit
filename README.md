<p align="center">
  <img src="https://kennethulloa.github.io/forgeit-assets/forgeit.png" width="120px">
</p>

# ForgeIt
Scaffolding library written in Python. Jinja2 is used for template rendering and Typer for CLI.

## Installation
In a terminal run

```shell
# Windows
pip install forgeit
# MacOS/Linux
pip3 install forgeit
```

If you prefer, you could build the tool locally.
  1. Clone this repository
  2. Go to the project folder with `cd forgeit/`
  3. Activate a virtual environment (recommended)
      
      ```shell
      # Windows
      python -m venv .venv
      .venv/Scripts/activate
      # MacOS/Linux
      python3 -m venv .venv
      source .venv/bin/activate
      ```
    
  4. Install `build` package

      ```shell
      # Windows
      pip install build
      # MacOS/Linux
      pip3 install build
      ```

  5. Build the project
      ```shell
      # Windows
      python -m build
      # MacOS/Linux
      python3 -m build
      ```
  
  6. Deactivate the virtual environment (optional, perform this step if you want global installation).
  
  7. Install `forgeit`

      ```shell
      # Windows
      pip install dist/<tar or whl>
      # MacOS/Linux
      pip3 install dist/<tar or whl>
      ```

### First steps

After the installation you will have no templates. In order to start using it you should install the example template to explore the tool's functionalities.

```shell
forgeit example
forgeit install example.zip
forget init flask-api
```
The tool will ask you to enter some values and then a simple API project using Flask, SQLAlchemy and Marshmallow will be created. 

Run `flask run` in the project directory. You should see the project starting. By default CRUD operations will be available at `/api/users` including a simple login.

To extend the application run `forgeit new entity`. You will be prompted to enter the structure for the new entity and then all the scaffold will be created.

In the method `register_controller` in the `app.py` file, include the controller for your entity like this `from controllers.<entity_name> import <entity_name>_controller` and pass it to the array of controllers `[user_controller, <entity_name>_controller]`.



## CLI Documentation

It provides the following commands:

### `init`

Render a template's files given a name. If no variables file is given, the user will be prompted to enter them manually.

* Usage: `forgeit init <name> [<file>]`

### `new`

Renders a template's fragment (subtemplate) using stored context `.forge.json` file. If no variables file is given, the user will be prompted to enter the manually.

* Usage: `forgeit new <name> [<file>]`

### `install`

Installs a template description from a file path. It can be a zip file or a directory path.

The provided ZIP/folder path file must have the following structure:
```
templates/
  # Files with jinja syntax
files/
  # Files that will be cloned
template.json # Template schema/definition
```

* Usage: `forgeit install <path>`

### `list`

Lists all the available templates.

* Usage: `forgeit list`


### `version`

Displays the current version of the tool.

* Usage: `forgeit version`

### `validate`

Validate a template description. It must be a JSON file.

* Usage: `forgeit validate <file>`

### `example`

Create an example template. It will create a ZIP file containing a basic layout of a 
valid template in the current working directory. You could install it to use it if you want.

* Usage `forgeit example`

### `delete`

Deletes a installed template using its name.

* Usage `forgeit delete <template name>`

## Template Schema

It consists of the following properties:

* `name`: The name of the template.
* `label`: The label of the template.
* `description`: The description of the template.
* `variables`: An object containing variable definitions.
* `content`: An object containing the template content.
* `subtemplates`: An object containing subtemplate definitions.

## Template Types

The following types are supported:

* `template`: Renders a template file using the provided variables. Paths will always be relative to `templates` folder in the user profile.
* `file`: Copies a file from the provided path. Paths will always be relative to `static` folder in the user profile.
* `content`: Renders a string template using the provided variables.

## Template Context

When a template gets rendered, a `.forgeit.json` file is created in the current working directory so the `new` command nows which template use as parent and all the variables used to avoid introducing them again on every render.

## Example Template File

Here is an example template file that uses the schema defined in `forgeit/schemas.py`
```json
{
  "name": "my_template",
  "label": "My Template",
  "description": "This is a sample template.",
  "variables": {
    "name": {
      "type": "string",
      "label": "Name"
    },
    "age": {
      "type": "integer",
      "label": "Age"
    }
  },
  "content": {
    "index.html": "template:index.html.j2",
    "style.css": "file:style.css",
    "script.js": "content:<script>alert('Hello, {{ name }}!');</script>"
  },
  "subtemplates": {
    "child_template": {
      "label": "Child Template",
      "description": "This is a child template.",
      "variables": {
        "child_name": {
          "type": "string",
          "label": "Child Name"
        }
      },
      "content": {
        "child.html": "template:child.html.j2"
      }
    }
  }
}
```

This template defines two variables, `name` and `age`, and uses them to render three files: `index.html` using a template file, `style.css` by copying a file, and `script.js` using a string template. It also defines a subtemplate, child_template, which has its own variables and content.

Note: This is just a sample template file, and you can customize it to fit your needs.

## Template storage

All templates are stored locally in the user directory under `.forgeit` folder. For instance, in Windows you might encounter all the templates under `C:\Users\<USER NAME>\AppData\Roaming\forgeit`, in Mac OS under `~/Library/Application Support/.forgeit` or `~/.config/.forgeit` in Linux.

 All templates are centralized, so this directory is the only source of truth regarding template files and its metadata. In your first install, a `forgeit.db` file will be created to store in a convenient way all the required information to render the template.

## Why JSON?

JSON is a lightweight yet powerful format to define metadata. The starting approach was to use Python files to setup the templates. This was discarted due to security reasons. Since JSON are directly translated into dictionaries and its structure is a reflection from the original source it was a straight forward choice. YAML was discarted because it might required an extra step to understand its mappint to a dict or another structure in Python.
