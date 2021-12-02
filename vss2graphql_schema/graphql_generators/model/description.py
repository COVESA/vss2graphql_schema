class Description:
    __slots__ = ('description', 'unit', 'min_value', 'max_value', 'enum')
    description: str
    unit: str
    min_value: str
    max_value: str
    enum: str

    def __init__(
            self, description: str, unit: str = '', min_value: str = '',
            max_value: str = '', enum: str = '',
    ) -> None:
        self.description = description
        self.unit = unit
        self.min_value = min_value
        self.max_value = max_value
        self.enum = enum

    def __str__(self) -> str:
        values = []
        if self.unit:
            values.append('@unit: ' + self.unit)
        if self.min_value:
            values.append('@min: ' + self.min_value)
        if self.max_value:
            values.append('@max: ' + self.max_value)
        if self.enum:
            values.append('@enum: ' + self.enum)

        return self.description + ('\n' + '\n'.join(values) if values else '')

    def empty(self) -> bool:
        for s in self.__slots__:
            if getattr(self, s, False):
                return False
        return True
