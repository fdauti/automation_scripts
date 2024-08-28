FROM debian:stable

# Install python and git
RUN apt-get update -y \
 && apt-get install -y python3 \
 && apt-get install -y python3-venv \
 && apt-get install -y python3-pip \
 && apt-get install -y git

# Set the time zone
ENV TZ="America/Toronto"

# Custom cache invalidation
ARG CACHEBUST=1

# Clone netdd repository  
RUN git clone https://.../netdd_demo.git

# Replace 'activate' cmd by setting the environment variables
RUN mkdir /netdd_demo/venv
ENV VIRTUAL_ENV=/netdd_demo/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Persistent volume mount point
VOLUME /netdd_demo/files

# Install dependencies:
RUN python3 -m pip install --upgrade pip \ 
    && pip3 install -r /netdd_demo/requirements.txt

# Run the application:
WORKDIR /netdd_demo
ENTRYPOINT ["python3", "netdd_main.py"]
