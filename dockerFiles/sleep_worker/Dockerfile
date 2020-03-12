FROM python:3

WORKDIR /usr/src/app

COPY worker.py ./ 
RUN pip install --no-cache-dir pika 

CMD [ "python", "-u", "./worker.py" ]