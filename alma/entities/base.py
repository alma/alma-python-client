from copy import deepcopy


class Base:
    def __init__(self, data):
        for attr, value in data.items():
            self.__setattr__(attr, deepcopy(value))
