FROM python:3.8

WORKDIR /fsdir

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY run.py .

COPY storage.json .

EXPOSE 53533/udp

CMD ["python", "./run.py"]