import subprocess as sp

wificredname = 'homeexcept'

sp.call(['sudo','systemctl','stop','dnsmasq'])
sp.call(['sudo','systemctl','stop','hostapd'])

file = open('/etc/dhcpcd.conf','w')
file.write('interface wlan0\n')
file.write('\tstatic ip_address=192.168.4.1/24')
file.close()

sp.call(['sudo','mv','/etc/dnsmasq.conf','/etc/dnsmasq.conf.orig'])

file = open('/etc/dnsmasq.conf','w')
file.write('interface=wlan0\n')
file.write('\tdhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h')
file.close()

file=open('/etc/hostapd/hostapd.conf','w')
file.write('interface=wlan0\n')
file.write('driver=nl80211\n')
file.write('ssid='+wificredname+'\n')
file.write('hw_mode=g\n')
file.write('channel=7\n')
file.write('wmm_enabled=0\n')
file.write('macaddr_acl=0\n')
file.write('auth_algs=1\n')
file.write('ignore_broadcast_ssid=0\n')
file.write('wpa=2\n')
file.write('wpa_passphrase=peaceofmind\n')
file.write('wpa_key_mgmt=WPA-PSK\n')
file.write('wpa_pairwise=TKIP\n')
file.write('rsn_pairwise=CCMP\n')
file.close()

file=open('/etc/default/hostapd','w')
file.write('DAEMON_CONF="/etc/hostapd/hostapd.conf"')
file.close()

sp.call(['sudo','systemctl','start','dnsmasq'])
sp.call(['sudo','systemctl','start','hostapd'])

file =open('/etc/wpa_supplicant/wpa_supplicant.conf','w')
file.close()

file =open('/etc/network/interfaces','w')
file.close()

sp.call(['sudo','systemctl','daemon-reload'])
sp.call(['sudo','service','dhcpcd','restart'])