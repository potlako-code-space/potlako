# Pull the official base image
FROM python:3.9.6-slim-buster

# Set work directory in the Docker image
WORKDIR /app

# Set environment variables in the Docker image
# Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY ./requirements_production.txt .
RUN pip install --upgrade pip && pip install -r requirements_production.txt

# Copy project
COPY . .

# Run the application:
CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000" ]