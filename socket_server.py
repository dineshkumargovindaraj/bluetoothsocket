import socket
import time
import struct
import sys
import re
import test_internet
from base64 import b64encode
from hashlib import sha1
import subprocess as sp
import os

SERVER_ADD = '192.168.4.1'
PORT = 5002

message_wificred = 'wifi-name'
message_reboot = 'Reboot'
GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

websocket_answer = (
    'HTTP/1.1 101 Switching Protocols',
    'Upgrade: websocket',
    'Connection: Upgrade',
    'Sec-WebSocket-Accept: {key}\r\n\r\n',
)

find_socket_cmd = 'ps aux | grep sensorServer | grep -v grep'
close_socket_cmd = 'kill -9 {0}'
up_time_cmd = 'ifconfig | grep wlan0'

global clientSocket
global serverSocket


def find_and_close_socket():

    output = sp.check_output(find_socket_cmd, shell=True)
    processes = output.split('\n')
    this_id = os.getpid()
    for process in processes:
        if 'grep' in process.split():
            continue
        if process == '':
            continue
        id = process.split()[1]
        if id == str(this_id):
            continue
        sp.call(close_socket_cmd.format(id.strip()), shell=True)


def connection():
    global clientSocket
    global serverSocket

    find_and_close_socket()
    serverSocket = socket.socket()
   
    # Set linger to 0 so socket dies quicker after shutdown
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 0))

    try:
        serverSocket.bind((SERVER_ADD, PORT))
    except:
        print("Socket already open, waiting for close")
        time.sleep(5)
        serverSocket.bind((SERVER_ADD, PORT))

    serverSocket.listen(5)
    while True:
        clientSocket, clientAddr = serverSocket.accept()
        text = clientSocket.recv(8192)
        key = (re.search('Sec-WebSocket-Key:\s+(.*?)[\n\r]+', text)
               .groups()[0]
               .strip())
        response_key = b64encode(sha1(key + GUID).digest())
        response = '\r\n'.join(websocket_answer).format(key=response_key)
        clientSocket.send(response)
        payload = decode_frame(clientSocket.recv(8192))
        if payload == 'True':
            add_sensor()


def add_sensor():
    global clientSocket

    # Encode the message and send it to client
    wificred_res_encoded = encode_frame(message_wificred)
    clientSocket.send(wificred_res_encoded)

    # Decode the frame and save the credentials
    wificred = decode_frame(clientSocket.recv(8192))
    wifi_name, wifi_pwd = wificred.split(',')
	print("wifi credentials ----",wifi_name, wifi_pwd)

    sensor_id = 'homeexcept'
    sensor_res_encoded = encode_frame(sensor_id)
    clientSocket.send(sensor_res_encoded)

    reboot_res_encoded = encode_frame(message_reboot)
    clientSocket.send(reboot_res_encoded)
    confirm = decode_frame(clientSocket.recv(1024))
    if confirm == 'True':
        serverSocket.close()
        wifi_connect(wifi_name, wifi_pwd)


def wifi_connect(wifi_name, wifi_pwd):
    wifi_connect_count = 0
    valid_connection = False
    while not valid_connection:
        if wifi_connect_count == 0:
            sp.call(['nmcli', "connection", "down", "hotspot"])
            time.sleep(5)
            sp.call(["sudo", "nmcli", "dev", "wifi", "connect", str(wifi_name), "password", str(wifi_pwd), 'ifname',
                     'wlan0'])
            time.sleep(5)
            valid_connection = test_internet.test()

        elif 1 <= wifi_connect_count <= 3:
            sp.call(['nmcli', 'con', 'delete', str(wifi_name)])
            sp.call(["sudo", "nmcli", "dev", "wifi", "connect", str(wifi_name), "password", str(wifi_pwd), 'ifname',
                     'wlan0'])
            time.sleep(5)
            valid_connection = test_internet.test()

        else:
            sp.call(['nmcli', 'con', 'delete', str(wifi_name)])
            time.sleep(15)
            sp.call(['nmcli', "connection", "up", "hotspot"])
            print ("Restart socket service...")
            sys.exit()

        wifi_connect_count = wifi_connect_count + 1

    if valid_connection:
        print ("Wifi credentials matched...")

    print ("Disable socket service...")
    print ("Stop socket service...")

    sys.exit()


def change_host_name():
    file = open('/etc/hosts', 'w')
    file.write('127.0.0.1\tlocalhost\n')
    file.write('127.0.0.1\thomeexcept\n')
    file.close()
    file = open('/etc/hostname', 'w')
    file.write('homeexcept')
    file.close()
    sp.call(['sudo', 'hostname', 'homeexcept'])


def create_hotspot():

    id = 'homeexcept'
    sp.call(["nmcli", "device", "wifi", "hotspot", "con-name", "hotspot", "ssid", id, "band", "bg",
             "password", "hex1234"])
    sp.call(["nmcli", "connection", "modify", 'hotspot', "ipv4.addresses", "192.168.4.1/24"])
    change_host_name()


def check_up_time():
    while True:
        try:
            up_time = sp.check_output(up_time_cmd, shell=True)
            if not up_time == '':
                return
        except:
            time.sleep(10)
            sp.call(['sudo', 'nmcli', 'r', 'wifi', 'on'])
            return


def decode_frame(result):
    frame = bytearray(result)
    payload_len = frame[1]-128
    mask = frame[2:6]
    encrypted_payload = frame[6:6+payload_len]
    payload = bytearray([encrypted_payload[i] ^ mask[i % 4] for i in range(payload_len)])
    return payload


def encode_frame(message):
    send_frame = [129]
    send_frame += [len(message)]
    frame_to_send = bytearray(send_frame)+message
    return frame_to_send


if __name__ == "__main__":
    check_up_time()
    if os.path.isfile('/etc/NetworkManager/system-connections/hotspot'):
        sp.call(["sudo", "rm", "/etc/NetworkManager/system-connections/hotspot"])
    time.sleep(10)
    create_hotspot()
    sp.call(["nmcli", "connection", "down", "hotspot"])
    time.sleep(5)
    sp.call(["nmcli", "connection", "up", "hotspot"])
    connection()