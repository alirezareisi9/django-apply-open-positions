FROM python:3.12


# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1  # Avoids .pyc files
ENV PYTHONUNBUFFERED 1  # shows logs in real time


# Set working directory inside the container
WORKDIR /code
# the directory in which your application code runs and where commands 
#  are executed. It serves as a default directory for all subsequent 
#  commands, meaning that any relative paths specified in the commands 
#  will be relative to this directory.


COPY requirements.txt /code
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /code

EXPOSE 8000

# Default command: Django dev server: Run when start a container from image
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

