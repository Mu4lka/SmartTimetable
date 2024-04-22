class Container:
    def __init__(self, properties: dict):
        for key, value in properties.items():
            self.__setattr__(key, value)
            
    @staticmethod
    def to_containers(dictionaries: list[dict]):
        for properties in dictionaries:
            yield Container(properties)
