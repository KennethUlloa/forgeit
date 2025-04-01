import os
from .engine import Engine
from .model import Template, TemplateType, Context

""""
class _Template:
    def __init__(
        self,
        *,
        name: str,
        label: str,
        variables: dict[str, dict],
        content: dict[str, str],
        computed: dict[str, Any] = {},
        **_,
    ):
        self.name = name
        self.label = label
        self.variables = {
            name: VariableTypeStore.get(var["type"])(name=name, **var)
            for name, var in variables.items()
        }
        self.env = {
            "$cwd$": CWD,
            "$appdir$": APP_DIR
        }
        self.content = content
        self.computed = computed

    def render(self, root: str, store: bool = True, context: dict = {}):
        context.update(self.get_variables())
        content = self.bind_env_to_content(root)
        for target, source in track(content.items(), "Rendering template..."):
            rich.print(f":white_check_mark: [green]{self.render_item(target, source, context)}[/green]")

        if not store:
            return

        output = {"variables": context, "$root$": root, "name": self.name}

        with open(CURRENT_TEMPLATE, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2)

    def render_item(self, target: str, source: str, variables: dict):
        target_path = render_string(target, variables)
        file_content = self.get_content_from_source(source, variables)
        dirname = os.path.dirname(target_path)
        os.makedirs(dirname, exist_ok=True)
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(file_content)
        return target_path

    def bind_env_to_content(self, root: str):
        env = {**self.env}
        env["$root$"] = root
        content = {}
        # Set up env in the content templates
        for target, source in self.content.items():
            key = target
            value = source
            for name, val in env.items():
                key = key.replace(name, val)
                value = value.replace(name, val)
            content[key] = value

        return content

    def get_variables(self):
        return {name: var.request_input("") for name, var in self.variables.items()}

    def get_content_from_source(self, source: str, data: dict):
        parts = source.split(":", 1)
        if parts[0] in ["file", "template"]:
            with open(parts[1], "r", encoding="utf-8") as f:
                content = f.read()
                if parts[0] == "template":
                    content = render_string(content, data)
                return content
        if parts[0] == "content":
            return render_string(parts[1], data)
"""


def render_file(
    target: str, source: str, ctx: Context, variables: dict, engine: Engine
):
    output_path = engine.render_string(target, variables)
    output_path = os.path.normpath(output_path)
    template_type, content = source.split(":", 1)

    if template_type not in TemplateType.values():
        raise ValueError(
            f"{template_type} is not a valid template type, expected any of {','.join(TemplateType.values())}"
        )

    rendered_content = content

    match template_type:
        case TemplateType.TEMPLATE:
            rendered_content = engine.render_file(content, variables)

        case TemplateType.FILE:
            with open(engine.render_string(content, ctx), "r", encoding="utf-8") as f:
                rendered_content = f.read()

        case TemplateType.CONTENT:
            rendered_content = engine.render_string(content, variables)

    output_path_dir = os.path.dirname(output_path)
    os.makedirs(output_path_dir, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered_content)

    return output_path


def render_template(template: Template, ctx: Context, variables: dict):
    engine = Engine(template.path)
    return [
        render_file(os.path.join(ctx.root, target), source, ctx, variables, engine)
        for target, source in template.content.items()
    ]
