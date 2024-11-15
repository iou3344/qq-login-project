from PyQt5.QtCore import QObject, pyqtSignal
import requests
import time
import re
import threading
import os

class QQLoginManager(QObject):
    qr_code_updated = pyqtSignal(bytes)  # 二维码数据
    status_updated = pyqtSignal(str)  # 状态信息
    login_success = pyqtSignal(str, str)  # QQ号, 昵称
    login_failed = pyqtSignal(str)  # 错误信息
    
    def __init__(self):
        super().__init__()
        self.running = False
        self.thread = None
        
    def get_ptqrtoken(self, qrsig):
        e = 0
        for i in range(len(qrsig)):
            e += (e << 5) + ord(qrsig[i])
        return 2147483647 & e
    
    def start_login(self):
        if self.thread and self.thread.is_alive():
            return
            
        self.running = True
        self.thread = threading.Thread(target=self._login_thread)
        self.thread.daemon = True
        self.thread.start()
        
    def stop_login(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
            
    def _login_thread(self):
        retry_count = 0
        while self.running and retry_count < 3:
            try:
                if not self._get_qrcode():
                    retry_count += 1
                    continue
                    
                if self._check_login_status():
                    break
                    
                # 如果登录失败，重试
                retry_count += 1
                time.sleep(1)
                
            except Exception as e:
                self.login_failed.emit(f'登录出错: {str(e)}')
                retry_count += 1
                time.sleep(1)
                
    def _get_qrcode(self):
        url = 'https://ssl.ptlogin2.qq.com/ptqrshow'
        params = {
            'appid': '549000912',
            'e': '2',
            'l': 'M',
            's': '3',
            'd': '72',
            'v': '4',
            't': str(time.time()),
            'daid': '5'
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0.0.0'
        }
        
        r = requests.get(
            url, 
            params=params, 
            headers=headers, 
            proxies={'http': None, 'https': None}, 
            verify=True
        )
        
        if r.status_code == 200:
            self.qrsig = r.cookies.get('qrsig')
            if self.qrsig:
                self.qr_code_updated.emit(r.content)
                self.status_updated.emit('请使用手机QQ扫码登录')
                return True
                
        return False
        
    def _check_login_status(self):
        ptqrtoken = self.get_ptqrtoken(self.qrsig)
        check_url = 'https://ssl.ptlogin2.qq.com/ptqrlogin'
        
        qr_expired_time = time.time() + 180  # 二维码3分钟有效期
        
        while self.running and time.time() < qr_expired_time:
            params = {
                'u1': 'https://qzs.qq.com/qzone/v5/loginsucc.html',
                'ptqrtoken': ptqrtoken,
                'ptredirect': '0',
                'h': '1',
                't': '1',
                'g': '1',
                'from_ui': '1',
                'ptlang': '2052',
                'action': '0-0-' + str(int(time.time())),
                'js_ver': '22080914',
                'js_type': '1',
                'login_sig': '',
                'pt_uistyle': '40',
                'aid': '549000912',
                'daid': '5'
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0.0.0'
            }
            
            try:
                r = requests.get(
                    check_url,
                    params=params,
                    cookies={'qrsig': self.qrsig},
                    headers=headers,
                    proxies={'http': None, 'https': None},
                    verify=True
                )
                
                if '二维码未失效' in r.text:
                    self.status_updated.emit('等待扫码...')
                elif '二维码认证中' in r.text:
                    self.status_updated.emit('正在验证...')
                elif '二维码已失效' in r.text:
                    self.status_updated.emit('二维码已失效，正在刷新...')
                    return False
                elif '登录成功' in r.text:
                    qq_number = re.search(r'&uin=(\d+?)&', r.text)
                    nick_name = re.search(r'nickname=([^&]+)&', r.text)
                    
                    if qq_number:
                        self.login_success.emit(
                            qq_number.group(1),
                            nick_name.group(1) if nick_name else ''
                        )
                    return True
                    
            except Exception as e:
                self.status_updated.emit(f'网络错误: {str(e)}')
                time.sleep(1)
                continue
                
            time.sleep(2)
            
        return False