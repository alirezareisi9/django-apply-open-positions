FROM python:3.12

WORKDIR /app


COPY req.txt /app
RUN pip install --upgrade pip
RUN pip install -r req.txt
COPY . /app

EXPOSE 8000
ENTRYPOINT [ "python3" ]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] 