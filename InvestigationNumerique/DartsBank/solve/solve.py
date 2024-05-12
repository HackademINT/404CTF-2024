from pyshark import FileCapture
from sys import argv
from json import loads
from base64 import b64decode

with open(argv[2]) as f:
    key = loads(f.read())


packets = FileCapture(argv[1], display_filter='http.request.method=="POST"')

for packet in packets:
    if not "HTTP" in packet:
        continue
    http = packet["HTTP"]
    data = "".join(http.file_data.split(':'))
    data = bytes.fromhex(data).decode('ascii')
    data = bytearray(b64decode(data))
    for i in range(len(data)):
        data[i] ^= key[i % len(key)]
    data = data.decode('ascii')
    print(data, end="")
