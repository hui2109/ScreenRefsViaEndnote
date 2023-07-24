# from lxml import etree
#
# # 要插入的XML节点
# new_record = '<record>some text.</record>'
#
# # 解析XML文件
# xml_template = '''<xml>
#     <records>
#     </records>
# </xml>'''
#
# root = etree.fromstring(xml_template)
# print(etree.tostring(root))
#
# # 找到要插入的位置（这里假设要插入到<records>节点的末尾）
# records_node = root.find('.//records')
# print(type(records_node))
#
# # 创建要插入的节点
# new_node = etree.fromstring(new_record)
#
# # 将新节点插入到指定位置
# records_node.append(new_node)
#
# # 输出插入后的XML内容
# resulting_xml = etree.tostring(root, pretty_print=True, encoding='unicode')
# print(resulting_xml)

# from PyQt6.QtWidgets import *
# from PyQt6.QtCore import *
# from PyQt6.QtGui import *
#
#
# class MyWindow(QMainWindow):
#     def __init__(self, *args, **kwargs):
#         super(MyWindow, self).__init__(*args, **kwargs)
#         self.resize(500, 500)
#         self.setWindowTitle('的学习')
#         self.move(100, 100)
#         self.initWidgets()
#
#     def initWidgets(self):
#         pass
#
#
# if __name__ == '__main__':
#     import sys
#
#     app = QApplication(sys.argv)
#     window = MyWindow()
#     window.show()
#     sys.exit(app.exec())

# def is_chinese_or_english(char):
#     code_point = ord(char)
#     return (0x4E00 <= code_point <= 0x9FFF) or (0x3400 <= code_point <= 0x4DBF) or (0x20000 <= code_point <= 0x2A6DF) or (0x2A700 <= code_point <= 0x2B73F) or (0x2B740 <= code_point <= 0x2B81F) or (0x2B820 <= code_point <= 0x2CEAF) or (0x2F800 <= code_point <= 0x2FA1F) or (0x41 <= code_point <= 0x5A) or (0x61 <= code_point <= 0x7A)
#
# # Test the function
# characters = "Hello, 你好，世界！"
# for char in characters:
#     if is_chinese_or_english(char):
#         print(f"'{char}' is Chinese or English.")
#     else:
#         print(f"'{char}' is neither Chinese nor English.")

# def is_chinese_or_english(char):
#     try:
#         # Get the Unicode character name
#         name = unicodedata.name(char)
#         # Check if the character is Chinese (Han) or Latin (English)
#         return 'CJK UNIFIED IDEOGRAPH' in name or 'LATIN' in name
#     except ValueError:
#         # If unicodedata.name() raises ValueError, the character is not a valid Unicode character
#         return False
#
# # Test the function
# characters = "Hello, 你好，世界！"
# for char in characters:
#     if is_chinese_or_english(char):
#         print(f"'{char}' is Chinese or English.")
#     else:
#         print(f"'{char}' is neither Chinese nor English.")


# def is_chinese(str_):
#     if not '\u4e00' <= str_ <= '\u9fa5':
#         return False
#     else:
#         return True
#
#
# print(is_chinese("好"))
# print(is_chinese("刚"))
# print(is_chinese("f"))


# import sys
#
# from PyQt6.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem
#
#
# class MyWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle('ListWidgetItem Index Example')
#         self.setGeometry(100, 100, 400, 200)
#
#         list_widget = QListWidget(self)
#         list_widget.setGeometry(20, 20, 360, 160)
#
#         for index in range(20):
#             item = QListWidgetItem(f'Item {index}')
#             item.setData(1, index)  # Set the index as custom data for the item
#             list_widget.addItem(item)
#
#         list_widget.clicked.connect(self.onItemClicked)
#
#     def onItemClicked(self, item):
#         index = item.data(1)  # Get the custom data (index) of the clicked item
#         print(f'Clicked Item Index: {index}')
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MyWindow()
#     window.show()
#     sys.exit(app.exec())

