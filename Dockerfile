FROM almirai/python:3.8.12-alpine
LABEL author="almirai"
LABEL email="live.almirai@outlook.com"
LABEL version="0.1"
LABEL description="Crawler to get tide data."
LABEL name="tide-crawler"
COPY . .
USER root
RUN python -m pip install --no-cache-dir -U -i https://pypi.tuna.tsinghua.edu.cn/simple pip && \
    pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
USER appuser
EXPOSE 8000
ENV LOG_LEVEL=info
CMD gunicorn --config=gunicorn.py app:app
