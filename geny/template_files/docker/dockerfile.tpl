# Base image
FROM python:3.11-alpine

# Working directory
WORKDIR /app

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8

# Copy dependencies
COPY requirements.txt /app

# Install dependencies...
# Code here...

# Copy other files to docker container
COPY . .

# Switch users
RUN groupadd -r docker && useradd --no-log-init -r -g docker docker
USER docker

CMD ["python3"]
