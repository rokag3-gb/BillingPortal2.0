FROM python:3.9-slim
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y g++ build-essential unixodbc-dev ca-certificates curl libgssapi-krb5-2 && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt && python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "Mate365BillingPortal.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]