# MSSQL Testing App

A testing app written in Python that I use to test SQL server failover cluster and Always On Availability Group failover functionality.

## Running

To run from the command line simply run `python app\main.py`

Or run via docker `docker run -it maxanderson95/mssql-testing-app:latest`

## Configuration

You can specify configuration using environment variables.

To specify logging level: `DYNACONF_LOGGING.LEVEL="DEBUG"`. The default is `INFO`.

To specify the connection string that the app will use to connect to the database server: `DYNACONF_SQL.CONNECTIONSTRING=DRIVER={FreeTDS};SERVER=;PORT=;DATABASE=;UID=;PWD="`.

## Example

Here is an example of running via Docker while passing in the environment variables:

`docker run -e DYNACONF_LOGGING.LEVEL="DEBUG" -e DYNACONF_SQL.CONNECTIONSTRING="DRIVER={FreeTDS};SERVER=1.2.3.4\INSTANCENAME;PORT=1433;DATABASE=db;UID=dbuser;PWD=abc123" -it --rm maxanderson95/mssql-testing-app:latest`