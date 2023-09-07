from config import settings
from sqlalchemy.engine import URL, Engine
from sqlalchemy.orm import Session, sessionmaker

connection_url = URL.create(
    drivername="mssql+pyodbc",
    username=settings.username,
    password=settings.password,
    host=settings.host,
    port=settings.port,
    database=settings.database,
    query={
        "driver": "ODBC Driver 18 for SQL Server",
        "encrypt": settings.encrypt,
        "MultiSubnetFailover": settings.multisubnetfailover,
        "Connect Timeout": str(settings.connect_timeout)
    }
)


def create_session(engine: Engine) -> Session:
    Session = sessionmaker(bind=engine)
    return Session()
