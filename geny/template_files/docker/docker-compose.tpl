# These settings are provided for development purposes only. Not suitable for production.

version: '3'

volumes:
    database:


services:
  app:
    container_name: "{{ project }}_web"
    build:
        context: .
    # command: "gunicorn {{ project }}.wsgi:application --bind 0.0.0.0:{{ port }} --workers {{ workers }}"
    volumes:
        - .:/app
    env_file:
        - .env
    ports:
        - 8007:8000 # host:docker
    depends_on:
        - database
        - celery-worker

  database:
    container_name: "{{ project }}_database"
    image: postgres:15-alpine
    volumes:
        - ./database:/var/lib/postgresql/data/
    ports:
        - 5437:5432 # host:docker
    env_file:
        - .env
    healthcheck:
        test: ["CMD-SHELL", "pg_ready -U postgres"]
        interval: 10s
        timeout: 83s
        retries: 40
    restart: unless-stopped

  redis:
    container_name: "{{ project }}_redis"
    image: redis:latest
    ports:
        - 6377:6379 # host:docker
    restart: unless-stopped

  celery_worker:
    container_name: "{{ project }}_celery_worker"
    build:
      context: .
    # command: celery worker --app {{ project }} --concurrency=20 -linfo -E
    depends_on:
      - redis
    env_file:
      - .env
    restart: on-failure
    stop_grace_period: 5s
