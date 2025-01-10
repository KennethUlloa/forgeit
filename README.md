# ForgeIt

Configurable project generator CLI tool.

## Object description
- An object with a single key that starts with `$`.
- Objects passed as the value of an object description will act as keyword arguments and lists will be treated as positional arguments.
- If you provide any other value to the object description it will return just the symbol, not an instance of that symbol.
- The description must follow the dot format as the path of the module for the leading symbol.

JSON

```json
{
  "$module.Class": {
    "kwarg1": 100,
    "kwarg2": {
        "module1.Class": ["arg1", "arg1"]
    },
    "kwarg3": { 
        "$module2.Class": null 
    }
  }
}
```
Python
```python
import module
import module1
import module2

obj = module.Class(
    kwarg1=100, 
    kwarg2=module1.Class("arg1", "arg2"), 
    kwarg3=module2.Class
)
```
## Variables
Objects that represent the name and the type of a needed value for the template. They provide information for the CLI to show different prompts based on the type.

You can nest variables inside others as long as the end node represents a type.

#### Example
Let's imagine you need to retrieve the following information of your user:
- Name
- Age
- Favourite sports
- Address
    - Street
    - Postal code

You should provide this object to the template:
```json
{
    "name": {"$str": null},
    "age": {"$int": null},
    "nicknames": {"$list": null}
    "address": {
        "street": {"$str": null},
        "postalCode": {"$int": null}
    }
}
```
The CLI will show different prompts for each type. Internally the data will be modeled like the following:
```json
{
    "name": "John Doe",
    "age": 26,
    "nicknames": ["Johnny", "Joe"]
    "address": {
        "street": "1234 Main Street",
        "postalCode": 123456
    }
}
```
Then you could access the user address like `address.street` (if your selected template engine supports this syntax).

## Processors
Object that "process" and add/update variables in a given dictionary. Dot notation is used to access/set nested variables.

Let's continue with the example of the user
```json
{
    "name": "John Doe",
    "age": 26,
    "nicknames": ["Johnny", "Joe"]
    "address": {
        "street": "1234 Main Street",
        "postalCode": 123456
    }
}
```
For instance, if you needed to create an slug based on the name for the person and store it in a new key you could do this in your template definition:
```json
{
    /* ... */
    "processors":[
        {
            "$forgeit.processor.SnakeCase": ["name","slug"]
        }
    ]
}
```
And after the processing, the data would look like this:
```json
{
    "name": "John Doe",
    "age": 26,
    "nicknames": ["Johnny", "Joe"]
    "address": {
        "street": "1234 Main Street",
        "postalCode": 123456
    },
    "slug": "john_doe"
}
```
Processors are lineal, that's why they're inside an array. Once a processor finishes its processing, the results are available for the next processor. 

When storing a new key, if the path doesn't exists, it is created. Storing the proccesed value of `SnakeCase` in `url.slug` will create the following inside the data dictionary:
```json
{
    /* ... */
    "url": {
        "slug": "john_doe"
    }
}
```
## Configuration
By default, the tool is expecting an object with this signature:
```python
class Config:
    TEMPLATES: dict[str, ITemplate]
    ENGINE: ITemplateEngine
    ENCODING: str
```

So you can reference any class/object that has this shape and it will work.

If you are using the tool just as a library you could use Python objects directly instead of loading the configuration from JSON files.

## Engines
An abstract class definition is used to avoid sticking to an specific engine, so you can basically install and use any engine you desire as long as you create a wrapper class around the engine to use it with the tool. By default, Jinja is used to render all.