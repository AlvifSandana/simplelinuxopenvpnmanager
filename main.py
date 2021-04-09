import eel
import logging
import os
import platform
import subprocess


# initiate eel 
eel.init('web', allowed_extensions=['.js', '.html'])

# expose python functions
@eel.expose
def getSysInfo():
    info = []
    info.append(platform.system())
    info.append(platform.release())
    info.append(getOVPNStatus())
    return info

@eel.expose
def getOVPNStatus():
    check = subprocess.Popen(["which", "openvpn"], stdout=subprocess.PIPE, text=True)
    stdout = check.communicate()[0]
    if check.poll() != 0:
        message = 'Not Installed'
    else:
        message = 'Installed'
    return message

@eel.expose
def getOVPNListFiles():
    try:
        conf_dir = os.getcwd() + '/config_dir'
        list_proc = subprocess.Popen(["find", f"{conf_dir}", "-iname", "*.ovpn"], stdout=subprocess.PIPE, text=True)
        stdout = list_proc.communicate()[0]
        list_conf = stdout.split("/home/alvif/PycharmProjects/linuxopenvpnmanager/config_dir/")
    except Exception as error:
        print(error)
    return list_conf

@eel.expose
def connectVPN(config_name):
    try:
        conf_dir = os.getcwd() + '/config_dir/' + config_name
        current_ip = str(os.system("curl https://ipinfo.io/ip"))
        conn_proc = subprocess.Popen("sudo", "openvpn", "--config", f"'{conf_dir}'", stdout=subprocess.PIPE, text=True)
        while True:
            check_ip = str(os.system("curl https://ipinfo.io/ip"))
            if current_ip != check_ip:
                conn_msg = 'Connected'
            else:
                conn_msg = 'Not Connected'
    except Exception as error:
        print(error)



# run 
if __name__ == '__main__':
    try:
        eel.start('main.html', host='localhost', port=27000, size=(800, 480))
    except Exception as e:
        print(e)
