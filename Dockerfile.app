FROM python:3.10

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=safarbazi_project.settings

# Create and set the working directory
RUN mkdir /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY /safarbazi_project/. /app
COPY ./requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

COPY ./entrypoint.sh /

ENTRYPOINT ["sh", "/entrypoint.sh"]

