import socket
import time
import subprocess
import ledBlink
import wifiConfig
import piUID
import rebootConfig
import re
from base64 import b64encode
from hashlib import sha1

SERVER_ADD = '192.168.4.1'
PORT = 5002

message_wificred = 'wifi-name'
message_connectionString = 'ConnectionString'
SENSOR_ID = piUID.getUID()
message_reboot = 'Reboot'

websocket_answer = (
    'HTTP/1.1 101 Switching Protocols',
    'Upgrade: websocket',
    'Connection: Upgrade',
    'Sec-WebSocket-Accept: {key}\r\n\r\n',
)
GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

def connection():
        time.sleep(20)
        serverSocket = socket.socket()
        serverSocket.bind((SERVER_ADD,PORT))

        print 'Server Started, Listening For Connections'
        serverSocket.listen(5)
        serverOn = True
        while serverOn:
                clientSocket, clientAddr = serverSocket.accept()
                print 'Connected To:' , clientAddr
                ledBlink.blink(0)
                text = clientSocket.recv(8192)
                key = (re.search('Sec-WebSocket-Key:\s+(.*?)[\n\r]+', text)
                        .groups()[0]
                        .strip())
                response_key = b64encode(sha1(key + GUID).digest())
                response = '\r\n'.join(websocket_answer).format(key=response_key)
                print response
                clientSocket.send(response)
                
                payload = decode_frame(clientSocket.recv(8192))
                
                if (payload=='True'):
                        print 'Adding Sensor'
                        time.sleep(5)

                        print 'Request wifi name'
                        #Encode the message and send it to client
                        wificred_res_encoded = encode_frame(message_wificred)
                        clientSocket.send(wificred_res_encoded)
                        
                        #Decode the frame and save the credentials
                        wifiCred = decode_frame(clientSocket.recv(8192))
                        wifiName,wifiPswd = wifiCred.split(',')
                        print wifiName,wifiPswd
                        time.sleep(5)

                        print 'Sending sensor id to client'
                        sensor_res_encoded = encode_frame(SENSOR_ID)
                        clientSocket.send(sensor_res_encoded)


                        print 'Request for reboot'
                        reboot_res_encoded = encode_frame(message_reboot)
                        clientSocket.send(reboot_res_encoded)
                        confirm = decode_frame(clientSocket.recv(1024))
                        if (confirm == 'True'):
                                serverOn = False
                                rebootConfig.config()
                                wifiConfig.newConfig(wifiName,wifiPswd)
                        time.sleep(5)


        serverSocket.close()

def decode_frame(result):
        frame = bytearray(result)
        payload_len = frame[1]-128
        mask = frame[2:6]
        encrypted_payload = frame[6:6+payload_len]
        payload=bytearray([encrypted_payload[i]^mask[i%4] for i in range(payload_len)])
        return payload

def encode_frame(message):
        sendframe = [129]
        sendframe +=[len(message)]
        frame_to_send = bytearray(sendframe)+message
        return frame_to_send
    
if __name__=="__main__":
        connection()


				
