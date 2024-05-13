import socket

from dataclasses import dataclass
from struct import pack, unpack
from threading import Lock
from typing import Any, Callable, Iterator, Unpack


MAX_FRAME_TLV_COUNT = 1000


@dataclass
class TLV:
    type: int
    # No needs to store the length, it's len(bytes) + 4
    value: bytes

    def encode(self):
        return pack(r'>HH', self.type, len(self)) + self.value

    def __len__(self):
        return len(self.value) + 4  # Two bytes for types and two bytes for length


@dataclass
class FrameStart:
    frame_type: int
    frame_sequence: int


@dataclass
class FrameEnd:
    frame_sequence: int


class Codec:
    _encoders: dict[type, Callable] = {}
    _decoders: dict[int, Callable] = {}
    _frame_classes: dict[int, type] = {}
    _frame_ids: dict[type, int] = {}

    @staticmethod
    def encoder(type_: type):
        def decorator(func):
            Codec._encoders[type_] = func
            return func
        return decorator

    @staticmethod
    def decoder(discriminator: int):
        def decorator(func):
            Codec._decoders[discriminator] = func
            return func
        return decorator

    @staticmethod
    def frame(discriminator):
        def decorator(clazz):
            Codec._frame_classes[discriminator] = clazz
            Codec._frame_ids[clazz] = discriminator
            return clazz
        return decorator

    def encode_data(self, data: Any) -> TLV:
        encoder = Codec._encoders.get(type(data))
        if encoder is None:
            raise NotImplementedError(f"Unsupported type: {type(data)}")
        return encoder(data)

    def decode_tlv(self, tlv: TLV) -> Any:
        decoder = Codec._decoders.get(tlv.type)
        if decoder is None:
            raise NotImplementedError(f"Unknown TLV discriminator: {tlv.type}")
        return decoder(tlv)

    def encode_frame(self, frame: Any, sequence: int) -> Iterator[TLV]:
        frame_type = Codec._frame_ids.get(type(frame))
        if frame_type is None:
            raise NotImplementedError(f"Unknown frame type: {type(frame)}")
        yield self.encode_data(FrameStart(frame_type, sequence))
        annotations = frame.__annotations__ if "__annotations__" in dir(frame) else {}
        for field, type_ in annotations.items():
            value = getattr(frame, field)
            encoder = Codec._encoders.get(type_)
            if encoder is None:
                raise NotImplementedError(f"Unsupported data type: {type_}")
            yield encoder(value)
        yield self.encode_data(FrameEnd(sequence))

    def decode_frame(self, *tlvs: Unpack[TLV]):
        if len(tlvs) < 2:
            raise ValueError(f"Frame must have at least two TLVs, found only {len(tlvs)}")
        start, end = tlvs[0], tlvs[-1]
        start = self.decode_tlv(start)
        end = self.decode_tlv(end)
        if not isinstance(start, FrameStart):
            raise TypeError(f"First TLV in frame is expected to be FrameStart, not {type(start)}")
        if not isinstance(end, FrameEnd):
            raise TypeError(f"Last TLV in frame is expected to be FrameEnd, not {type(end)}")
        if start.frame_sequence != end.frame_sequence:
            raise ValueError(f"Frame start and end TLV sequence numbers are not matching: {start.frame_sequence} != {end.frame_sequence}")
        clazz = Codec._frame_classes.get(start.frame_type)
        if clazz is None:
            raise ValueError(f"Unknown frame identifier: {start.frame_type}")
        return clazz(*(self.decode_tlv(tlv) for tlv in tlvs[1:-1]))


@Codec.encoder(FrameStart)
def encode_frame_start(start: FrameStart) -> TLV:
    return TLV(0x00, pack(r'>HH', start.frame_type, start.frame_sequence))


@Codec.decoder(0x00)
def decode_frame_start(tlv: TLV) -> FrameStart:
    return FrameStart(*unpack(r'>HH', tlv.value))


@Codec.encoder(FrameEnd)
def encode_frame_end(end: FrameEnd) -> TLV:
    return TLV(0x01, pack(r'>H', end.frame_sequence))


@Codec.decoder(0x01)
def decode_frame_end(tlv: TLV) -> FrameEnd:
    return FrameEnd(unpack(r'>H', tlv.value)[0])


@Codec.encoder(int)
def encode_int(value: int) -> TLV:
    return TLV(0x10, pack(r'>i', value))


@Codec.decoder(0x10)
def decode_int(tlv: TLV) -> int:
    return unpack(r'>i', tlv.value)[0]


