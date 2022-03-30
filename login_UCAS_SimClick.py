# from pyvirtualdisplay import Display

from selenium import webdriver
import requests
import time
import getpass

# 日期数据转换
def time2date(timestamp):
    time_arry = time.localtime(int(timestamp))
    return time.strftime('%Y-%m-%d %H:%M:%S', time_arry)

# 流量数据转换
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

class UCASLoginManager:
    def __init__(self, url="http://124.16.81.61"):
        self.url = url
        self.login_url = url + "/cgi-bin/srun_portal"
        self.online_url = url + "/cgi-bin/rad_user_info"
        # self.browser = webdriver.Chrome()
        self.browser = webdriver.Firefox()
        self.browser.get(self.url)
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
        }
        self.username = ""
        self.password = ""
        
    def is_online(self, ):
        _text = requests.get(self.online_url, headers=self.headers).text
        if 'not_online' in _text:
            return False
        try:
            items = _text.split(',')
            self.online_info = {
                'online':True, 'username':items[0], 
                'login_time':items[1], 'now_time':items[2], 
                'used_bytes':items[6], 'used_second':items[7], 
                'ip':items[8], 'balance':items[11], 
                'auth_server_version':items[21]
                }
            return True
        except Exception as e:
            print(_text)
            print('Catch `Status Internal Server Error`? The request is frequent!')
            print(e)
            
    def show_online(self):
        if not self.is_online(): 
            print('###*** NOT ONLINE! ***###')
            return
        print('###*** ONLINE INFORMATION! ***###')
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
        # 如果已在线，判断是否重新登录
        if self.is_online():
            while 1:
                _continue = input("已在线，是否重新登录[y/n]: ")
                if _continue=="n" or _continue=="no":
                    return
                elif _continue=="y" or _continue=="yes":
                    # TODO: 待实现
                    self.logout()
                    break
                else:
                    continue
                    
        # 处理登陆，输入用户名和密码
        self.username = input("username: ")
        self.password = getpass.getpass("password: ")
        
        # 填充用户名和密码
        username_box = self.browser.find_element_by_id("username")
        passwd_box = self.browser.find_element_by_id("password")
        username_box.send_keys(self.username)
        passwd_box.send_keys(self.password)
        # 模拟点击
        login_button = self.browser.find_element_by_class_name("btn-login")
        login_button.click()
        time.sleep(1)
        self.show_online()
        
    # 模拟点击下线
    def _logout(self):
        # 判断是否在线，只对在线情况进行处理
        if self.is_online():
            logout_button = self.browser.find_element_by_class_name("btn-logout")
            logout_button.click()
            time.sleep(1)
            logout_confirm = self.browser.find_element_by_class_name("btn-confirm")
            logout_confirm.click()
        print('###*** LOGOUT SUCCESS! ***###')
        
    # 发送请求下线
    def logout(self):
        if not self.is_online(): return True
        payload = {
            'action': 'logout',
            'ac_id': 1,
            'username': self.online_info['username'],
            'type': 2
            }
        # 发送下线请求
        resp_text = requests.post(
            self.login_url, 
            data=payload, 
            headers=self.headers
        ).text
        self.browser.refresh()
        if 'logout_ok' in resp_text:
            print('###*** LOGOUT SUCCESS! ***###')
            return True
        elif 'login_error' in resp_text:
            print('###*** LOGOUT FAILED! (login error) ***###')
            print(resp_text)
            return False
        else:
            print('###*** LOGOUT FAILED! (unknown error) ***###')
            print(resp_text)
            return False
        
    def exit(self):
        self.browser.close()

def show_commands():
    wellcome = '############### Wellcome to Srun Client ###############'
    print(wellcome)
    print('[1]: show online information')
    print('[2]: login')
    print('[3]: logout')
    print('[h]: show this messages')
    print('[q]: quit')
    print('#' * len(wellcome))
    
if __name__ == "__main__":
    # 虚拟界面
    # _dis = Display(visible=0, size=(600,600))
    # _dis.start()
    
    # manager
    ucas_client = UCASLoginManager()
    show_commands()
    ucas_client.show_online()
    command = '_'
    while command != 'q':
        command = input('>')
        if command == '1':
            ucas_client.show_online()
        elif command == '2':
            ucas_client.login()
        elif command == '3':
            ucas_client.logout()
        elif command == 'h':
            show_commands()
        elif command == 'q':
            ucas_client.exit()
            print('bye!')
        else:
            print('unknown command!')