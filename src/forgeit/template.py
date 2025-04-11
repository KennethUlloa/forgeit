import os
from . import env
from .engine import Engine
from .model import Template, TemplateType, Context, SubTemplate
from .utils import read, save


def path(template: Template):
    return os.path.normpath(
        os.path.join(
            env.APP_DIR,
            template.parent_name
            if isinstance(template, SubTemplate)
            else template.name,
        )
    )


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
            with read(engine.render_string(content, ctx)) as f:
                rendered_content = f.read()

        case TemplateType.CONTENT:
            rendered_content = engine.render_string(content, variables)

    output_path_dir = os.path.dirname(output_path)
    os.makedirs(output_path_dir, exist_ok=True)

    with save(output_path) as f:
        f.write(rendered_content)

    return output_path


def render_template_as_callbacks(template: Template, ctx: Context, variables: dict):
    engine = Engine(path(template))

    def create_callback(target, source):
        def render():
            return render_file(
                os.path.join(ctx.root, target), source, ctx, variables, engine
            )

        return render

    return [
        create_callback(target, source) for target, source in template.content.items()
    ]


def render_template(template: Template, ctx: Context, variables: dict):
    engine = Engine(path(template))
    return [
        render_file(os.path.join(ctx.root, target), source, ctx, variables, engine)
        for target, source in template.content.items()
    ]
