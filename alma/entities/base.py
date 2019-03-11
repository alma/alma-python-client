from copy import deepcopy


class Base:
    def __init__(self, data):
        self._data = data

        for attr, value in data.items():
            self.__setattr__(attr, deepcopy(value))

    @property
    def raw_data(self):
        return self._data
