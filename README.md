# MSSQL Testing App

A testing app written in Python that I use to test SQL server failover cluster and Always On Availability Group failover functionality.

## Running

To run from the command line simply run `python src\main.py`

Or run via docker:

1. Build and tag the image `docker build -t mssql-testing-app .`
1. Run the container `docker run -it mssql-testing-app`

## Configuration

You will need to specify various settings for the app to startup.

This is done using a file. There are two example `.toml` files in this directory. The app will look for a config file named `settings.toml` in the working directory.

## Example

Here is an example of running the container while also mounting in a settings file as a volume:

```
docker run -it -v $(pwd)/settings_native.toml:/app/settings.toml mssql-testing-app
```
