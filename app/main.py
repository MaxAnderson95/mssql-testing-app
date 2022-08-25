import pyodbc
import requests
import time
import sys
import os
from logger import configure_logging
from config import settings

logger = configure_logging(__name__)


def open_db_connection():
    return pyodbc.connect(
        settings.sql.connectionstring, autocommit=True, timeout=2
    )


def get_db_cursor(connection):
    return connection.cursor()


def get_users(connection):
    logger.info("Getting a list of users")
    try:
        cursor = get_db_cursor(connection)
        cursor.execute(
            "SELECT * FROM USERS"
        )
        rows = cursor.fetchall()
        cursor.close()
        logger.info(f"{len(rows)} users found.")
    except Exception as e:
        raise e
    return rows


def get_random_user():
    r = requests.get('https://random-data-api.com/api/v2/users')
    return r.json()


def insert_user(connection, first_name: str, last_name: str, dob: str):
    cursor = get_db_cursor(connection)
    try:
        cursor.execute(
            f"INSERT INTO [users] ([FirstName],[LastName],[DateOfBirth]) VALUES (?, ?, ?)", first_name, last_name, dob
        )
        connection.commit()
    except:
        logger.exception("Failed to insert user into user table")
    cursor.close()


def insert_random_user(connection):
    random_user = get_random_user()

    first_name = random_user.get("first_name")
    last_name = random_user.get("last_name")
    dob = random_user.get("date_of_birth")

    logger.info(f"Inserting a random user: {first_name} {last_name}")
    insert_user(
        connection,
        first_name,
        last_name,
        dob
    )


def main():
    logger.debug("Application Startup")
    logger.debug(f"Value of logging level: {settings.logging.level}")
    logger.debug(
        f"Value of SQL connection string: {settings.sql.connectionstring}")

    try:
        while True:
            sleep = 5
            logger.debug("Opening connection to database")
            try:
                connection = open_db_connection()
            except pyodbc.OperationalError:
                logger.error(
                    f"Failed to connect to database. Trying again in {sleep} seconds.")
                time.sleep(sleep)
                continue

            logger.debug("Connection open")

            try:
                users = get_users(connection)
            except:
                logger.error(
                    f"Error retreiving users from database. Trying again in {sleep} seconds.")
                logger.debug("Closing connection")
                connection.close()
                time.sleep(sleep)
                continue

            insert_random_user(connection)

            logger.info(f"Sleeping for {sleep} seconds.")
            logger.debug("Closing connection")
            connection.close()
            time.sleep(sleep)
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        try:
            connection.close()
        except BaseException:
            pass
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

    connection.close()


if __name__ == "__main__":
    main()