# import sys
# from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QMessageBox, QClipboard
#
# class MyWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle('Copy Button Example')
#         self.setGeometry(100, 100, 400, 200)
#
#         central_widget = QWidget(self)
#         self.setCentralWidget(central_widget)
#
#         layout = QVBoxLayout()
#         central_widget.setLayout(layout)
#
#         # Sample text to be copied
#         self.text_to_copy = "Hello, this text will be copied!"
#
#         label = QLabel(self.text_to_copy, self)
#         layout.addWidget(label)
#
#         copy_button = QPushButton('Copy', self)
#         layout.addWidget(copy_button)
#
#         # Connect the button's clicked signal to the copy_text function
#         copy_button.clicked.connect(self.copy_text)
#
#     def copy_text(self):
#         # Get a reference to the clipboard
#         clipboard = QApplication.clipboard()
#
#         # Set the text to be copied to the clipboard
#         clipboard.setText(self.text_to_copy)
#
#         # Show a message box to indicate successful copy
#         QMessageBox.information(self, 'Copy Success', 'Text copied to clipboard!', QMessageBox.Ok)
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MyWindow()
#     window.show()
#     sys.exit(app.exec())


# import sys
#
# from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog
#
#
# class MyWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle('Open File Dialog Example')
#         self.setGeometry(100, 100, 400, 200)
#
#         # Create a QPushButton to open the file dialog
#         open_button = QPushButton('Open File', self)
#         open_button.setGeometry(150, 80, 100, 30)
#
#         # Connect the button's clicked signal to the open_file_dialog function
#         open_button.clicked.connect(self.open_file_dialog)
#
#     def open_file_dialog(self):
#         # Show the file dialog to open a file
#         # options = QFileDialog.Options()
#         file_name, _ = QFileDialog.getOpenFileName(self, "Open Fileaaa", "", "XML File (*.xml)")
#
#         # If a file is selected, print its path
#         if file_name:
#             print(f"Selected file: {file_name}")
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MyWindow()
#     window.show()
#     sys.exit(app.exec())


# import sys
# from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
# from PyQt6.QtCore import Qt, QEvent, QTimer
# from PyQt6.QtGui import QKeyEvent
#
# class MyWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle('Button with "qq" Shortcut')
#         self.setGeometry(100, 100, 400, 200)
#
#         self.button = QPushButton('Click Me (qq)', self)
#         self.button.setGeometry(100, 80, 200, 30)
#
#         self.q_count = 0
#         self.q_timer = QTimer()
#         self.q_timer.timeout.connect(self.reset_q_count)
#
#     def event(self, event):
#         if event.type() == QEvent.Type.KeyPress:
#             key_event = QKeyEvent(event)
#
#             if key_event.key() == Qt.Key.Key_Q:
#                 if self.q_count == 0:
#                     self.q_timer.start(500)  # Start the timer to handle the second "q"
#                 self.q_count += 1
#
#                 if self.q_count == 2:
#                     self.q_count = 0
#                     self.q_timer.stop()
#                     self.button.click()
#                     return True
#
#         return super().event(event)
#
#     def reset_q_count(self):
#         self.q_count = 0
#         self.q_timer.stop()
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MyWindow()
#     window.show()
#     sys.exit(app.exec())


# import sys
#
# from PyQt6.QtCore import *
# from PyQt6.QtWidgets import *
# from PyQt6.QtGui import *
#
#
# class CustomEventFilter(QObject):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.key_sequence = ""
#
#     def eventFilter(self, obj, event):
#         if event.type() == QEvent.Type.KeyPress:
#             key = event.key()
#             if key == Qt.Key.Key_Q:
#                 self.key_sequence += "q"
#                 if self.key_sequence == "qq":
#                     self.key_sequence = ""
#                     obj.click()
#             else:
#                 self.key_sequence = ""
#         return super().eventFilter(obj, event)
#
#
# class MyWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle('Button with "qq" Shortcut')
#         self.setGeometry(100, 100, 400, 200)
#
#         button = QPushButton('Click Me ("qq")', self)
#         button.setGeometry(100, 80, 200, 30)
#         button.clicked.connect(self.on_button_clicked)
#
#         event_filter = CustomEventFilter(self)
#         self.installEventFilter(event_filter)
#
#         # Create a QShortcut for the "qq" sequence
#         shortcut_qq = QShortcut(QKeySequence.fromString('qq'), self)
#         shortcut_qq.activated.connect(button.click)
#
#     def on_button_clicked(self):
#         print("Button clicked!")
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MyWindow()
#     window.show()
#     sys.exit(app.exec())

