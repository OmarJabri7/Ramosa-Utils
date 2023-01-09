# Set base image (host OS)
FROM python:3.8.13

# By default, listen on port 8080
EXPOSE 8080/tcp

# Install any dependencies
RUN pip install Flask==2.2.2 numpy==1.23.3 pandas==1.4.4 names XlsxWriter requests parsel httpx selectorlib

# Copy the content of the local src directory to the working directory
COPY app.py ./

COPY utils utils

COPY templates templates

# Specify the command to run on container start
CMD [ "python", "./app.py" ]