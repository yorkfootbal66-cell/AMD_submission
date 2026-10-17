# The app only: it needs no GPU.  The model runs elsewhere, behind the endpoint named in ORDERDESK_MODEL_BASE_URL.
FROM python:3.13-slim
WORKDIR /app
COPY orderdesk ./orderdesk
COPY samples ./samples
ENV ORDERDESK_PORT=8080 ORDERDESK_DATA_DIR=/data PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN useradd --create-home --uid 10001 desk && mkdir /data && chown desk /data
USER desk
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s CMD python -c "import urllib.request,os; urllib.request.urlopen('http://127.0.0.1:%s/healthz' % os.environ['ORDERDESK_PORT'], timeout=4)"
CMD ["python", "-m", "orderdesk.server"]
