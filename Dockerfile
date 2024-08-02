# Use an official lightweight Python runtime as a parent image
# FROM python:3.8-alpine
FROM python:3.8.10
# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
 
# Set the working directory in the container
WORKDIR /app
 
# Copy the current directory contents into the container at /app
COPY . /app
 
 
COPY ./requirements.txt .
 
RUN pip install -r requirements.txt
RUN pip install djangorestframework-simplejwt
 
 
CMD ["python", "manage.py", "runserver", "0.0.0.0:9001"]