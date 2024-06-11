FROM python:latest
WORKDIR /app
COPY . .
RUN pip3 -r install requirements.txt
CMD [ "python3", "app.py" ]