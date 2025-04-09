FROM python:3.13.3-slim

RUN mkdir /
WORKDIR /
ADD . /
RUN pip install -r requirements.txt

EXPOSE 42069
CMD ["python", "/api.py"]