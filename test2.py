import subprocess as sp

wificredname = 'homeexcept'

file = open('/etc/dhcpcd.conf','w')
file.write('denyinterfaces wlan0')
file.close()

file = open('/etc/network/interfaces','w')
file.write('auto lo\n')
file.write('iface lo inet loopback\n\n')
file.write('auto eth0\n')
file.write('iface eth0 inet dhcp\n\n')
file.write('allow-hotplug wlan0\n')
file.write('iface wlan0 inet static\n')
file.write('\taddress 192.168.4.1\n')
file.write('\tnetmask 255.255.255.0\n')
file.write('\tnetwork 192.168.4.0\n')
file.write('\tbroadcast 192.168.4.255')
file.close()


file=open('/etc/hostapd/hostapd.conf','w')
file.write('interface=wlan0\n')
file.write('driver=nl80211\n')
file.write('ssid='+wificredname+'\n')
file.write('hw_mode=g\n')
file.write('channel=6\n')
file.write('ieee80211n=1\n')
file.write('wmm_enabled=1\n')
file.write('ht_capab=[HT40][SHORT-GI-20][DSSS_CCK-40]\n')
file.write('macaddr_acl=0\n')
file.write('auth_algs=1\n')
file.write('ignore_broadcast_ssid=0\n')
file.write('wpa=2\n')
file.write('wpa_key_mgmt=WPA-PSK\n')
file.write('wpa_passphrase=peaceofmind\n')
file.write('rsn_pairwise=CCMP')
file.close()

file=open('/etc/default/hostapd','w')
file.write("DAEMON_CONF='/etc/hostapd/hostapd.conf'")
file.close()


file = open('/etc/dnsmasq.conf','w')
file.write('interface=wlan0\n')
file.write('listen-address=192.168.4.1\n')
file.write('bind-interfaces\n')
file.write('server=8.8.8.8\n')
file.write('domain-needed\n')
file.write('bogus-priv\n')
file.write('dhcp-range=192.168.4.2,192.168.4.20,24h')
file.close()

print ('done!')