"""
Configuration settings for the application and PostgreSQL database.

Provides settings for connecting to the database and configuring the application behavior.
"""

from pydantic_settings import BaseSettings


class PostgresSettings(BaseSettings):
    """
    PostgreSQL configuration settings.

    Attributes:
        HOST (str): The database host. Defaults to "localhost".
        USER (str): The username for the database. Defaults to "admin".
        PASSWORD (str): The password for the database. Defaults to "admin".
        DATABASE (str): The database name. Defaults to "postgres".
        PORT (int): The port for the database connection. Defaults to 5432.

    Properties:
        url (str): The database connection URL for asyncpg.
        url_for_alembic (str): The database connection URL for Alembic migrations.

    Config:
        case_sensitive (bool): Indicates if environment variables are case-sensitive. Defaults to False.
        env_prefix (str): Prefix for environment variables. Defaults to "PG_".
    """

    HOST: str = "localhost"
    PORT: int = 5432
    USER: str = "admin"
    PASSWORD: str = "admin"
    DATABASE: str = "postgres"

    @property
    def url(self) -> str:
        """
        Generate the database connection URL for asyncpg.

        Returns:
            str: The connection URL.
        """
        return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}"

    @property
    def url_for_alembic(self) -> str:
        """
        Generate the database connection URL for Alembic migrations.

        Returns:
            str: The connection URL.
        """
        return f"postgresql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}"

    class Config:
        """
        Configuration options for PostgresSettings.

        Attributes:
            case_sensitive (bool): Whether environment variables are case-sensitive. Defaults to False.
            env_prefix (str): The prefix for environment variables. Defaults to "PG_".
        """

        case_sensitive = False
        env_prefix = "PG_"


class AppSettings(BaseSettings):
    """
    Application configuration settings.

    Attributes:
        PORT (int): The port on which the application will run. Defaults to 3779.
        TITLE (str): The title of the application. Defaults to "Deposit API".
        VERSION (str): The version of the application. Defaults to "0.1.0".
        IS_DEBUG (bool): Whether the application is in debug mode. Defaults to False.

    Config:
        case_sensitive (bool): Indicates if environment variables are case-sensitive. Defaults to False.
    """

    PORT: int = 3779
    TITLE: str = "Deposit API"
    VERSION: str = "0.1.0"
    IS_DEBUG: bool = False

    class Config:
        """
        Configuration options for AppSettings.

        Attributes:
            case_sensitive (bool): Whether environment variables are case-sensitive. Defaults to False.
        """

        case_sensitive = False
        env_prefix = "APP_"
