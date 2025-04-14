class DecompilerException(Exception):
    def __init__(self, location: int, message: str) -> None:
        super().__init__(f"At {location}: {message}")
        self.message = message
        self.location = location
