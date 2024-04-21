class Sheet:
    gridProperties: dict = None
    index: int = None
    sheetId: int = None
    sheetType: str = None
    title: str = None

    def __init__(self, properties: dict):
        for key, value in properties.items():
            self.__setattr__(key, value)
