from generategatewayid import GenerateGatewayId
from base64 import b64encode
from hashlib import sha1
import socket
import time
import re

SERVER_ADD = '192.168.4.1'
PORT = 5002

message_wificred = 'wifi-name'
gateway_id,gateway_key=GenerateGatewayId().get_gateway_info()
gateway_cred=gateway_id +','+ gateway_key
message_reboot = 'reboot'

websocket_answer = (
    'HTTP/1.1 101 Switching Protocols',
    'Upgrade: websocket',
    'Connection: Upgrade',
    'Sec-WebSocket-Accept: {key}\r\n\r\n',
)
GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

def listener():
	
	time.sleep(20)
	serverSocket = socket.socket()
	serverSocket.bind((SERVER_ADD,PORT))

    print ('Server Started, Listening For Connections')
	serverSocket.listen(5)
	serverOn = True
	while serverOn:
		clientSocket, clientAddr = serverSocket.accept()
		print ('Connected To:' , clientAddr)
		ledBlink.blink(0)
		text = clientSocket.recv(8192)
		key = (re.search('Sec-WebSocket-Key:\s+(.*?)[\n\r]+', text)
				.groups()[0]
				.strip())
		response_key = b64encode(sha1(key + GUID).digest())
		response = '\r\n'.join(websocket_answer).format(key=response_key)
		print (response)
		clientSocket.send(response)
		
		payload = decode_frame(clientSocket.recv(8192))
		
		if (payload=='True'):
			print ('Adding Gateway')
			time.sleep(5)

			print ('Request wifi name')
			#Encode the message and send it to client
			wificred_res_encoded = encode_frame(message_wificred)
			clientSocket.send(wificred_res_encoded)
			
			#Decode the frame and save the credentials
			wifiCred = decode_frame(clientSocket.recv(8192))
			wifiName,wifiPswd = wifiCred.split(',')
			print (wifiName,wifiPswd)
			time.sleep(5)

			print ('Sending gateway_credentials to client')
			sensor_res_encoded = encode_frame(gateway_cred)
			clientSocket.send(sensor_res_encoded)

			print ('Request for reboot')
			reboot_res_encoded = encode_frame(message_reboot)
			clientSocket.send(reboot_res_encoded)
			confirm = decode_frame(clientSocket.recv(1024))
			if (confirm == 'True'):
				serverOn = False
				wifi_config(wifiName,wifiPswd)
			time.sleep(5)


	serverSocket.close()

	
def wifi_config(wifiname, wifipsk):

	sp.call(['sudo','systemctl','daemon-reload'])
	
	# Update the wpa_supplicant.conf file to add the network provided by the user
	file = open('/etc/wpa_supplicant/wpa_supplicant.conf','w')
	file.write('ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n')
	file.write('update_config=1\n')
	file.write('country=US\n')
	file.write('\n')
	file.write('network={\n')
	file.write('\tssid="'+wifiname+'"\n')
	file.write('\tpsk="'+wifipsk+'"\n')
	file.write('}')
	file.close()

	# Update the interfaces to remove the static IP associated with ad hoc $
	file = open('/etc/network/interfaces','w')
	file.write('source-directory /etc/network/interfaces.d\n')
	file.write('auto wlan0\n')
	file.close()
	
	file = open('/etc/dhcpcd.conf','w')
	file.close()
	subprocess.call(['sudo','service','dhcpcd','restart'])


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
    listener()


				
