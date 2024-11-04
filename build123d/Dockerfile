FROM python:3.12.7-slim-bookworm
WORKDIR /opt/build123d
RUN \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install \
        --assume-yes --quiet --no-install-recommends \
        inotify-tools=3.22.6.0-4 \
        libgl1=1.6.0-1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    python -m venv /opt/build123d && \
    . ./bin/activate && \
    pip install --no-cache-dir --upgrade pip==24.3.1 && \
    pip install --no-cache-dir build123d==0.7.0 watchdog[watchmedo]==6.0.0
WORKDIR /models
COPY ./entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