@Codec.encoder(float)
def encode_float(value: float) -> TLV:
    return TLV(0x18, pack('>d', value))


@Codec.decoder(0x18)
def decode_float(tlv: TLV) -> float:
    return unpack(r'>d', tlv.value)[0]


@Codec.encoder(bytes)
@Codec.encoder(bytearray)
def encode_bytes(data: bytes | bytearray) -> TLV:
    return TLV(0x20, data)


@Codec.decoder(0x20)
def decode_bytes(tlv: TLV) -> bytes:
    return tlv.value


@Codec.encoder(str)
def encode_string(data: str) -> TLV:
    encoded = data.encode('utf-8')
    return TLV(0x30, encoded)


@Codec.decoder(0x30)
def decode_string(tlv: TLV) -> str:
    return tlv.value.decode('utf-8')


@Codec.encoder(bool)
def encode_bool(data: bool) -> TLV:
    return TLV(0x40, b'T' if data else b'F')


@Codec.decoder(0x40)
def decode_bool(tlv: TLV) -> bool:
    match tlv.value:
        case b'T':
            return True
        case b'F':
            return False
        case _:
            raise ValueError(f"Invalid boolean bytes: {tlv.value}")


@Codec.frame(0x00)
@dataclass
class PingFrame:
    when: float


@Codec.frame(0x01)
@dataclass
class PongFrame:
    when: float


@Codec.frame(0x10)
@dataclass
class SystemInfoFrame:
    system: str
    hostname: str
    release: str
    version: str
    machine: str


@Codec.frame(0x11)
class SystemInfoRequestFrame:
    pass


@Codec.frame(0x20)
class DieRequestFrame:
    pass


@Codec.frame(0x30)
@dataclass
class ProcessStartRequestFrame:
    command: str
    request_id: int


@Codec.frame(0x31)
@dataclass
class ProcessStartedFrame:
    command: str
    pid: int
    request_id: int


@Codec.frame(0x32)
@dataclass
class ProcessPipeFrame:
    pid: int
    descriptor: int
    data: bytes


@Codec.frame(0x33)
@dataclass
class ProcessTerminatedFrame:
    pid: int
    status: int


@Codec.frame(0x40)
@dataclass
class FileDownloadRequestFrame:
    request_id: int
    file: str
    chunk_size: int


@Codec.frame(0x42)
@dataclass
class FileTransferStartFrame:
    request_id: int
    filename: str
    size: int


@Codec.frame(0x43)
@dataclass
class FileTransferDataFrame:
    request_id: int
    data: bytes


@Codec.frame(0x44)
@dataclass
class FileTransferCompleteFrame:
    request_id: int


@Codec.frame(0x45)
@dataclass
class FileTransferFailFrame:
    request_id: int


class ProtocolSession:
    _sock: socket.socket
    _lock: Lock
    _codec: Codec
    __sequence: int
    __handlers = {}

    def __init__(self, sock: socket.socket):
        self._sock = sock
        self._codec = Codec()
        self.__sequence = 0
        self._lock = Lock()

    def send(self, frame: Any):
        self._lock.acquire(blocking=True)
        for tlv in self._codec.encode_frame(frame, self.__sequence):
            self._sock.send(tlv.encode())
            self.__sequence += 1
        self._lock.release()

    def receive(self) -> Any:
        tlvs = []
        for _ in range(MAX_FRAME_TLV_COUNT):
            tlv = self._receive_tlv()
            if tlv is None:
                return None
            tlvs.append(tlv)
            if tlv.type == 0x01:  # TLV end
                break
        else:
            self._lock.release()
            raise ValueError("Received too many TLVs for a single frame")
        frame = self._codec.decode_frame(*tlvs)
        return frame

    def _receive_tlv(self) -> TLV | None:
        tlv_header = self._sock.recv(4)
        if len(tlv_header) == 0:
            return None
        tlv_type, tlv_length = unpack(r'>HH', tlv_header)
        tlv_value = self._sock.recv(tlv_length - 4)  # We already got the header
        if len(tlv_value) == 0:
            return None
        return TLV(tlv_type, tlv_value)

    def run(self):
        while True:
            frame = self.receive()
            if frame is None:
                break
            handler = self.__handlers.get(type(frame))
            if handler is None:
                print(f"Unsupported frame: {frame}")
                continue
            handler(frame, self)

    def handler(self, clazz):
        def decorator(func):
            self.__handlers[clazz] = func
            return func

        return decorator

    @property
    def address(self) -> tuple[str, int]:
        return self._sock.getpeername()





