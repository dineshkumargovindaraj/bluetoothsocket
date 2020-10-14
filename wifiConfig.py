import subprocess

def newConfig(wifiname, wifipsk):
        # Update the wpa_supplicant.conf file to add the network provided by th$
        file = open('/etc/dhcpcd.conf','w')
        file.close()
        subprocess.call(['sudo','service','dhcpcd','restart'])
        
        file = open('/etc/wpa_supplicant/wpa_supplicant.conf','w')
        file.write('ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n')
        file.write('update_config=1\n')
        file.write('\n')
        file.write('network={\n')
        file.write('\tssid="'+wifiname+'"\n')
        file.write('\tpsk="'+wifipsk+'"\n')
        # file.write('\tkey_mgmt=WPA-PSK\n')
        file.write('}')
        file.close()

        # Update the interfaces to remove the static IP associated with ad hoc $
        file = open('/etc/network/interfaces','w')
        file.write('source-directory /etc/network/interfaces.d\n')
        file.write('auto wlan0\n')
        file.close()

        subprocess.call(['sudo','reboot'])

if __name__=="__main__":
        newConfig('T4GGuest','ILoveT4G')
        subprocess.call(['sudo','reboot'])
