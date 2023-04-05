FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir /app/sdq
EXPOSE 80
CMD [ "gunicorn", "-w", "1", "-b", "0.0.0.0:80", "sdq.src.wsgi:app"]