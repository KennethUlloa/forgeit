# Models for {{ module_name }} module
class {{ module_camel_case }}:
    id: int


class {{ module_camel_case }}Repository:
    def find_all(self) -> list[{{ module_camel_case }}]:
        pass
    
    def save(self, entity: {{ module_camel_case }}) -> {{ module_camel_case }}:
        pass
    
    def delete(self, id: int) -> None:
        pass

    def find_by_id(self, id: int) -> {{ module_camel_case }}:
        pass

    def update(self, entity: {{ module_camel_case }}) -> {{ module_camel_case }}:
        pass
