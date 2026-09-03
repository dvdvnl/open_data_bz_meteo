FROM dvdvnl/devcontainer:python-3.14

# Install make
RUN apt-get update && apt-get install -y make bash-completion

# Upgrade pip
RUN pip install --upgrade pip

# Setup workdir
WORKDIR /usr/src/app

RUN mkdir -p /home/devcon/.ssh

# Install dependencies
COPY pyproject.toml .
RUN pip install -e .[develop]

# Keep the container running
CMD ["sleep", "infinity"]
