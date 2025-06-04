from PyQt6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor, QPainter, QBrush, QPixmap
import os

class ToggleImageWidget(QLabel):    
    def __init__(self, parent=None):
        super().__init__(parent)
        # Fix path to point to the correct assets directory
        assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')
        
        # Debug: print the assets directory path
        print(f"Assets directory: {assets_dir}")
        
        unchecked_path = os.path.join(assets_dir, 'checkbox_unchecked.png')
        unchecked_hover_path = os.path.join(assets_dir, 'checkbox_unchecked_hover.png')
        checked_path = os.path.join(assets_dir, 'checkbox_checked.png')
        checked_hover_path = os.path.join(assets_dir, 'checkbox_checked_hover.png')
        
        # Debug: Check if files exist
        print(f"Unchecked exists: {os.path.exists(unchecked_path)}")
        print(f"Unchecked hover exists: {os.path.exists(unchecked_hover_path)}")
        print(f"Checked exists: {os.path.exists(checked_path)}")
        print(f"Checked hover exists: {os.path.exists(checked_hover_path)}")
        
        self.icon_unchecked = QPixmap(unchecked_path)
        self.icon_unchecked_hover = QPixmap(unchecked_hover_path)
        self.icon_checked = QPixmap(checked_path)
        self.icon_checked_hover = QPixmap(checked_hover_path)
        
        self.checked = False
        self.focused = False
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFixedSize(50, 50)
        self.corner_radius = 8
        self.update_pixmap()
        self.setStyleSheet(f"border-radius: {self.corner_radius}px; background: transparent;")

    def update_pixmap(self):
        if not self.checked and not self.focused:
            pixmap = self.icon_unchecked
        elif not self.checked and self.focused:
            pixmap = self.icon_unchecked_hover
        elif self.checked and not self.focused:
            pixmap = self.icon_checked
        elif self.checked and self.focused:
            pixmap = self.icon_checked_hover
        else:
            pixmap = self.icon_unchecked
        if pixmap and not pixmap.isNull():
            scaled = pixmap.scaled(42, 42, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.setPixmap(scaled)
        else:
            self.clear()

    def focusInEvent(self, event):
        self.focused = True
        self.update_pixmap()
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.focused = False
        self.update_pixmap()
        super().focusOutEvent(event)

    def toggle(self):
        self.checked = not self.checked
        self.update_pixmap()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.toggle()
        super().mousePressEvent(event)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Space, Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.toggle()
        else:
            super().keyPressEvent(event)


def inputbox(prompt, title="Eingabe", default_long_text="", image_url=None):
    """
    Show a custom PyQt6 dialog for user input with a text field, a 5-char field, and a custom toggle widget.
    Returns: (titel, episode, more)
    """
    app = QApplication.instance()
    app_created = False
    if not app:
        app = QApplication([])
        app_created = True

    class RoundedDialog(QDialog):
        def paintEvent(self, event):
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            rect = self.rect()
            color = QColor("#192a56")
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rect, 24, 24)
            super().paintEvent(event)

    dialog = RoundedDialog()
    dialog.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
    dialog.setFixedSize(400, 400)
    dialog.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    darkblue = "#192a56"
    accent = "#233e70"
    textcolor = "#f5f6fa"
    bordercolor = "#ff9800"
    bordercolor_unfocused = "#0099cc"
    style = f"""
        QDialog {{ border-radius: 24px; }}
        QLabel, QLineEdit, QCheckBox, QPushButton {{
            color: {textcolor}; font-size: 24px; font-family: 'Segoe UI', 'Arial', sans-serif;
        }}
        QLineEdit, QCheckBox {{
            background: {accent}; border: 2px solid {bordercolor_unfocused}; border-radius: 8px; padding: 8px 12px;
        }}
        QLineEdit:focus, QCheckBox:focus {{ border: 2px solid {bordercolor}; background: #233e70; }}
        QPushButton {{ background: {accent}; border: 2px solid {bordercolor}; border-radius: 8px; padding: 8px 24px; font-weight: bold; }}
        QPushButton:hover {{ background: {bordercolor}; color: {darkblue}; }}
    """
    dialog.setStyleSheet(style)

    font = QFont('Segoe UI', 24)
    dialog.setFont(font)
    for widget in dialog.findChildren((QLabel, QLineEdit, QPushButton)):
        widget.setFont(font)

    layout = QVBoxLayout()
    layout.setSpacing(20)
    layout.setContentsMargins(10, 15, 10, 15)
    dialog.setLayout(layout)

    title_label = QLabel(prompt)
    title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title_label.setFont(font)
    layout.addWidget(title_label)

    # Add image preview above the form fields (not above OK button)
    image_label = QLabel()
    image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    image_label.setFixedSize(160, 160)
    image_label.hide()
    layout.insertWidget(1, image_label)  # Insert after title_label, before titel_edit

    titel_edit = QLineEdit()
    titel_edit.setPlaceholderText("Titel...")
    titel_edit.setFont(font)
    titel_edit.setFixedHeight(64)
    titel_edit.setText(default_long_text)
    layout.addWidget(titel_edit)

    layout.addStretch()

    form_frame = QFrame()
    form_frame.setFixedWidth(400)
    form_layout = QVBoxLayout()
    form_layout.setSpacing(24)
    form_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    form_frame.setLayout(form_layout)

    input_layout = QHBoxLayout()
    input_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    input_layout.addStretch(1)
    episode_edit = QLineEdit()
    episode_edit.setMaxLength(5)
    episode_edit.setFixedWidth(120)
    episode_edit.setFixedHeight(64)
    episode_edit.setFont(font)
    episode_edit.setPlaceholderText("Episode...")
    input_layout.addWidget(episode_edit)
    input_layout.addSpacing(32)
    more_toggle = ToggleImageWidget()
    more_toggle.setFixedSize(64, 64)
    input_layout.addWidget(more_toggle)
    input_layout.addStretch(1)

    form_layout.addLayout(input_layout)
    layout.addWidget(form_frame)
    layout.addStretch()

    button_layout = QHBoxLayout()
    button_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    ok_button = QPushButton("OK")
    ok_button.setFont(font)
    ok_button.setFixedHeight(72)
    ok_button.setFixedWidth(220)
    button_layout.addWidget(ok_button)
    layout.addLayout(button_layout)
    ok_button.clicked.connect(dialog.accept)

    # Show image if image_url is provided (for fsmirror/netflix or local fallback)
    from PyQt6.QtGui import QPixmap
    import urllib.parse
    if image_url:
        try:
            pixmap = None
            # Check if image_url is a local file and exists
            if os.path.isfile(image_url):
                pixmap = QPixmap(image_url)
            # If not a local file, try to load from URL
            elif urllib.parse.urlparse(image_url).scheme in ("http", "https"):
                from urllib.request import urlopen
                img_data = urlopen(image_url).read()
                pixmap = QPixmap()
                pixmap.loadFromData(img_data)
            # If pixmap loaded and valid, show it
            if pixmap and not pixmap.isNull():
                image_label.setPixmap(pixmap.scaled(160, 160, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
                image_label.show()
        except Exception as e:
            print(f"Could not load image: {e}")

    screen = app.primaryScreen().geometry()
    dialog.resize(800, 600)
    dialog.move((screen.width() - dialog.width()) // 2, (screen.height() - dialog.height()) // 2)

    if default_long_text == "Fill":
        titel_edit.setFocus()
    else:
        episode_edit.setFocus()

    titel_result = ""
    episode_result = ""
    more_result = False
    if dialog.exec() == QDialog.DialogCode.Accepted:
        episode_result = episode_edit.text().strip()
        more_result = more_toggle.checked
        titel_result = titel_edit.text().strip()

    dialog.deleteLater()
    if app_created:
        QTimer.singleShot(0, app.quit)
    return titel_result, episode_result, more_result
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    result = inputbox("Test Prompt", "Test Title", default_long_text="Default", image_url="icon.png")
    print("Form result:", result)
    sys.exit()