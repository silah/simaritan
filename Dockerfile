FROM python:slim

RUN useradd simaritan
WORKDIR /home/simaritan
COPY requirements.txt requirements.txt

RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY simaritan simaritan
COPY migrations migrations
COPY simaritan.py config.py models.py app.db boot.sh ./

RUN chmod +x boot.sh
ENV FLASK_APP simaritan.py

RUN chown -R simaritan:simaritan ./
USER simaritan
EXPOSE 5000


ENTRYPOINT ["./boot.sh"]