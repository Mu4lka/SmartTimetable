class Event:
    def __init__(self):
        self.__delegate = []

    def subscribe(self, func):
        self.__delegate.append(func)

    def unsubscribe(self, func):
        self.__delegate.remove(func)

    async def invoke(self, *args):
        for func in self.__delegate:
            await func(*args)
