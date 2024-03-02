from time import sleep
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST
import platform
import subprocess

def getIP():
    osnm = platform.system()
    if osnm == "Darwin":
        ip = subprocess.check_output("ipconfig getifaddr en0", shell=True).decode("utf-8").strip()
    elif osnm == "Linux":
        ip = subprocess.check_output("hostname -I | awk '{print $1}'", shell=True).decode("utf-8").strip()
    elif osnm == "Windows":
        ip = subprocess.check_output("ipconfig | findstr /i \"ipv4\"", shell=True).decode("utf-8").strip().split(":")[-1].strip()
    return ip

def broadcastConn():
    DATA = "LogIn: "
    PORT = 11200
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind((getIP(), 0))
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    my_ip = getIP()

    while 1:
        data = DATA+my_ip
        data = data.encode()
        s.sendto(data, ('<broadcast>', PORT))
        #print("Sent")
        sleep(1)
