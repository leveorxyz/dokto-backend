FROM python:3.9-slim-bullseye
WORKDIR /Dokto-Backend
COPY . .
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
RUN cp example.env .env
RUN pip install -r requirements.txt
RUN pip install wheel
RUN pip install psycopg2-binary
RUN python manage.py migrate

# Run the application:
CMD ["python", "manage.py","runserver", "0.0.0.0:80"]
