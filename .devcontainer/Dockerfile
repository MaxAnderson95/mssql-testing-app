FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

# Install the ODBC 18 Drivers
COPY odbc_driver.sh .
RUN /bin/bash odbc_driver.sh