from socket import socket, AF_INET, SOCK_DGRAM
import platform, subprocess

def getIP():
    osnm = platform.system()
    if osnm == "Darwin":
        ip = subprocess.check_output("ipconfig getifaddr en0", shell=True).decode("utf-8").strip()
    elif osnm == "Linux":
        ip = subprocess.check_output("hostname -I | awk '{print $1}'", shell=True).decode("utf-8").strip()
    elif osnm == "Windows":
        ip = subprocess.check_output("ipconfig | findstr /i \"ipv4\"", shell=True).decode("utf-8").strip().split(":")[-1].strip()
    return ip


s = socket(AF_INET, SOCK_DGRAM)
PORT = 11200
s.bind(('', PORT))

DATA = "LogIn"

while 1:
    data, addr = s.recvfrom(1024)
    if data.decode().startswith(DATA):
        print(data, addr, sep="\n", end="\n\n")