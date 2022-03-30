from UCASSrunLogin.LoginManager import LoginManager

import requests
import time
import getpass
    
def get_func(url, *args, **kwargs):
    resp = requests.get(url, *args, **kwargs)
    return resp.text

def post_func(url, data, *args, **kwargs):
    resp = requests.post(url, data=data, *args, **kwargs)
    return resp.text

def time2date(timestamp):
    time_arry = time.localtime(int(timestamp))
    return time.strftime('%Y-%m-%d %H:%M:%S', time_arry)

def humanable_bytes(num_byte):
    num_byte = float(num_byte)
    num_GB, num_MB, num_KB = 0, 0, 0
    if num_byte >= 1024**3:
        num_GB = num_byte // (1024**3)
        num_byte -= num_GB * (1024**3)
    if num_byte >= 1024**2:
        num_MB = num_byte // (1024**2)
        num_byte -= num_MB * (1024**2)
    if num_byte >= 1024:
        num_KB = num_byte // 1024
        num_byte -= num_KB * 1024
    return '{} GB {} MB {} KB {} B'.format(num_GB, num_MB, num_KB, num_byte)


def humanable_bytes2(num_byte):
    num_byte = float(num_byte)
    if num_byte >= 1024**3:
        return '{:.2f} GB'.format(num_byte/(1024**3))
    elif num_byte >= 1024**2:
        return '{:.2f} MB'.format(num_byte/(1024**2))
    elif num_byte >= 1024**1:
        return '{:.2f} KB'.format(num_byte/(1024**1))

class UCASClient:
    name = "UCAS"
    srun_ip = "124.16.81.61"
    login_url = 'http://{}/cgi-bin/srun_portal'.format(srun_ip)
    online_url = 'http://{}/cgi-bin/rad_user_info'.format(srun_ip)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
    }
    
    def __init__(self, username=None, passwd=None, print_log=True):
        self.username = username
        self.passwd = passwd
        self.print_log = print_log
        self.online_info = dict()
        self.check_online()
        
        self.lm = LoginManager()
        
    def _log(self, msg):
        if self.print_log:
            print('[SrunClient {}] {}'.format(self.name, msg))
    
    def check_online(self):
        resp_text = get_func(self.online_url, headers=self.headers)
        if 'not_online' in resp_text:
            self._log('###*** NOT ONLINE! ***###')
            return False
        try:
            items = resp_text.split(',')
            self.online_info = {
                'online':True, 'username':items[0], 
                'login_time':items[1], 'now_time':items[2], 
                'used_bytes':items[6], 'used_second':items[7], 
                'ip':items[8], 'balance':items[11], 
                'auth_server_version':items[21]
                }
            return True
        except Exception as e:
            print(resp_text)
            print('Catch `Status Internal Server Error`? The request is frequent!')
            print(e)
            
    def show_online(self):
        if not self.check_online(): return
        self._log('###*** ONLINE INFORMATION! ***###')
        header = '================== ONLIN INFORMATION =================='
        print(header)
        print('Username: {}'.format(self.online_info['username']))
        print('Login time: {}'.format(time2date(self.online_info['login_time'])))
        print('Now time: {}'.format(time2date(self.online_info['now_time'])))
        print('Used data: {}'.format(humanable_bytes(self.online_info['used_bytes'])))
        print('Ip: {}'.format(self.online_info['ip']))
        print('Balance: {}'.format(self.online_info['balance']))
        print('=' * len(header))
        
    def login(self):
        self.lm.login(
            username = self.username,
            password = self.passwd
        )
        
    def logout(self):
        if not self.check_online(): return True
        payload = {
            'action': 'logout',
            'ac_id': 1,
            'username': self.online_info['username'],
            'type': 2
            }
        resp_text = post_func(self.login_url, data=payload, headers=self.headers)
        if 'logout_ok' in resp_text:
            self._log('###*** LOGOUT SUCCESS! ***###')
            return True
        elif 'login_error' in resp_text:
            self._log('###*** LOGOUT FAILED! (login error) ***###')
            self._log(resp_text)
            return False
        else:
            self._log('###*** LOGOUT FAILED! (unknown error) ***###')
            self._log(resp_text)
            return False
        
def show_commands():
    wellcome = '############### Wellcome to Srun Client ###############'
    print(wellcome)
    print('[1]: show online information')
    print('[2]: set username and passwd')
    print('[3]: login')
    print('[4]: logout')
    print('[h]: show this messages')
    print('[q]: quit')
    print('#' * len(wellcome))
    
if __name__ == "__main__":
    ucas_client = UCASClient()
    show_commands()
    ucas_client.show_online()
    command = '_'
    while command != 'q':
        command = input('>')
        if command == '1':
            ucas_client.show_online()
        elif command == '2':
            ucas_client.username = input('username: ')
            ucas_client.passwd = getpass.getpass('passwd: ')
        elif command == '3':
            ucas_client.login()
        elif command == '4':
            ucas_client.logout()
        elif command == 'h':
            show_commands()
        elif command == 'q':
            print('bye!')
        else:
            print('unknown command!')
