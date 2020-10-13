import socket
import threading


def start_server():
   host, port = "192.168.4.1", 5002
   global sock_server
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   s.bind((host, port))
   s.listen(1)
   while True:
      sock_server, sockname = s.accept()
      break


def receiveTCP(sock):
   message = sock.recv(32)
   return message


def stopAlarm():
   print ('Stopping the alarm!!!')


def startAlarm():
   print ('Starting the alarm!!!')


class OrderWaiter(threading.Thread):
   def __init__(self, **kwargs):
      super(OrderWaiter, self).__init__(**kwargs)

   def run(self):
      global sock_server
      while True:
         try:
            message = receiveTCP(sock_server)
         except Exception:
            pass
         else:
            if message != '':
               if message == 'stop alarm':
                  stopAlarm()
               elif message == 'start alarm':
                  startAlarm()
               sock_server.close()
               break

if __name__ == '__main__':
   sock_server = None
   start_server() # pass the host and the port as parameters
   OrderWaiter().start() #start the thread which will wait for the order