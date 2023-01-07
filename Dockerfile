FROM python:latest
COPY . /
EXPOSE 8888
WORKDIR files/lib
RUN pip install -r ../../requirements.txt
CMD python network_site.py
CD ../../
CMD python -m http.server