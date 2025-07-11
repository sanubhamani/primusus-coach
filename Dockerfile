FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 10000

CMD ["uvicorn", "coach_api:app", "--host", "0.0.0.0", "--port", "10000"]
# trigger full rebuild
