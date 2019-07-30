# this should be ran using python:3.7
FROM python:3.7

# Creating a user tu run the process
RUN groupadd -r extuser && useradd -r -g extuser extuser

# installing system deps.
RUN apt-get update && apt-get install -y  \
    sed \
    && apt-get clean


# create data directory
RUN mkdir -p /upload /extmp \
#	&& chown -R extuser:extuser /data \
	&& chown -R extuser:extuser /upload \
	&& chown -R extuser:extuser /extmp \
	&& chmod -R 757 /upload \
	&& chmod -R 757 /extmp


# VOLUME /data
VOLUME /upload


COPY . /app

# Set the working directory to /app
WORKDIR /app

RUN chown -R extuser:extuser /app


# Install any needed packages specified in requirements.txt
RUN pip install -U pip && pip install .


COPY bin /opt/extractxt

RUN chown -R extuser:extuser /opt/extractxt \
    && chmod 757 /opt/extractxt \
    && chmod +x /opt/extractxt/*.sh

ENV PROCESSTXT_SCRIPT /opt/extractxt/processtxt.sh


ENV UPLOAD_FOLDER '/upload'

ENV TMP_FOLDER '/extmp'

# setting up the environment variables for the rmxbot configuration file
ENV RMXBOT_ENDPOINT 'http://localhost:8000'

# the redis host
ENV REDIS_HOST_NAME 'redis'

# Make port 8003 available to the world outside this container
EXPOSE 8003

USER extuser
