class ClassSDMXAttributeError(Exception):
    """Base class for other exceptions"""

    def __init__(self, data, message):
        self.message = message
        self.data = data

    def __str__(self):
        return f'{self.data} -> {self.message}'


class ClassConfStatusError(ClassSDMXAttributeError):
    """Raised when the input value is not included in the list of available values for confStatus"""
    """Exception raised for errors in the input data.

    Attributes:
        data -- input data which caused the error
        message -- explanation of the error
    """

    def __init__(self, data, message="ConfStatus value is not the expected"):
        super().__init__(data=data, message=message)
