FROM python:3.9-slim

RUN apt update && apt install -y curl

ADD requirements.txt /app/
RUN python3 -m pip install -r /app/requirements.txt

ADD api.py /app/
WORKDIR /app/


HEALTHCHECK --interval=10s --timeout=5s CMD ["curl","-s","127.0.0.1:5000/health"]

CMD ["python3","/app/api.py"]
