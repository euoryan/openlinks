import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtProperty  # Adicionando o import correto
import webbrowser
import random

class AnimatedText(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.full_text = text
        self.current_text = ""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_text)
        self.setText("")
        self.setStyleSheet("color: #ffffff; font-size: 14px;")
        self.setMinimumWidth(300)  # Garante espaço suficiente para o texto
        
    def start_animation(self, interval=50):
        self.current_text = ""
        self.timer.start(interval)
        
    def update_text(self):
        if len(self.current_text) < len(self.full_text):
            self.current_text += self.full_text[len(self.current_text)]
            self.setText(self.current_text)
        else:
            self.timer.stop()

class ConnectionDot(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(4, 4)
        self.opacity = 0
        self.animation = QPropertyAnimation(self, b"opacity")
        self.animation.setDuration(1000)
        self.animation.setLoopCount(-1)
        
    @pyqtProperty(float)
    def opacity(self):
        return self._opacity
        
    @opacity.setter
    def opacity(self, value):
        self._opacity = value
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        color = QColor("#dc3545")
        color.setAlphaF(self._opacity)
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        
        painter.drawEllipse(0, 0, 4, 4)

class BackgroundLogo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 200)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Configurar a fonte para o caractere japonês
        font = QFont("Yu Gothic", 150)
        painter.setFont(font)
        
        # Configurar cor semi-transparente
        color = QColor("#dc3545")
        color.setAlphaF(0.05)  # 5% de opacidade
        painter.setPen(color)
        
        # Desenhar o caractere
        painter.drawText(self.rect(), Qt.AlignCenter, "さ")

class FuturisticLoader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connection Interface")
        self.setFixedSize(600, 400)  # Aumentei a largura
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Container principal
        self.container = QWidget()
        self.container.setObjectName("container")
        container_layout = QVBoxLayout(self.container)
        container_layout.setSpacing(20)
        layout.addWidget(self.container)
        
        # Background Logo
        self.background_logo = BackgroundLogo(self.container)
        self.background_logo.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.background_logo.raise_()
        self.background_logo.move(200, 100)  # Ajuste a posição conforme necessário
        
        # Header
        header = QLabel("SISTEMA EUORYAN")
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont("Segoe UI", 20, QFont.Bold))
        header.setStyleSheet("color: #dc3545;")
        container_layout.addWidget(header)
        
        # Status container
        status_container = QWidget()
        status_layout = QVBoxLayout(status_container)
        status_layout.setSpacing(15)
        container_layout.addWidget(status_container)
        
        # Status messages with dots
        self.status_messages = []
        self.dots = []
        messages = [
            "Estabelecendo conexão com o servidor...",
            "Verificando credenciais de acesso...",
            "Recebendo dados do sistema...",
            "Processando informações de usuário...",
            "Preparando interface do sistema..."
        ]
        
        for msg in messages:
            row = QWidget()
            row_layout = QHBoxLayout(row)
            row_layout.setSpacing(10)
            row_layout.setContentsMargins(20, 0, 20, 0)  # Adiciona margem lateral
            
            dot = ConnectionDot()
            self.dots.append(dot)
            row_layout.addWidget(dot)
            
            text = AnimatedText(msg)
            self.status_messages.append(text)
            row_layout.addWidget(text, 1)  # Stretch factor 1
            
            status_layout.addWidget(row)
        
        # Progress Bar
        progress_container = QWidget()
        progress_layout = QHBoxLayout(progress_container)
        progress_layout.setContentsMargins(20, 0, 20, 0)
        
        self.progress = QProgressBar()
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(2)
        self.progress.setObjectName("progressBar")
        progress_layout.addWidget(self.progress)
        
        container_layout.addWidget(progress_container)
        
        # Social info
        social_info = QLabel("@euoryan · github.com/euoryan")
        social_info.setAlignment(Qt.AlignCenter)
        social_info.setStyleSheet("color: #666666;")
        container_layout.addWidget(social_info)
        
        # Estilo
        self.setStyleSheet("""
            QWidget#container {
                background-color: #1a1a1a;
                border: 1px solid #dc3545;
                border-radius: 10px;
            }
            
            QProgressBar {
                border: none;
                background-color: #333333;
            }
            
            QProgressBar::chunk {
                background-color: #dc3545;
            }
        """)
        
        # Centralizar na tela
        self.center_on_screen()
        
        # Iniciar animação
        self.current_step = 0
        self.progress_value = 0
        self.start_animations()
    
    def center_on_screen(self):
        screen = QApplication.desktop().screenGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
    
    def start_animations(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(50)
        
        # Iniciar primeira mensagem
        self.start_next_message()
    
    def start_next_message(self):
        if self.current_step < len(self.status_messages):
            # Animar dot
            dot_anim = self.dots[self.current_step].animation
            dot_anim.setStartValue(0)
            dot_anim.setEndValue(1)
            dot_anim.setEasingCurve(QEasingCurve.InOutQuad)
            dot_anim.start()
            
            # Animar texto
            self.status_messages[self.current_step].start_animation()
            
            # Preparar próxima mensagem
            QTimer.singleShot(1500, self.start_next_message)
            self.current_step += 1
    
    def update_progress(self):
        self.progress_value += 1
        self.progress.setValue(self.progress_value)
        
        if self.progress_value >= 100:
            self.timer.stop()
            self.open_links()
    
    def open_links(self):
        links = [
            "https://euoryan.com/link/",
            "https://github.com/euoryan/"
        ]
        for link in links:
            webbrowser.open_new_tab(link)
        
        # Fecha o app após um breve delay
        QTimer.singleShot(500, self.close)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FuturisticLoader()
    window.show()
    sys.exit(app.exec_())