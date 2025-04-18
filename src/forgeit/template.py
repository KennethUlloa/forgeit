from dataclasses import asdict
import os
from typing import Callable, Protocol
from . import env
from .engine import RenderEngine
from .model import Template, TemplateType, Context, SubTemplate, BaseTemplate
from .utils import read, save


class RenderContext(Protocol):
    template: BaseTemplate
    ctx: Context
    variables: dict
    engine: RenderEngine
    template_path: str
    static_path: str


type ContentRenderCallback = Callable[[RenderContext, str], str]


def _file_renderer(ctx: RenderContext, path: str) -> str:
    input_path = os.path.join(
        ctx.static_path,
        ctx.engine.render_string(path, asdict(ctx.ctx)),
    )

    with read(input_path) as f:
        return f.read()


def _template_renderer(ctx: RenderContext, path: str) -> str:
    return ctx.engine.render_file(path, ctx.variables)


def _content_renderer(ctx: RenderContext, path: str) -> str:
    return ctx.engine.render_string(path, ctx.variables)


class TemplateRenderer:
    __content_renderers: dict[TemplateType, ContentRenderCallback] = {
        TemplateType.FILE: _file_renderer,
        TemplateType.TEMPLATE: _template_renderer,
        TemplateType.CONTENT: _content_renderer,
    }

    def __init__(self, template: BaseTemplate, ctx: Context, variables: dict) -> None:
        self.template_path = os.path.realpath(
            os.path.join(env.APP_DIR, template.path_name, "templates")
        )
        self.static_path = os.path.realpath(
            os.path.join(env.APP_DIR, template.path_name, "files")
        )

        self.engine = RenderEngine(self.template_path)
        self.template = template
        self.ctx = ctx
        self.variables = variables

    def render(self, root: str):
        return [
            self.render_content(target, source, root)
            for target, source in self.template.content.items()
        ]

    def render_callbacks(self, root: str) -> list[Callable[[], str]]:
        def create_callback(target: str, source: str) -> Callable[[], str]:
            return lambda: self.render_content(target, source, root)

        return [
            create_callback(target, source)
            for target, source in self.template.content.items()
        ]

    def render_content(self, target: str, source: str, root: str):
        template_type, content = source.split(":", 1)
        renderer = self.__content_renderers[template_type]
        content = renderer(self, content)

        output_path = os.path.normpath(
            os.path.join(root, self.engine.render_string(target, self.variables))
        )

        output_path_dir = os.path.dirname(output_path)
        if output_path_dir:
            os.makedirs(output_path_dir, exist_ok=True)

        with save(output_path) as f:
            f.write(content)

        return output_path


def template_path(template: Template):
    return os.path.normpath(
        os.path.join(
            env.APP_DIR,
            template.parent_name
            if isinstance(template, SubTemplate)
            else template.name,
        )
    )
