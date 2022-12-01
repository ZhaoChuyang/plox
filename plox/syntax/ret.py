class Return(RuntimeError):
    def __init__(self, value: object, message: str = None):
        super().__init__(message)
        self.value = value
