# this should be ran using python:3.6
FROM python:3.7

# Creating a user tu run the process
RUN groupadd -r extuser && useradd -r -g extuser extuser


# create data directory
RUN mkdir -p /data && mkdir /upload \
	&& chown -R extuser:extuser /data \
	&& chown -R extuser:extuser /upload

ENV UPLOAD_FOLDER '/upload'

ENV TMP_FOLDER '/tmp'


# install tesseract
RUN apt-get update && \
	apt-get -y install \
	tesseract-ocr-all \
	poppler-utils \
	imagemagick \
	sed \
	&& apt-get clean

VOLUME /data

# setting up the environment variables for the rmxbot configuration file
ENV RMXBOT_ENDPOINT 'http://localhost:8000'

# the redis host
ENV REDIS_HOST_NAME 'redis'

COPY . /app

COPY bin /opt/extractbin

RUN chmod 755 /opt/extractbin && chmod +x /opt/extractbin/*.sh

# Set the working directory to /app
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip install -U pip && pip install .


ENV PDFTOTXT_SCRIPT /opt/extractbin/pdftotext.sh
ENV PROCESSTXT_SCRIPT /opt/extractbin/processtxt.sh


RUN chown -R extuser:extuser /app

# Make port 8003 available to the world outside this container
EXPOSE 8003

USER extuser
