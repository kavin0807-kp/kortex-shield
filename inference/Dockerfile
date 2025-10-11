FROM python:3.11-slim

WORKDIR /app
COPY ./app /app/app
COPY ../kortex_model /app/kortex_model

RUN pip install --no-cache-dir fastapi "uvicorn[standard]" torch transformers tokenizers

EXPOSE 9000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9000", "--workers", "1"]
