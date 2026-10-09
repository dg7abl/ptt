@'
import socket
import time
from pynput.keyboard import Controller, KeyCode
keyboard = Controller()
ptt_key = KeyCode.from_char("-")
pressed = False
last_signal = 0
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 49512))
sock.settimeout(0.2)
print("PTT-Empfaenger bereit auf UDP 49512", flush=True)
try:
 while True:
 try:
 data, address = sock.recvfrom(64)
 if address[0] != "192.168.178.46":
 continue
 command = data.strip()
 last_signal = time.monotonic()
 if command == b"DOWN" and not pressed:
 keyboard.press(ptt_key)
 pressed = True
 print("PTT gedrueckt (-)", flush=True)
 elif command == b"UP" and press
keyboard.release(ptt_key)
 pressed = False
 print("PTT losgelassen (-)", flush=True)
 except socket.timeout:
 if pressed and time.monotonic() - last_signal > 2:
 keyboard.release(ptt_key)
 pressed = False
 print("PTT automatisch freigegeben", flush=True)
except KeyboardInterrupt:
 pass
finally:
 if pressed:
 keyboard.release(ptt_key)
 sock.close()
'@ | Set-Content "$env:USERPROFILE\ptt_receiver.py" -Encoding UTF8

# "C:\Users\user\AppData\Local\Programs\Python\Python313\python.exe"
#"$env:USERPROFILE\ptt_receiver.py"
