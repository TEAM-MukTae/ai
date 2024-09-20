FROM python:3.10

ENV PYTHONUNBUFFERED=1

COPY . /Muktae
WORKDIR /Muktae

ADD requirements.txt /Muktae/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]