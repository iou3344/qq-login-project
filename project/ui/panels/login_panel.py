from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from core.login_manager import QQLoginManager

class QQLoginPanel(QWidget):
    login_success = pyqtSignal(str, str)  # QQ号, 昵称
    login_failed = pyqtSignal(str)  # 错误信息
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.login_manager = QQLoginManager()
        self.initUI()
        self.setupConnections()
        
    def initUI(self):
        self.setFixedSize(300, 380)
        
        layout = QVBoxLayout()
        
        # 二维码显示标签
        self.qr_label = QLabel()
        self.qr_label.setFixedSize(200, 200)
        self.qr_label.setStyleSheet("""
            QLabel {
                background-color: white;
                border: 1px solid #dcdcdc;
                border-radius: 3px;
            }
        """)
        layout.addWidget(self.qr_label, alignment=Qt.AlignCenter)
        
        # 状态显示标签
        self.status_label = QLabel('正在获取二维码...')
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
        
    def setupConnections(self):
        self.login_manager.qr_code_updated.connect(self.updateQRCode)
        self.login_manager.status_updated.connect(self.status_label.setText)
        self.login_manager.login_success.connect(self.onLoginSuccess)
        self.login_manager.login_failed.connect(self.onLoginFailed)
        
    def showEvent(self, event):
        super().showEvent(event)
        self.login_manager.start_login()
        
    def hideEvent(self, event):
        super().hideEvent(event)
        self.login_manager.stop_login()
        
    def updateQRCode(self, qr_data):
        pixmap = QPixmap()
        pixmap.loadFromData(qr_data)
        self.qr_label.setPixmap(pixmap.scaled(
            200, 200,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        ))
        
    def onLoginSuccess(self, qq_number, nickname):
        self.login_success.emit(qq_number, nickname)
        
    def onLoginFailed(self, error_msg):
        self.login_failed.emit(error_msg)