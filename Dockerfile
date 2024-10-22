FROM python:3.10-slim as build

ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN apt-get update \
    && apt-get install -y curl unzip gcc python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN bash -c "$(curl -L https://github.com/SSaeedhoseini/Marzban-scripts/raw/master/install_latest_xray.sh)"

COPY ./requirements.txt /code/
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN apt-get remove -y curl unzip gcc python3-dev

FROM build as prod

COPY . /code


RUN ln -s /code/marzban-cli.py /usr/bin/marzban-cli \
    && chmod +x /usr/bin/marzban-cli \
    && marzban-cli completion install --shell bash

CMD ["bash", "-c", "alembic upgrade head; python main.py"]