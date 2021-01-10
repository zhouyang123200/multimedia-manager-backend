FROM python:3.7

ENV WORK_ENV=PROD
WORKDIR /opt

COPY src ./
COPY requirements.txt ./

RUN pip install -r requirements.txt

CMD ["python" "src/run.py"]
