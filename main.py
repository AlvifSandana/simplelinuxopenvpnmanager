import eel
import os
import platform
import requests
import subprocess

# initiate eel
eel.init('web', allowed_extensions=['.js', '.html'])


# expose python functions
@eel.expose
def getsysinfo():
    info = [platform.system(), platform.release(), getovpnstatus()]
    return info


@eel.expose
def getovpnstatus():
    check = subprocess.Popen(["which", "openvpn"], stdout=subprocess.PIPE, text=True)
    result = check.communicate()[0]
    if check.poll() != 0:
        message = 'Not Installed'
    else:
        message = f'Installed ({result})'
    return message


@eel.expose
def getovpnlistfiles():
    global list_conf
    try:
        conf_dir = os.getcwd() + '/config_dir'
        list_proc = subprocess.Popen(["find", f"{conf_dir}", "-iname", "*.ovpn"], stdout=subprocess.PIPE, text=True)
        stdout = list_proc.communicate()[0]
        list_conf = stdout.split('/home/alvif/PycharmProjects/linuxopenvpnmanager/config_dir/')
    except Exception as error:
        print(error)
    return list_conf


@eel.expose
def connectvpn(config_name):
    # global conn_msg
    # try:
    #     conf_dir = os.getcwd() + '/config_dir/' + config_name
    #     current_ip = str(os.system("curl https://ipinfo.io/ip"))
    #     conn_proc = subprocess.Popen(["sudo", "openvpn", "--config", f"'{conf_dir}'"],
    #                                  stdout=subprocess.PIPE, text=True)
    #     while True:
    #         check_ip = str(os.system("curl https://ipinfo.io/ip"))
    #         if current_ip != check_ip:
    #             conn_msg = 'Connected'
    #         else:
    #             conn_msg = 'Not Connected'
    # except Exception as error:
    #     print(error)
    # return conn_msg
    pass


@eel.expose
def checkpublicip():
    try:
        url = 'https://ipinfo.io/ip'
        request = requests.get(url)
        ip_addr = request.text
        if ip_addr != '' or ip_addr is not None:
            return ip_addr
        else:
            return '127.0.0.1'
    except Exception as error:
        print(error)


# run
if __name__ == '__main__':
    try:
        eel.start('main.html', host='localhost', port=27000, size=(800, 480))
    except Exception as e:
        print(e)
