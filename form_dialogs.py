from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QFrame)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor, QPainter, QBrush
from toggle_image_widget import ToggleImageWidget

class RoundedDialog(QDialog):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        color = QColor("#192a56")  # main background
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 24, 24)
        super().paintEvent(event)

def inputbox(app, prompt, title="Eingabe", default_long_text=""):
    # Subclass QDialog to override paintEvent for opaque rounded background
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
        QDialog {{
            border-radius: 24px;
        }}
        QLabel, QLineEdit, QCheckBox, QPushButton {{
            color: {textcolor};
            font-size: 24px;
            font-family: 'Segoe UI', 'Arial', sans-serif;
        }}
        QLineEdit, QCheckBox {{
            background: {accent};
            border: 2px solid {bordercolor_unfocused};
            border-radius: 8px;
            padding: 8px 12px;
        }}
        QLineEdit:focus, QCheckBox:focus {{
            border: 2px solid {bordercolor};
            background: #233e70;
        }}
        QPushButton {{
            background: {accent};
            border: 2px solid {bordercolor};
            border-radius: 8px;
            padding: 8px 24px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background: {bordercolor};
            color: {darkblue};
        }}
    """
    dialog.setStyleSheet(style)

    font = QFont('Segoe UI', 24)
    dialog.setFont(font)

    layout = QVBoxLayout()
    layout.setSpacing(20)
    layout.setContentsMargins(10, 15, 10, 15)
    dialog.setLayout(layout)

    title_label = QLabel(prompt)
    title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title_label.setFont(font)
    layout.addWidget(title_label)

    new_edit = QLineEdit()
    new_edit.setPlaceholderText("Enter additional text...")
    new_edit.setFont(font)
    new_edit.setFixedHeight(64)
    new_edit.setText(default_long_text)
    layout.addWidget(new_edit)

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
    char_edit = QLineEdit()
    char_edit.setMaxLength(5)
    char_edit.setFixedWidth(120)
    char_edit.setFixedHeight(64)
    char_edit.setFont(font)
    input_layout.addWidget(char_edit)
    input_layout.addSpacing(32)
    b64_uuncheck = "iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAACXBIWXMAAAsTAAALEwEAmpwYAAACHklEQVRoge2aMWsUQRiGn93J7gUVCWzA4q4QEc8QkIBNEjuDP0DwbPIPgpae+AcEY6tpr0qjEH9A0C5eQIQQCMnBocLdFUJOghjJ7jIXi72V2Y2FrjKZk3ma4ftmivcpZpr5HBodFG4Dy8BlzKYN1IFXacMdrgJ4AqxhvgQkGddIMguAseHGYxLDUSPN/HAMuENOwpEyKjffNCd3tyZFeHQROKs5YJ5DWRr/tD81s9+buzl3LISv7NWBdw6NTgeopF3/29fP06srB24cV7XH/Q0GntfaWVyaiM6dv6C0ey6KhCNlaLIEgBvH1enVlQNHylBpl131UOXt602TJVLcOK5WNtY3Mz21CHa3Ar2RihPsbWeyZkREFI7C0wuAiMIrau3m9sc1Zvlb1JfrhMjIYkVMw4qYhhUxDStiGlbENKyIaVgR07AipmFFTMOKmIYVMQ0rYhpWxDSsiGn8tyJHp5KiGIdqkRGRfqmtN0txpF/6qNYZkf7UzBe9cYqTz5oR6c4vzA48r6U30p8z8LxWd35hVu25QDctjoXwdxaXJkyWSf/Zc0MDPYdGpwa8UA87UkaVjfVmsLcdiCi8BJzRmvYk36Vf+tC/eq3fvXErP/kAcNcZTgctAw/05/snPAXq6R15BDw7xTBFeU6S/edll8B9kgGbUXiC20ANuEeSHSc3eAbJ/3WNZAjtOlAGPH0Zf0kM9ID3JMNmL4FIPfADhb+OJo5uNn4AAAAASUVORK5CYII=="
    b64_funcheck = "iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAACXBIWXMAAAsTAAALEwEAmpwYAAACYklEQVRoge2azWoTURiGn5xORmOzKFSofwspknSvNhEvQagVkrmKBtyoeAOCuilYF72FtLS10GtoUnTjqgnxZ2EoBZWCU2Mn48TFydjTcUAa7eQUzgMD4Z0TeB+YObM4X6q3SBw2cLd/3QYu9bNh8A1oA2+AV/3Liy5KxYjcA54B106238C0gIfAqhoK5fcI8BRYQV8JkN1WkF1HwtBSFjxBmp4Wwq6P4PDRKgFL6qpuILyFrenN9e2p865nX+3BaKI1+6RgP2t7H2emtj/PTW/dSosg+q6WgeVUbxEbeAdcCe/sutndUtXZ6/hWPsnSfyNj+Y1lpzo2kXUnlLgNTAqk0W+JbiAOdJQA6PhWvlR19rqBOFDiy4AjgFl18Yt6oaajREjHt/LztWItEs8K4KaarDfy48nVGoyNZi7a8YYALqiJ69k6b70AuJ6di0QXBXAmEp5NqM+/EN25bBG77BRiRHTDiOiGEdENI6IbRkQ3jIhuGBHdMCK6YUR0w4johhHRDSOiG0ZEN4yIbgjkObbKj2EUOQ4p2I9EngB21CRre63kKg3GqO19iEQ7AnirJjP5xtfkKg1GTMfXAlhTk0qhXsxYfiOxVsckY/mNSqFejMRrAnm+/ilM0iKwl53qmI4y4fF05Ky9DSyFAwNloKr+qRsIb75W3Nxo5sZdz54EziXW+Cjfs7b3/k6u+eV+sRY3MOCgiIAcpHmQZMP/wHP6oxzqd+QxsDCUOoPxEtkZOCryE6gg51J03oJbyFdhDtkZiJ/XAnn8W0bObl1HjkmkT7xiPF0OB89WkZvTH4NnvwAB/KODCobGlAAAAABJRU5ErkJggg=="
    b64_fcheck = "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"
    toggle_widget = ToggleImageWidget(b64_uuncheck, b64_funcheck, b64_fcheck)
    toggle_widget.setFixedSize(64, 64)
    input_layout.addWidget(toggle_widget)
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

    screen = app.primaryScreen().geometry()
    dialog.resize(800, 600)
    dialog.move(
        (screen.width() - dialog.width()) // 2,
        (screen.height() - dialog.height()) // 2
    )

    if default_long_text == "Fill":
        new_edit.setFocus()
    else:
        char_edit.setFocus()

    text_result = ""
    check_result = False
    new_edit_result = ""
    if dialog.exec() == QDialog.DialogCode.Accepted:
        text_result = char_edit.text().strip()
        check_result = toggle_widget.checked
        new_edit_result = new_edit.text().strip()

    dialog.deleteLater()
    return text_result, check_result, new_edit_result
