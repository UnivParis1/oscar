class EntityNotFoundError(Exception):
    pass


class DuplicateEntitiesError(Exception):
    pass


class ConnectionFailureError(ConnectionError):
    pass
