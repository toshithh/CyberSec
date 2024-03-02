import socket
import os

class RecvLogs:
    def __init__(self, ip) -> None:
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip #server ip
        self.port = 11200 # server port

        self.soc.connect((self.ip, self.port))
        self.tasks()
        self.soc.close()
    
    def tasks(self):
        while True:
            cmd = input("Enter Command: ")
            if cmd == "help":
                print(f"\nCommands:\n logFile\n delete\n liveLogs [num]\n delete logfile\n")
            if cmd == "logFile":
                self.soc.sendall(cmd.encode())
                recv = self.soc.recv(10240)
                fl = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Logs.txt")
                fl = open(fl, "wb")
                fl.write(recv)
                fl.close()
                print("Log file downloaded.")
            elif "liveLogs" in cmd:
                try:
                    n = int(cmd.replace("liveLogs", "").strip())
                except:
                    n = float("inf")
                cmd = "liveLogs"
                i = 0
                while i < n:
                    self.soc.sendall(cmd.encode())
                    recv = self.soc.recv(1024).decode()
                    if recv != "< >":
                        print(recv)
                        i+=1
            elif cmd == "exit":
                self.soc.sendall(cmd.encode())
                break
            else:
                self.soc.sendall(cmd.strip().encode())
                recv = self.soc.recv(4096).decode()
                print(recv)

RecvLogs("192.168.105.106")
