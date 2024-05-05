class Container:
    def __init__(self, input_dict: dict):
        for key, value in input_dict.items():
            setattr(self, key, value)
            
    @staticmethod
    def to_containers(input_dicts: list[dict]):
        for input_dict in input_dicts:
            yield Container(input_dict)
