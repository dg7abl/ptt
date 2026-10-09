#cat > ~/hotas_ptt.py <<'PY'
import socket
import struct
import select
JOYSTICK = "/dev/input/js1"
WINDOWS_IP = "10.10.10.51"
WINDOWS_PORT = 49512
PTT_BUTTON = 0
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
def send(command):
 sock.sendto(command.encode(), (WINDOWS_IP, WINDOWS_PORT))
 if command != "DOWN":
 print(f"PTT {command}", flush=True)
pressed = False
print("HOTAS Warthog PTT bereit - Button 0", flush=True)
try:
 with open(JOYSTICK, "rb", buffering=0) as js:
 while True:
 ready, _, _ = select.select([js], [], [], 0.3)
 if ready:
 event = js.read(8)
 if len(event) != 8:
 break
 timestamp, value, event_type, number = \
 struct.unpack("IhBB", event)
 if event_type & 0x80:
 continue
 if (event_type & 0x7F) != 0x01 or number != PTT_BUTTON:
 continue
 if value and not pressed:
 pressed = True
 print("PTT DOWN", flush=True)
 send("DOWN")
 elif not value and pressed:
 pressed = False
 send("UP")
elif pressed:
 send("DOWN")
except KeyboardInterrupt:
 pass
finally:
 if pressed:
 send("UP")
 sock.close()
PY


# python ~/hotas_ptt.py
