FROM python:3.12-slim
WORKDIR /app
COPY app.py .
ENV PORT=8000
EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"
CMD ["python", "app.py"]
