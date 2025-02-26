FROM python:3.12-alpine3.21

WORKDIR /app
COPY . /app

# Set correct MySQL connection details
ENV DB_PASSWORD=redeemx
ENV DB_USER=redeemx
ENV DB_PASSWORD=redeemx
ENV DB_HOST=redeemx_db
ENV DB_PORT=3306
ENV DB_NAME=redeemx_db

# JWT settings
ENV SECRET_KEY="secret_key"
ENV ALGORITHM="HS256"
ENV ACCESS_TOKEN_EXPIRE_MINUTES=30

RUN apk add --no-cache gcc musl-dev libffi-dev
RUN python -m venv /env
RUN /env/bin/pip install --upgrade pip
RUN /env/bin/pip install -r requirements.txt

EXPOSE 8000
CMD ["/env/bin/python", "src/scripts.py"]
CMD ["/env/bin/python", "src/main.py"]

