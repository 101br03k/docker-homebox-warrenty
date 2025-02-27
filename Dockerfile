FROM python:3.13.2-slim

RUN mkdir /
WORKDIR /
ADD . /
RUN pip install -r requirements.txt

EXPOSE 42069
CMD ["python", "/api.py"]