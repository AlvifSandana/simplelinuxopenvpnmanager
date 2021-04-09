import os
import subprocess


def connectVPN(config_name):
   try:
      conf_dir = f"{os.getcwd()}/config_dir"
      filename = f"'{config_name}'"
      current_ip = os.system("curl https://ipinfo.io/ip")
      print(conf_dir)
      # passku = '240800'
      # subprocess.Popen(["echo", passku], stdout=subprocess.PIPE)
      # subprocess.Popen(["sudo", "openvpn", "--config", filename],cwd=conf_dir).communicate(input=b'240800\n')
      os.system(f"sudo openvpn --config {filename}")
      #   while True:
      #       check_ip = str(os.system("curl https://ipinfo.io/ip"))
      #       if current_ip != check_ip:
      #           conn_msg = 'Connected'
      #       else:
      #           conn_msg = 'Not Connected'
   except Exception as error:
      print(error)

# connectVPN("server5-VPNSplit.com.ovpn")

proc = subprocess.Popen(["sudo", "openvpn3" ,"session-start", "--config", "/home/alvif/PycharmProjects/linuxopenvpnmanager/config_dir/server5-VPNSplit.com.ovpn"], stdout=subprocess.PIPE, text=True)
# proc.communicate(input=b'vpnsplit.com-100470492502109\n240800')
