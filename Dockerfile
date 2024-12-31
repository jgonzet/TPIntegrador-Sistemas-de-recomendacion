FROM python:3.11.9-slim
COPY . .
RUN pip3 install -r requirements.txt
CMD ["flask","--app","app.py","run","--host=0.0.0.0"]

  