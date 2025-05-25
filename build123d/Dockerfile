FROM python:3.13.3-slim-bookworm
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
    pip install --no-cache-dir --upgrade pip==25.0 && \
    pip install --no-cache-dir build123d==0.9.1 watchdog[watchmedo]==6.0.0
WORKDIR /models
COPY ./entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
