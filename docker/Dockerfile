FROM python:3.9.16-slim-buster

LABEL image.author.name "jvfecav"

# Get curl/unzip
# Get curl/unzip
RUN apt-get update && \
    apt-get install -y curl unzip procps build-essential && \
    rm -rf /var/lib/apt/lists/*

# Install MicroView
RUN pip install https://github.com/dalmolingroup/microview/archive/main.zip

CMD ["bash"]
