from datetime import datetime

from .ModelAbstract import ModelAbstract

__all__ = ["ModelResponse"]


class ModelResponse(ModelAbstract):
    """
    Represents a response model used for application data representation.

    ModelResponse is a subclass of ModelAbstract that encapsulates
    essential metadata fields commonly used for tracking record creation,
    modification, and deletion timelines.

    Attributes:
        id (int | None): Unique identifier for the response model. Defaults to NotImplemented.
        created_at (datetime | None): Timestamp indicating when the record was created.
            Defaults to NotImplemented.
        updated_at (datetime | None): Timestamp indicating when the record was last updated.
            Defaults to NotImplemented.
        deleted_at (datetime | None): Timestamp indicating when the record was deleted.
            Defaults to NotImplemented.
    """

    id: int | None = NotImplemented
    created_at: datetime | None = NotImplemented
    updated_at: datetime | None = NotImplemented
    deleted_at: datetime | None = NotImplemented
