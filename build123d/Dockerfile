FROM python:3.12.8-slim-bookworm
WORKDIR /opt/build123d
ADD https://github.com/noirblancrouge/Beon/raw/refs/heads/master/fonts/ttf/Beon-Regular.ttf /usr/share/fonts/truetype/beon/
RUN \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install \
        --assume-yes --quiet --no-install-recommends \
        fontconfig=2.14.1-4 \
        inotify-tools=3.22.6.0-4 \
        libgl1=1.6.0-1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    python -m venv /opt/build123d && \
    . ./bin/activate && \
    pip install --no-cache-dir --upgrade pip==24.3.1 && \
    pip install --no-cache-dir build123d==0.8.0 watchdog[watchmedo]==6.0.0
WORKDIR /models
COPY ./entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
