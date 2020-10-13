import bluetooth
import socket

# Windows MAC
bd_addr = "90:61:AE:92:13:3B" 
port = 1
sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))
 
trame_envoi_1= [0x7E, 0x7E, 0x73, 0x02, 0x73, 0x02]

for i in trame_envoi_1:
    sock.send(bytes(i))
    print(hex(i))

trame_recue=[]
i=0
while i<9:
    x=sock.recv(1)
    trame_recue.append(ord(x))
    i=i+1
print ('Trame_recue = ',trame_recue)