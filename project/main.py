from ui.panels.login_panel import QQLoginPanel

class MainWindow:
    def __init__(self):
        # ...其他初始化代码...
        
        self.login_panel = QQLoginPanel()
        self.login_panel.login_success.connect(self.onLoginSuccess)
        self.login_panel.login_failed.connect(self.onLoginFailed)
        
    def showLoginPanel(self):
        self.login_panel.show()
        
    def onLoginSuccess(self, qq_number, nickname):
        print(f"登录成功 QQ: {qq_number}, 昵称: {nickname}")
        # 处理登录成功后的逻辑
        
    def onLoginFailed(self, error_msg):
        print(f"登录失败: {error_msg}")
        # 处理登录失败的逻辑