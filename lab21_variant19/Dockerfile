FROM python:3.12-slim
WORKDIR /app
COPY app ./app
ENV PYTHONPATH=/app
EXPOSE 8000
CMD ["python", "-m", "app.api"]
