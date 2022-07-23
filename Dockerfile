FROM python:3.9-slim

RUN apt-get update \
    && apt-get install -y curl gcc g++ gnupg2 \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/ubuntu/21.04/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 mssql-tools unixodbc unixodbc-dev \
    && apt-get clean

WORKDIR /srv/

RUN touch .env
COPY requirements.txt /srv/

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt && rm -rf .cache/pip

COPY . /srv/

EXPOSE 8080

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8080", "--noreload"]

