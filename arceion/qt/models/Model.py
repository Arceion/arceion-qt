from datetime import datetime

from .ModelAbstract import ModelAbstract

__all__ = ["Model"]


class Model(ModelAbstract):
    """
    Represents a data model with timestamp and identifier attributes.

    This class implements the structure for a data model, incorporating identifiers
    and timestamps for managing object states such as creation, updates, and deletion.
    It extends the functionality defined in the `ModelAbstract` parent class.

    Attributes:
        id (int | None): Unique identifier for the instance. Defaults to NotImplemented.
        created_at (datetime | None): Timestamp indicating when the instance was created.
            Defaults to NotImplemented.
        updated_at (datetime | None): Timestamp indicating the last time the instance was
            updated. Defaults to NotImplemented.
        deleted_at (datetime | None): Timestamp indicating when the instance was deleted,
            if applicable. Defaults to None.
    """

    id: int | None = NotImplemented  # type: ignore
    created_at: datetime | None = NotImplemented
    updated_at: datetime | None = NotImplemented
    deleted_at: datetime | None = None
