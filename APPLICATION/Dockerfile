FROM python:3.9-slim-bullseye

WORKDIR /app

RUN python3 -m venv /opt/venv

COPY requirements.txt ./

ENV PATH=/opt/venv/bin:$PATH

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

EXPOSE 4000

ENV PATH=/opt/venv/bin:$PATH
CMD [ "flask", "run","--host=0.0.0.0","--port","4000"]