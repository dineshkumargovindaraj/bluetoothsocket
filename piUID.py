import subprocess

def getUID():
        UID = subprocess.check_output(['grep','Serial','/proc/cpuinfo'])
        UID = UID[-17:]
        return UID

if __name__ == '__main__':
        Serial = getUID()
        print Serial