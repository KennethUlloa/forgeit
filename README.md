# ForgeIt
Scaffolding library written in Python. Jinja2 is used for template rendering and Typer for CLI.

## CLI Documentation

It provides the following commands:

### `init`

Render a template's files given a name. If no variables file is given, the user will be prompted to enter them manually.

* Usage: `fg init <name> [<file>]`

### `new`

Renders a template's fragment (subtemplate) using stored context `.forge.json` file. If no variables file is given, the user will be prompted to enter the manually.

* Usage: `fg new <name> [<file>]`

### `install`

Installs a template description from a file path. It must be a ZIP File.

The provided ZIP file must have the following structure:
```
[zip file]
    templates/
        # Files with jinja syntax
    static/
        # Files that will be cloned
    template.json # Template schema/definition
```

* Usage: `fg install <path>`

### `list`

Lists all the available templates.

* Usage: `fg list`


### `version`

Displays the current version of the tool.

* Usage: `fg version`

### `validate`

Validate a template description. It must be a JSON file.

* Usage: `fg validate <file>`

### `example`

Create an example template. It will create a ZIP file containing a basic layout of a 
valid template in the current working directory. You could install it to use it if you want.

* Usage `fg example`

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