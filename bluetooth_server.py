import bluetooth
import socket

hostMACAddress = 'B8:27:EB:48:3A:70' MAC Raspberry PI
port = 12
backlog = 1
size = 1024
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
print('OK')
s.bind((hostMACAddress, port))
s.listen(backlog)

client, clientInfo = s.accept()
data =s.recv(size)
print(data)

client.close()
s.close()