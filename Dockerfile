# Pull the official base image
FROM python:3.9.6-slim-buster

# Set work directory in the Docker image
WORKDIR /potlako

ARG BASE_API_URL
ARG EMAIL_BACKEND
ARG EMAIL_HOST
ARG EMAIL_USE_TLS
ARG EMAIL_PORT
ARG EMAIL_USER
ARG EMAIL_HOST_PASSWORD
ARG EDC_SYNC_EVALUATION_TIMELINE_API
ARG EDC_SYNC_NAV_PLAN_API
ARG EDC_DEVICE_ID
ARG EDC_DEVICE_ROLE
ARG EDC_SYNC_SERVER_IP
ARG EDC_SYNC_FILES_REMOTE_HOST
ARG EDC_SYNC_FILES_USER
ARG EDC_SYNC_FILES_USB_VOLUME
ARG EDC_SYNC_FILES_REMOTE_MEDIA
ARG MYSQL_HOST
ARG MYSQL_ROOT_PASSWORD
ARG MYSQL_DB_NAME
ARG MYSQL_USER
ARG MYSQL_PASSWORD

# Set environment variables in the Docker image
# Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED 1

ENV EDC_SMS_BASE_API_URL ${EDC_SMS_BASE_API_URL}
ENV BASE_API_URL ${BASE_API_URL}
ENV EMAIL_BACKEND ${EMAIL_BACKEND}
ENV EMAIL_HOST ${EMAIL_HOST}
ENV EMAIL_USE_TLS ${EMAIL_USE_TLS}
ENV EMAIL_PORT ${EMAIL_PORT}
ENV EMAIL_USER ${EMAIL_USER}
ENV EMAIL_HOST_PASSWORD ${EMAIL_HOST_PASSWORD}
ENV COMMUNITIES_ENHANCED_CARE ${COMMUNITIES_ENHANCED_CARE}
ENV COMMUNITIES_INTERVENTION ${COMMUNITIES_INTERVENTION}
ENV EDC_DEVICE_ROLE ${EDC_DEVICE_ROLE}
ENV EDC_DEVICE_ID ${EDC_DEVICE_ID}
ENV EDC_SYNC_SERVER_IP ${EDC_SYNC_SERVER_IP}
ENV EDC_SYNC_EVALUATION_TIMELINE_API ${EDC_SYNC_EVALUATION_TIMELINE_API}
ENV EDC_SYNC_NAV_PLAN_API ${EDC_SYNC_NAV_PLAN_API}
ENV EDC_SYNC_FILES_SYNC_USER ${EDC_SYNC_FILES_SYNC_USER}
ENV EDC_SYNC_FILES_REMOTE_HOST ${EDC_SYNC_FILES_REMOTE_HOST}
ENV EDC_SYNC_FILES_USB_VOLUME ${EDC_SYNC_FILES_USB_VOLUME}
ENV EDC_SYNC_FILES_REMOTE_MEDIA ${EDC_SYNC_FILES_REMOTE_MEDIA}
ENV MYSQL_ROOT_PASSWORD ${MYSQL_ROOT_PASSWORD}
ENV MYSQL_DB_NAME ${MYSQL_DB_NAME}
ENV MYSQL_USER ${MYSQL_USER}
ENV MYSQL_DB_PASSWORD ${MYSQL_DB_PASSWORD}
ENV SSH_PASSWORD ${SSH_PASSWORD}
ENV MYSQL_HOST ${MYSQL_HOST}

SHELL ["/bin/bash", "-c"]

RUN function retry { for _ in {1..3}; do "$@" && return || sleep 5; done; }; \
    retry apt-get update && retry apt-get install -y git default-libmysqlclient-dev gcc pkg-config libcups2-dev
RUN apt-get update && apt-get install -y curl
# Dockerfile
RUN apt-get update && apt-get install -y mariadb-client
RUN apt-get update && apt-get install -y rsync
# Upgrade pip
RUN pip install --upgrade pip

#copy ssh key
COPY .ssh/id_rsa /root/.ssh/id_rsa

#update permissions
RUN chmod 600 ~/.ssh/id_rsa

# Install dependencies
COPY ./requirements_production.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements_production.txt -U \
    && pip uninstall pycrypto -y \
    && pip uninstall pycryptodome -y \
    && pip install python-dotenv \
    && pip install pycryptodome \
    && pip install Django==3.1.14

RUN mkdir -p /etc/potlako \
    && mkdir -p ~/crypto_fields \
    && chown -R $USER:$USER /etc/potlako

# Copy project
COPY . .

# Run the application:
CMD [ "python", "‘db_check’.py"]
CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000" ]