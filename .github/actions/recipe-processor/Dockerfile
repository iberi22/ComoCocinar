# Container image that runs your code
FROM python:3.11-slim

# Install git and python dependencies
RUN apt-get update && apt-get install -y --no-install-recommends git dos2unix && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir pyyaml python-frontmatter sentence-transformers

# Copies your action code to the filesystem path `/` of the container
COPY entrypoint.sh /entrypoint.sh
COPY extract_metadata.py /extract_metadata.py
COPY generate_embeddings.py /generate_embeddings.py

# Ensure entrypoint.sh is executable and in Unix format
RUN dos2unix /entrypoint.sh && chmod +x /entrypoint.sh

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/entrypoint.sh"]
