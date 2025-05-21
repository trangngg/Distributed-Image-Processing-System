FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Make sure entrypoint.sh executable
RUN chmod +x ./entrypoint.sh

EXPOSE 1300
EXPOSE 5003 5006
ENTRYPOINT ["./entrypoint.sh"]
