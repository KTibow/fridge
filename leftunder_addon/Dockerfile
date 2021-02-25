ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# Copy data for add-on
COPY run.sh /home
COPY app.py /home

# Install requirements for add-on
RUN apk add --no-cache python3 py3-pip
RUN pip3 install Flask requests

# Python 3 HTTP Server serves the current working dir
# So let's set it to our add-on persistent data directory.
WORKDIR /data

CMD /home/run.sh
