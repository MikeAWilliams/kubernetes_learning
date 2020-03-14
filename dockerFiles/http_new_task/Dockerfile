FROM python:3

WORKDIR /usr/src/app

COPY new_task_httpServer.py ./ 
RUN pip install --no-cache-dir pika 

CMD [ "python", "./new_task_httpServer.py" ]