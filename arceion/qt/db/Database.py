from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeMeta, Session, sessionmaker

__all__ = ['Database']


class Database:
    db_name: str
    engine: Engine
    Model: DeclarativeMeta
    session: Session

    def __init__(self, db_name):
        """
        Initializes a database connection and ORM setup.

        This constructor method sets up a database engine and an ORM base using
        SQLAlchemy. It prepares the connection to the specified SQLite database and
        configures a session object for interacting with it.

        Attributes:
        db_name: str
            The name of the SQLite database file to connect to.
        engine
            The SQLAlchemy database engine created for the specified SQLite database.
        Model
            The declarative base class for defining ORM models.
        session
            The SQLAlchemy session object for managing transactions.

        Parameters:
        db_name: str
            The name of the SQLite database file to connect to.
        """

        self.db_name = db_name
        self.engine = create_engine('sqlite:///' + self.db_name, echo_pool=True)
        self.Model = declarative_base()
        self.session = sessionmaker(bind=self.engine)()

    def create_all(self) -> None:
        """
        Creates all database tables defined in the metadata.

        This method utilizes the SQLAlchemy metadata object to generate and execute
        the SQL statements necessary to create all the tables associated
        with the current database engine. It is typically used during the
        initial setup phase of a database system.

        Raises:
            Any exceptions that may be raised by SQLAlchemy when creating tables
            (e.g., database connectivity issues, incorrect schema definitions, etc.).

        Returns:
            None
        """

        self.Model.metadata.create_all(self.engine)
