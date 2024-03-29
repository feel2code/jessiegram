FROM python:3.11
LABEL authors="feliks"
RUN mkdir /jessiegram
COPY requirements.txt /jessiegram
RUN pip3 install -r /jessiegram/requirements.txt --no-cache-dir
COPY jessiegram/ /jessiegram
WORKDIR /jessiegram
RUN python3 manage.py migrate
CMD ["python3", "manage.py", "runserver", "0:8000"]
