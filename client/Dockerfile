FROM python:3.6


RUN pip install python-telegram-bot --upgrade
RUN pip install requests

COPY . /app

WORKDIR /app

EXPOSE 12341

CMD ["python", "telegram_client.py"]
