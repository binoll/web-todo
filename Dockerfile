FROM python:3.11-slim

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY src /src
COPY web /web

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--reload", "--port", "80"]