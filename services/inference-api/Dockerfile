FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
RUN groupadd --gid 10001 aegis && useradd --uid 10001 --gid 10001 --no-create-home --shell /usr/sbin/nologin aegis
COPY services/inference-api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY services/inference-api/app ./app
COPY model ./model
RUN chown -R aegis:aegis /app
USER 10001:10001
EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
