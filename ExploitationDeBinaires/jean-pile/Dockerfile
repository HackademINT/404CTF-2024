FROM registry.hackademint.org/404-ctf-restore/nsjail:latest

RUN mkdir /app
WORKDIR /app

COPY data/ .

RUN chmod u+x /app/nsjail.sh && \
    chmod u+x /app/jean_pile && \
    chmod u+r /app/flag.txt

EXPOSE 4444

ENTRYPOINT [ "/app/nsjail.sh" ]
CMD [ "/app/jean_pile" ]
