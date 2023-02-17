import io
import sys
import PyQt5.QtWidgets as qtw
import matplotlib.pyplot as plt # Test
from PyQt5.QtCore import QFile, QIODevice
from PyQt5.QtWidgets import (
  QApplication, QPushButton, QMainWindow, QLabel, QFileDialog, QTextEdit)
from PyQt5.QtGui import QFont
sys.path.append('../')

from src.rc4 import rc4
from src.vigenere import vigenere_ext

# Color Palette
# 1B048A, 0047C0, 0073DD, 009BE2, 00C1D6, 00E5C1
COLOR_TEXT_D = 'color: #0047C0'
COLOR_TEXT_L = 'color: #009BE2'
COLOR_ERROR = 'color: #CE0000'
TEXTBOX_STYLE = 'background-color: #FFFFFF; color: #000000; font-size: 16px'

def bytes_to_string(data: bytes):
  return ''.join([chr(data[i]) for i in range(len(data))])

def string_to_bytes(data: str):
  return [ord(data[i]) for i in range(len(data))]

class Window(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setStyleSheet('background-color: #FAF9F6')
    self.setWindowTitle('RC4 and Extended Vigenere Cyper')
    self.setGeometry(0, 0, 1100, 1000)
    self.setMinimumSize(1100, 1000)
    
    # Labels
    self._lbl_title = QLabel('II4031 - Kriptografi dan Koding (Tugas 2)', self)
    self._lbl_title.move(10, 10)
    self._lbl_title.resize(700, 35)
    self._lbl_title.setFont(QFont('AnyStyle', 20, 500))
    self._lbl_title.setStyleSheet(COLOR_TEXT_D)

    self._lbl_input = QLabel('Plaintext Input', self)
    self._lbl_input.move(10, 40)
    self._lbl_input.resize(200, 35)
    self._lbl_input.setFont(QFont('AnyStyle', 14, 30))
    self._lbl_input.setStyleSheet(COLOR_TEXT_L)
    
    self._lbl_finput = QLabel('File Input', self)
    self._lbl_finput.move(440, 40)
    self._lbl_finput.resize(200, 35)
    self._lbl_finput.setFont(QFont('AnyStyle', 14, 30))
    self._lbl_finput.setStyleSheet(COLOR_TEXT_L)

    self._lbl_seinput = QLabel('Encrypt Secret Input\n*Between 8 and 256 Characters', self)
    self._lbl_seinput.move(660, 40)
    self._lbl_seinput.resize(300, 50)
    self._lbl_seinput.setFont(QFont('AnyStyle', 14, 30))
    self._lbl_seinput.setStyleSheet(COLOR_TEXT_L)
    
    self._lbl_error = QLabel('No Error', self)
    self._lbl_error.move(660, 300)
    self._lbl_error.resize(500, 150)
    self._lbl_error.setFont(QFont('AnyStyle', 12, 30))
    self._lbl_error.setStyleSheet(COLOR_ERROR)

    self._lbl_encrypted = QLabel('Encrypted File/Text', self)
    self._lbl_encrypted.move(10, 400)
    self._lbl_encrypted.resize(300, 50)
    self._lbl_encrypted.setFont(QFont('AnyStyle', 14, 30))
    self._lbl_encrypted.setStyleSheet(COLOR_TEXT_L)
    
    self._lbl_sdinput = QLabel('Decrypt Secret Input (*Between 8 and 256 Characters)', self)
    self._lbl_sdinput.move(10, 610)
    self._lbl_sdinput.resize(500, 50)
    self._lbl_sdinput.setFont(QFont('AnyStyle', 14, 30))
    self._lbl_sdinput.setStyleSheet(COLOR_TEXT_L)
    
    self._lbl_decrypted = QLabel('Decrypted File/Text', self)
    self._lbl_decrypted.move(10, 775)
    self._lbl_decrypted.resize(300, 50)
    self._lbl_decrypted.setFont(QFont('AnyStyle', 14, 30))
    self._lbl_decrypted.setStyleSheet(COLOR_TEXT_L)

    self._input_ptext = QTextEdit(self,
                                  lineWrapMode=qtw.QTextEdit.FixedColumnWidth,
                                  lineWrapColumnOrWidth=-1)
    self._input_ptext.move(10, 70)
    self._input_ptext.setFixedSize(400, 250)
    self._input_ptext.setStyleSheet(TEXTBOX_STYLE)
    
    self._input_esecret = QTextEdit(self,
                                  lineWrapMode=qtw.QTextEdit.FixedColumnWidth,
                                  lineWrapColumnOrWidth=-1)
    self._input_esecret.move(660, 100)
    self._input_esecret.setFixedSize(400, 200)
    self._input_esecret.setStyleSheet(TEXTBOX_STYLE)
    
    self._input_dsecret = QTextEdit(self,
                                  lineWrapMode=qtw.QTextEdit.FixedColumnWidth,
                                  lineWrapColumnOrWidth=-1)
    self._input_dsecret.move(10, 660)
    self._input_dsecret.setFixedSize(900, 100)
    self._input_dsecret.setStyleSheet(TEXTBOX_STYLE)
    
    # Buttons
    self._btn_load = QPushButton(self)
    self._btn_load.move(440, 85)
    self._btn_load.clicked.connect(self.load_file)
    self._btn_load.setFont(QFont('Courier', 14, 100))
    self._btn_load.setText('Load File')
    self._btn_load.setFixedSize(150, 30)
    self._btn_load.setStyleSheet('QPushButton { background-color: #0047C0; color: #FAF9F6; }'
                               'QPushButton::pressed { background-color: #FAF9F6; color: #0047C0; }')

    self._btn_eptext = QPushButton(self)
    self._btn_eptext.clicked.connect(self.encrypt)
    self._btn_eptext.move(10, 350)
    self._btn_eptext.setFont(QFont('Courier', 14, 100))
    self._btn_eptext.setText('Encrypt')
    self._btn_eptext.setFixedSize(150, 30)
    self._btn_eptext.setStyleSheet('QPushButton { background-color: #0047C0; color: #FAF9F6; }'
                               'QPushButton::pressed { background-color: #FAF9F6; color: #0047C0; }')
    
    self._btn_save = QPushButton(self)
    self._btn_save.clicked.connect(self.save_encrypted)
    self._btn_save.move(925, 500)
    self._btn_save.setFont(QFont('Courier', 14, 100))
    self._btn_save.setText('Save to File')
    self._btn_save.setFixedSize(150, 30)
    self._btn_save.setStyleSheet('QPushButton { background-color: #0047C0; color: #FAF9F6; }'
                               'QPushButton::pressed { background-color: #FAF9F6; color: #0047C0; }')
    
    self._btn_decrypt = QPushButton(self)
    self._btn_decrypt.clicked.connect(self.decrypt)
    self._btn_decrypt.move(925, 690)
    self._btn_decrypt.setFont(QFont('Courier', 14, 100))
    self._btn_decrypt.setText('Decrypt')
    self._btn_decrypt.setFixedSize(150, 30)
    self._btn_decrypt.setStyleSheet('QPushButton { background-color: #0047C0; color: #FAF9F6; }'
                               'QPushButton::pressed { background-color: #FAF9F6; color: #0047C0; }')
    
    self._btn_dsave = QPushButton(self)
    self._btn_dsave.clicked.connect(self.save_decrypted)
    self._btn_dsave.move(925, 875)
    self._btn_dsave.setFont(QFont('Courier', 14, 100))
    self._btn_dsave.setText('Save to File')
    self._btn_dsave.setFixedSize(150, 30)
    self._btn_dsave.setStyleSheet('QPushButton { background-color: #0047C0; color: #FAF9F6; }'
                               'QPushButton::pressed { background-color: #FAF9F6; color: #0047C0; }')
    
    self._output_encrypted = QTextEdit(self,
                                  lineWrapMode=qtw.QTextEdit.FixedColumnWidth,
                                  lineWrapColumnOrWidth=-1,
                                  readOnly=True)
    self._output_encrypted.move(10, 450)
    self._output_encrypted.setFixedSize(900, 150)
    self._output_encrypted.setStyleSheet(TEXTBOX_STYLE)
    
    self._output_decrypted = QTextEdit(self,
                                  lineWrapMode=qtw.QTextEdit.FixedColumnWidth,
                                  lineWrapColumnOrWidth=-1,
                                  readOnly=True)
    self._output_decrypted.move(10, 820)
    self._output_decrypted.setFixedSize(900, 150)
    self._output_decrypted.setStyleSheet(TEXTBOX_STYLE)

    self._cur_filepath = None

    self.show()
  
  def load_file(self):
    filepath = QFileDialog.getOpenFileName(None, 'OpenFile', '')
    if not filepath[0]: return
    self._cur_filepath = filepath[0]
    
    with open(self._cur_filepath, 'rb') as f:
      file_bytes = f.read()
    
    self._input_ptext.setPlainText(bytes_to_string(file_bytes))

  def encrypt(self):
    if not self._input_esecret.toPlainText():
      return self._lbl_error.setText('Please input secret used to encrypt')
    
    if not 8 <= len(self._input_esecret.toPlainText()) <= 256:
      return self._lbl_error.setText('Encrypt Secret\'s character count must be between [8...256]')

    if not self._input_ptext.toPlainText():
      return self._lbl_error.setText('Please input text to encrypt')

    secret = string_to_bytes(self._input_esecret.toPlainText())
    data = string_to_bytes(self._input_ptext.toPlainText())
    self.encrypted = vigenere_ext(secret, rc4(secret, data))
    self._output_encrypted.setPlainText(bytes_to_string(self.encrypted))

  def decrypt(self):
    if not self._output_encrypted.toPlainText():
      return self._lbl_error.setText('Please encrypt something first')

    if not self._input_dsecret.toPlainText():
      return self._lbl_error.setText('Please input secret used to decrypt')

    if not 8 <= len(self._input_dsecret.toPlainText()) <= 256:
      return self._lbl_error.setText('Decrypt Secret\'s character count must be between [8...256]')

    secret = string_to_bytes(self._input_dsecret.toPlainText())
    data = self.encrypted
    self.decrypted =  rc4(secret, vigenere_ext(secret, data, False))
    self._output_decrypted.setPlainText(bytes_to_string(self.decrypted))
  
  def save_encrypted(self):
    file_name, _ = QFileDialog.getSaveFileName(self, 'Save File', '')
    if not file_name: return
    file = QFile(file_name)
    if file.open(QIODevice.WriteOnly | QIODevice.Text):
      file.write(self.encrypted)
      file.close()
  
  def save_decrypted(self):
    file_name, _ = QFileDialog.getSaveFileName(self, 'Save File', '')
    if not file_name: return
    file = QFile(file_name)
    if file.open(QIODevice.WriteOnly | QIODevice.Text):
      file.write(self.decrypted)
      file.close()

if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = Window()
  sys.exit(app.exec_())
