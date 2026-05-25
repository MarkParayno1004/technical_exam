class AddressNotFoundError(Exception):
    def __init__(self, address_id: int) -> None:
        self.address_id = address_id
        super().__init__(f"Address with id {address_id} not found")


class DatabaseError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)
