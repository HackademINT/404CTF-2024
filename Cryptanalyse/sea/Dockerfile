FROM python:3.11


#adduser ctf --disabled-password --gecos "" --shell /usr/sbin/nologin && \

RUN apt update && \
    apt install -y socat && \
    apt install -y pip && \
    python3 -m pip install --upgrade pip

RUN mkdir /home/ctf

COPY requirements.txt /home/ctf/
COPY sea.py flag.py solve.py /home/ctf/
WORKDIR /home/ctf/

RUN pip install --requirement /home/ctf/requirements.txt

USER 65534:65534

EXPOSE 4000

CMD bash -c "socat tcp-listen:4000,reuseaddr,fork exec:'timeout -s KILL 4200 python3 /home/ctf/sea.py'"