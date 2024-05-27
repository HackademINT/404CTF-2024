FROM python:3.11-slim

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY api api
COPY fl fl

USER 65534:65534

EXPOSE 8000

CMD ["python", "-m", "api.main"]