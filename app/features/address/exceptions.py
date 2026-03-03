

class AddressNotFoundError(Exception):
    """Raised when an address is not found."""
    pass


class AddressAlreadyExistsError(Exception):
    """Raised when trying to create a duplicate address."""
    pass

