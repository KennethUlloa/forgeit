# Controller for {{ module_name }} module
from flask import Blueprint, request
from .model import {{ module_camel_case }}, {{ module_camel_case }}Repository
from .view import {{ module_name }}_view


{{ module_name }}_bp = Blueprint('{{ module_name }}', __name__, url_prefix='/{{ module_name }}s')


@{{ module_name }}_bp.get('')
def get_{{ module_name }}():
    repository = {{ module_camel_case }}Repository()
    return [{{ module_name }}_view(entity) for entity in repository.find_all()]


@{{ module_name }}_bp.get('<int:id>')
def get_{{ module_name }}(id: int):
    repository = {{ module_camel_case }}Repository()
    return {{ module_name }}_view(repository.find_by_id(id))


@{{ module_name }}_bp.post('')
def post_{{ module_name }}():
    repository = {{ module_camel_case }}Repository()
    entity = {{ module_camel_case }}(**request.json)
    return {{ module_name }}_view(repository.save(entity)), 201


@{{ module_name }}_bp.put('<int:id>')
def put_{{ module_name }}(id: int):
    repository = {{ module_camel_case }}Repository()
    entity = {{ module_camel_case }}(**request.json)
    entity.id = id
    return {{ module_name }}_view(repository.update(entity))


@{{ module_name }}_bp.delete('<int:id>')
def delete_{{ module_name }}(id: int):
    repository = {{ module_camel_case }}Repository()
    repository.delete(id)
    return '', 204