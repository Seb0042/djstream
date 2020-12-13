#! /usr/bin/env python3

import bluetooth
import subprocess
import requests
import netifaces as ni



def get_ip_ethernet():
  try:
    ni.ifaddresses('eth0')
    ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
    return ip
  except:
    return None

def get_ip_wifi(blue_comm):
  clist = []
  tlist = []
  command = "wpa_cli -i wlan0 < action_scan  | grep ESS | sort -k 5"
  with subprocess.Popen(["bash","-c",command],stdout=subprocess.PIPE) as proc:
    try:
      l = proc.stdout.read()
    except AttributeError:
      print()
  clist = l.split(b'\n')
  for w in clist:
    u = w.decode().split('\t')
    if u[0] != '':
      tlist += [u[4]]
  i = 0
  for w in tlist:
    blue_comm.send_comm(str(i)+": "+w+'\n')
    i = i + 1 
  blue_comm.send_comm('Enter number\n')
  get = blue_comm.read_comm()
  tn = int(get)
  blue_comm.send_comm('Enter the password\n')
  p = str(blue_comm.read_comm())
  # pour debug
  p = 'pfV4-bgX7jN7JHU<iRC36f *!5c1qztbQyWMJJj_?%U:Q9}3rfdiBoJ9q{gR3ee'
  blue_comm.send_comm('Connecting Wifi: '+tlist[tn]+'\n')
  f = open("action_connect","w")
  f.write("add_network\n")
  f.write("set_network 0 ssid \""+tlist[tn]+"\"\n")
  f.write("set_network 0 psk \""+p+"\"\n")
  f.write("enable_network 0\n")
  f.close()
  command = "wpa_cli -i wlan0 < action_connect"
  with subprocess.Popen(["bash","-c",command],stdout=subprocess.PIPE) as proc:
    try:
      l = proc.stdout.read()
    except AttributeError:
     print()

 
def test_connection():
  r = requests.get('https://www.google.com')
  if r.status_code != 200:
    return False
  else:
    return True

def do_connect(con_type,blue_comm):
  if con_type == 'ethernet':
    get_ip_ethernet()
  elif con_type == 'wifi':
    get_ip_wifi(blue_comm)
  return(test_connection())

class BluetoothComm:
    def __init__(self):
        self.server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        port = 1
        self.server_socket.bind(("",port))
        self.server_socket.listen(1)
        self.client_socket,address = self.server_socket.accept()
        print("Accepted connection from ",address)
        
    def read_comm(self):
        res = self.client_socket.recv(1024)
        if len(res):
            return res
        else:
            return None
 
    def send_comm(self, text):
        self.client_socket.send(text)
        
def main():
    blue_comm = BluetoothComm()
    buff_msg = b''
    blue_comm.send_comm('1 - Wifi\n')
    blue_comm.send_comm('2 - Ethernet\n')
    blue_comm.send_comm('3 - Start streaming\n') 
    while True:
        get = blue_comm.read_comm()
        blue_comm.send_comm(get)
        buff_msg = get
        #p = subprocess.Popen([b'bash',b'-c',buff_msg], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        #shell_out = p.communicate()
        #print('shell:',shell_out)
        print('read:',buff_msg)
        blue_comm.send_comm('\n')
        if buff_msg == b'2':
          blue_comm.send_comm('Activating ethernet interface. Ensure that the box  is connected with a network wire\n')
          r_cnx = do_connect('ethernet')
        elif buff_msg == b'1':
          blue_comm.send_comm('Activating WiFi. Please choose the network\n')
          r_cnx = do_connect('wifi',blue_comm) ):
        if r_cnx:
          blue_comm.send_comm('Connection to Internet Ok')
        else:
          blue_comm.send_comm('Connection to Internet not OK')
                      
main()
