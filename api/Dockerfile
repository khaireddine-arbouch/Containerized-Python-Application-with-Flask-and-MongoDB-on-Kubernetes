FROM python:3.11.6

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

ENV MONGO_URI="mongodb://localhost:27017"

CMD ["python", "app.py"]