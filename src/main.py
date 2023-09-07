import sys
import time
import requests
from config import settings
from logger import configure_logging
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from schema import Base, User
from sql import connection_url, create_session

logger = configure_logging(__name__)


def get_random_user() -> dict:
    r = requests.get('https://random-data-api.com/api/v2/users')
    return r.json()


def insert_user(engine: Engine, first_name: str, last_name: str, date_of_birth: str) -> None:
    new_user = User(first_name=first_name, last_name=last_name,
                    date_of_birth=date_of_birth)
    session = create_session(engine)
    session.add(new_user)
    session.commit()
    session.close()


def insert_random_user(engine: Engine) -> None:
    random_user_data = get_random_user()
    first_name, last_name, date_of_birth = random_user_data[
        'first_name'], random_user_data['last_name'], random_user_data['date_of_birth']
    logger.debug(f"Inserting a random user: {first_name} {last_name}")
    insert_user(engine, first_name, last_name, date_of_birth)


def get_users(engine: Engine) -> list[User]:
    session = create_session(engine)
    users = session.query(User).all()
    session.close()
    return users


def main() -> None:
    logger.debug(
        f"Starting the application using connection string:\n {connection_url}")

    try:
        sleep = settings.sleep_between_inserts
        counter = 0
        while True:
            # Sleep for the specified amount of time
            counter += 1
            if counter > 1:  # Don't sleep on the first iteration
                logger.debug(f"Sleeping for {sleep} seconds")
                time.sleep(sleep)

            # Create the engine and connect
            engine = create_engine(connection_url)
            connected = False
            while connected == False:
                try:
                    logger.debug("Connecting to the database")
                    engine.connect()

                    # Create the tables if they don't exist
                    Base.metadata.create_all(engine)
                except Exception as e:
                    engine.dispose()
                    logger.error(f"Failed to connect to the database {e}")
                    logger.debug(
                        f"Sleeping for {settings.sleep_between_inserts} seconds")
                    time.sleep(settings.sleep_between_inserts)
                else:
                    connected = True

            # Get a list of the users in the database
            try:
                users = get_users(engine)
                logger.debug(f"Number of users in the database: {len(users)}")
            except Exception as e:
                logger.error(f"Failed to get users from the database {e}")
                engine.dispose()
                connected = False
                continue

            # Insert a random user
            try:
                insert_random_user(engine)
            except Exception as e:
                logger.error(f"Failed to insert user into user table {e}")
                engine.dispose()
                connected = False
                continue

    except KeyboardInterrupt as e:
        logger.debug("Exiting...")
        engine.dispose()
        sys.exit(0)


if __name__ == "__main__":
    main()
