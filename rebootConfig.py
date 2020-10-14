import subprocess as sp
def config():
        sp.call(['sudo','systemctl','daemon-reload'])
        #sp.call(['sudo','systemctl','disable','socketserver.service'])
        #sp.call(['sudo','systemctl','enable','connection.service'])
        

if __name__ == '__main__':
        config()