# import sys
#
# from PyQt6.QtCore import *
# from PyQt6.QtWidgets import *
# from PyQt6.QtGui import *
#
#
# class CustomEventFilter(QObject):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.key_sequence = ""
#         self.timer = QTimer()
#         self.timer.setInterval(300)  # Set the time interval (in milliseconds) to detect double-click
#         self.timer.timeout.connect(self.reset_sequence)
#
#     def eventFilter(self, obj, event):
#         if event.type() == QEvent.Type.KeyPress:
#             key = event.key()
#             if key == Qt.Key.Key_Q:
#                 self.key_sequence += "q"
#                 if len(self.key_sequence) == 2:
#                     # Start the timer to detect double-click
#                     self.timer.start()
#                 if len(self.key_sequence) > 2:
#                     # If more than two consecutive keys are pressed, reset the sequence
#                     self.reset_sequence()
#             else:
#                 self.reset_sequence()
#         return super().eventFilter(obj, event)
#
#     def reset_sequence(self):
#         self.key_sequence = ""
#         self.timer.stop()
#
#
# class MyWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle('Keyboard Double-Click Event')
#         self.setGeometry(100, 100, 400, 200)
#
#         button = QPushButton('Double Click Me ("qq")', self)
#         button.setGeometry(100, 80, 200, 30)
#         button.clicked.connect(self.on_double_click)
#
#         event_filter = CustomEventFilter(self)
#         self.installEventFilter(event_filter)
#
#         # Create a QShortcut for the "qq" sequence
#         shortcut_qq = QShortcut(QKeySequence.fromString('qq'), self)
#         shortcut_qq.activated.connect(self.on_double_click)
#
#     def on_double_click(self):
#         print("Double-clicked!")
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MyWindow()
#     window.show()
#     sys.exit(app.exec())


# import sys
# from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QStackedWidget, QVBoxLayout, QWidget
#
# class MyWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle('QStackedWidget Example')
#         self.setGeometry(100, 100, 400, 200)
#
#         central_widget = QWidget(self)
#         self.setCentralWidget(central_widget)
#
#         layout = QVBoxLayout()
#         central_widget.setLayout(layout)
#
#         # Create a QStackedWidget
#         stacked_widget = QStackedWidget(self)
#         layout.addWidget(stacked_widget)
#
#         # Page 1
#         page1 = QWidget()
#         page1_layout = QVBoxLayout()
#         page1.setLayout(page1_layout)
#         label1 = QLabel("Page 1")
#         page1_layout.addWidget(label1)
#         stacked_widget.addWidget(page1)
#
#         # Page 2
#         page2 = QWidget()
#         page2_layout = QVBoxLayout()
#         page2.setLayout(page2_layout)
#         label2 = QLabel("Page 2")
#         page2_layout.addWidget(label2)
#         stacked_widget.addWidget(page2)
#
#         # Create buttons to switch between pages
#         button1 = QPushButton("Show Page 1")
#         button1.clicked.connect(lambda: stacked_widget.setCurrentIndex(0))
#
#         button2 = QPushButton("Show Page 2")
#         button2.clicked.connect(lambda: stacked_widget.setCurrentIndex(1))
#
#         layout.addWidget(button1)
#         layout.addWidget(button2)
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MyWindow()
#     window.show()
#     sys.exit(app.exec())


