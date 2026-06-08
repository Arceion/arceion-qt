from .ModelAbstract import ModelAbstract

__all__ = ["ModelRequest"]


class ModelRequest(ModelAbstract):
    """
    Represents a model request used for processing and managing data operations.

    This class serves as a specific implementation or extension of the
    ModelAbstract base class. It provides an interface for defining and handling
    model-related requests in the application or system. It is designed to be
    extended or instantiated where necessary and supports the inclusion of an
    identifier for identifying specific model requests.

    Attributes:
        id (int | None): Identifier for the model request. Defaults to
            NotImplemented if not provided or set explicitly.
    """

    id: int | None = NotImplemented
