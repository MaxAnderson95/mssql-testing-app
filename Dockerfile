FROM python:3.11

# Install the ODBC 18 Drivers
COPY odbc_driver.sh .
RUN /bin/bash odbc_driver.sh
RUN rm odbc_driver.sh

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source
COPY ./src /app

# Set working directory
WORKDIR /app

# Run the application
CMD ["python", "main.py"]
