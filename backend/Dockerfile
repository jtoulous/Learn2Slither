FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN apt-get update
RUN apt-get install sqlite3
RUN pip install -r requirements.txt
RUN pip install 'uvicorn[standard]'


#CMD ["tail", "-f", "/dev/null"]
CMD ["python", "backend.py", "run_dev"]