# Use an official Python runtime as the base image
FROM python:3.8-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose the port Gunicorn will listen on (default is 8000)
EXPOSE 8000

# Specify the command to run the Gunicorn server
CMD ["gunicorn", "-w", "4", "--bind", "0.0.0.0:8000", "app:app"]