# import sys
#
# from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
#
#
# class Window1(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle('Window 1')
#         self.setGeometry(100, 100, 400, 200)
#
#         button = QPushButton('Open Window 2', self)
#         button.setGeometry(150, 80, 100, 30)
#         button.clicked.connect(self.open_window2)
#
#     def open_window2(self):
#         self.close()
#         self.window2 = Window2()
#         self.window2.show()
#
#
# class Window2(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle('Window 2')
#         self.setGeometry(200, 200, 400, 200)
#
#         button = QPushButton('Open Window 1', self)
#         button.setGeometry(150, 80, 100, 30)
#         button.clicked.connect(self.open_window1)
#
#     def open_window1(self):
#         self.close()
#         self.window1 = Window1()
#         self.window1.show()
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window1 = Window1()
#     window1.show()
#     sys.exit(app.exec())


# import sys
# from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
#
# class Window1(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle('Window 1')
#         self.setGeometry(100, 100, 400, 200)
#
#         button = QPushButton('Open Window 2', self)
#         button.setGeometry(150, 80, 100, 30)
#         button.clicked.connect(self.open_window2)
#
#     def closeEvent(self, event):
#         # Handle the close event here (e.g., ask for confirmation)
#         reply = self.ask_for_confirmation()
#         if reply:
#             event.accept()  # Accept the close event
#         else:
#             event.ignore()  # Ignore the close event
#
#     def ask_for_confirmation(self):
#         # Implement your confirmation dialog here
#         return True  # Returning True for simplicity (always confirm)
#
#     def open_window2(self):
#         self.hide()  # Hide the current window instead of closing
#         window2 = Window2(self)
#         window2.show()
#
# class Window2(QMainWindow):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle('Window 2')
#         self.setGeometry(200, 200, 400, 200)
#
#         button = QPushButton('Open Window 1', self)
#         button.setGeometry(150, 80, 100, 30)
#         button.clicked.connect(self.open_window1)
#
#     def open_window1(self):
#         self.hide()  # Hide the current window instead of closing
#         self.parent().show()  # Show the parent window (Window1)
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window1 = Window1()
#     window1.show()
#     sys.exit(app.exec())




def _switch_btn_clicked1(self):
    if self.saved_dir_name:
        self._save_btn_clicked()

        # 隐藏控件
        self.hide()

        self.window2 = MyWindow2()
        try:
            self.window2.show()
        except Exception as e:
            self.window2._save_btn_clicked()
            print(e)

        if os.path.exists(os.path.join(AssetsPath, 'last_loaded_dir_path.pkl')):
            self.window2.saved_dir_name = load_pickle(os.path.join(AssetsPath, 'last_loaded_dir_path.pkl'))
            self.window2._base_load(self.window2.saved_dir_name)
            self.window2._enable_some_buttons()
        else:
            self.window2.status_bar.showMessage('缺失关键文件！请手动加载！')

    else:
        # 隐藏控件
        self.hide()

        self.window2 = MyWindow2()
        self.window2.show()

        self.window2._load_btn_clicked()


def _switch_btn_clicked2(self):
    if self.saved_dir_name:
        self._save_btn_clicked()

        # 隐藏控件
        self.hide()

        self.window1 = MyWindow1()
        try:
            self.window1.show()
        except Exception as e:
            self.window1._save_btn_clicked()
            print(e)

        if os.path.exists(os.path.join(AssetsPath, 'last_loaded_dir_path.pkl')):
            self.window1.saved_dir_name = load_pickle(os.path.join(AssetsPath, 'last_loaded_dir_path.pkl'))
            self.window1._base_load(self.window1.saved_dir_name)
            self.window1._enable_some_buttons()
        else:
            self.window1.status_bar.showMessage('缺失关键文件！请手动加载！')

    else:
        # 隐藏控件
        self.hide()

        self.window1 = MyWindow1()
        self.window1.show()

        self.window1._load_btn_clicked()

