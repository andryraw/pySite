FROM python:3.10.8-alpine

RUN adduser -D pysite

WORKDIR /home/pysite

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY main.py config.py .gitignore boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP main.py

RUN chown -R pysite:pysite ./
USER pysite

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]