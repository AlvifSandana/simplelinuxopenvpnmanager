import eel
import os
import platform
import requests
import subprocess

# initiate eel
eel.init('web', allowed_extensions=['.js', '.html'])


# expose python functions
# get system info
@eel.expose
def getsysinfo():
    info = [platform.system(), platform.release(), getovpnstatus()]
    return info


# get openvpn installation status
@eel.expose
def getovpnstatus():
    check = subprocess.Popen(["which", "openvpn"], stdout=subprocess.PIPE, text=True)
    result = check.communicate()[0]
    if check.poll() != 0:
        message = 'Not Installed'
    else:
        message = f'Installed'
    return message


# get list of the openvpn config files name
@eel.expose
def getovpnlistfiles():
    global list_conf
    try:
        conf_dir = os.getcwd() + '/config_dir'
        list_proc = subprocess.Popen(["find", f"{conf_dir}", "-iname", "*.ovpn"], stdout=subprocess.PIPE, text=True)
        stdout = list_proc.communicate()[0]
        list_conf = stdout.split(conf_dir + '/')
    except Exception as error:
        print(error)
    return list_conf


@eel.expose
def connectvpn(config_name):
    pass


@eel.expose
def checkpublicip():
    try:
        url = 'https://ipapi.co/json'
        request = requests.get(url)
        ip_info = request.json()
        result = [ip_info['ip'], ip_info['country_name'], 'connected']
        if ip_info != '' or ip_info is not None:
            return result
        else:
            return ['127.0.0.1', 'unavailable', 'unavailable']
    except Exception as error:
        print(error)


# run
if __name__ == '__main__':
    try:
        eel.start('main_app.html', host='localhost', port=27000, size=(1000, 480))
    except Exception as e:
        print(e)
