FROM python:3.9-slim
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y g++ build-essential unixodbc-dev ca-certificates \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt && python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "Mate365BillingPortal.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]