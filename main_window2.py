import os.path
import time

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from someConstant import AssetsPath, IncludeIcon, QuestionIcon, ExcludeIcon, AppIcon, StyleSheet
from utils import parse_xml, load_xml, save_pickle, load_pickle, export_selected_refs, translated_content,is_chinese


class MyWindow2(QWidget):
    def __init__(self, *args, **kwargs):
        super(MyWindow2, self).__init__(*args, **kwargs)
        self.setWindowTitle('文献分类')
        self.initWidgets()
        self.widgetsAdjust()
        self.bind_signal_func()

    def initWidgets(self):
        """
        初始化控件
        """
        # 上边控件
        layout_up = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self.list_view = QListWidget()
        layout_up.addWidget(self.list_view)

        # 下边控件
        layout_parse_load_switch = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self.switch_btn = QPushButton('模式切换')
        self.parse_btn = QPushButton('解析')
        self.load_btn = QPushButton('加载')
        layout_parse_load_switch.addWidget(self.parse_btn)
        layout_parse_load_switch.addWidget(self.load_btn)
        layout_parse_load_switch.addWidget(self.switch_btn)

        layout_down_btn = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self.last_btn = QPushButton('上一篇')
        self.next_btn = QPushButton('下一篇')
        self.checkbox_include = QCheckBox('纳入')
        self.checkbox_question = QCheckBox('问题')
        self.checkbox_exclude = QCheckBox('排除')
        self.save_btn = QPushButton('保存')
        self.export_btn = QPushButton('导出')
        self.translate_switch = QCheckBox('自动翻译')
        layout_down_btn.addWidget(self.last_btn)
        layout_down_btn.addWidget(self.checkbox_include)
        layout_down_btn.addWidget(self.checkbox_question)
        layout_down_btn.addWidget(self.checkbox_exclude)
        layout_down_btn.addWidget(self.next_btn)
        layout_down_btn.addWidget(self.translate_switch)
        layout_down_btn.addWidget(self.save_btn)
        layout_down_btn.addWidget(self.export_btn)

        layout_down = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        self.status_bar = QStatusBar()
        layout_down.addLayout(layout_down_btn)
        layout_down.addWidget(self.status_bar)

        layout_all_down = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        layout_all_down.addLayout(layout_down)
        layout_all_down.addLayout(layout_parse_load_switch)

        layout_final = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        layout_final.addLayout(layout_up)
        layout_final.addLayout(layout_all_down)

        self.setLayout(layout_final)

    def widgetsAdjust(self):
        """
        调整控件初始化参数
        """
        self.include_icon = QIcon(IncludeIcon)
        self.question_icon = QIcon(QuestionIcon)
        self.exclude_icon = QIcon(ExcludeIcon)
        self.app_icon = QIcon(AppIcon)
        self.non_icon = QIcon()

        self.checkbox_include.setIcon(self.include_icon)
        self.checkbox_include.setAutoExclusive(True)

        self.checkbox_question.setIcon(self.question_icon)
        self.checkbox_question.setAutoExclusive(True)

        self.checkbox_exclude.setIcon(self.exclude_icon)
        self.checkbox_exclude.setAutoExclusive(True)

        # 禁用一些控件
        self._disable_some_buttons()

        # 设置状态栏文字
        font = QFont()
        font.setPointSizeF(13.0)
        font.setFamily('微软雅黑')
        self.status_bar.setFont(font)
        self.status_bar.showMessage('Ready!')

        # 设置控件的ID
        self.list_view.setObjectName('list_view2')
        self.switch_btn.setObjectName('switch_btn2')

        # 设置list_view为多选模式
        self.list_view.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        self.saved_dir_name = None
        self.trans_flag = False
        self.showMaximized()

    def bind_signal_func(self):
        self.parse_btn.clicked.connect(self._parse_btn_clicked)
        self.load_btn.clicked.connect(self._load_btn_clicked)

        self.list_view.itemClicked.connect(self._list_view_itemClicked)
        # self.list_view.currentItemChanged.connect(self._list_view_currentItemChanged)

        self.last_btn.clicked.connect(self._last_btn_clicked)
        self.next_btn.clicked.connect(self._next_btn_clicked)
        self.checkbox_include.toggled.connect(self._checkbox_include_toggled)
        self.checkbox_question.toggled.connect(self._checkbox_question_toggled)
        self.checkbox_exclude.toggled.connect(self._checkbox_exclude_toggled)
        self.save_btn.clicked.connect(self._save_btn_clicked)
        self.export_btn.clicked.connect(self._export_btn_clicked)
        self.switch_btn.clicked.connect(self._switch_btn_clicked)
        self.translate_switch.toggled.connect(self._translate_switch_toggled)

        self._bind_key_func()

    def _bind_key_func(self):
        shortcut_up = QShortcut(QKeySequence(Qt.Key.Key_Up), self)
        shortcut_up.activated.connect(self.last_btn.click)
        shortcut_left = QShortcut(QKeySequence(Qt.Key.Key_Left), self)
        shortcut_left.activated.connect(self.last_btn.click)

        shortcut_down = QShortcut(QKeySequence(Qt.Key.Key_Down), self)
        shortcut_down.activated.connect(self.next_btn.click)
        shortcut_right = QShortcut(QKeySequence(Qt.Key.Key_Right), self)
        shortcut_right.activated.connect(self.next_btn.click)

        self.checkbox_include.setShortcut(Qt.Key.Key_Z)
        self.checkbox_question.setShortcut(Qt.Key.Key_X)
        self.checkbox_exclude.setShortcut(Qt.Key.Key_C)

        self.save_btn.setShortcut('Ctrl+S')
        self.export_btn.setShortcut('Ctrl+Shift+S')

        self.switch_btn.setShortcut(Qt.Key.Key_K)

    def _translate_switch_toggled(self, checked):
        if checked:
            temp_low, temp_high = self._get_trans_index_range(self.curr_index)
            for i in range(temp_low, temp_high + 1):
                # 首先检查是否是英文
                if not is_chinese(self.items_list[i].text()[0]):
                    if self.info_list[i][2] != '翻译失败！' and self.info_list[i][2] != '':
                        text = self.items_list[i].text()
                        if text:
                            if '\n' not in text:
                                self.items_list[i].setText(text + '\n' + self.info_list[i][2])
                        else:
                            self.items_list[i].setText(self.info_list[i][2])
                    else:
                        contents = translated_content(self.items_list[i].text())
                        self.info_list[i][2] = contents
                        text = self.items_list[i].text()
                        if text:
                            if '\n' not in text:
                                self.items_list[i].setText(text + '\n' + self.info_list[i][2])
                        else:
                            self.items_list[i].setText(self.info_list[i][2])

    def _get_trans_index_range(self, index):
        temp_low = index - 5
        temp_high = index + 5

        if temp_low < 0:
            temp_low = 0
        if temp_high >= self.max_num:
            temp_high = self.max_num - 1
        return temp_low, temp_high

    def _list_view_itemClicked(self, current):
        self._translate_switch_toggled(self.trans_flag)
        self.selected_items = self.list_view.selectedItems()
        if len(self.selected_items) > 1:
            # 将复选框全部取消勾选
            # 断开信号
            self.checkbox_include.toggled.disconnect(self._checkbox_include_toggled)
            self.checkbox_question.toggled.disconnect(self._checkbox_question_toggled)
            self.checkbox_exclude.toggled.disconnect(self._checkbox_exclude_toggled)

            self.checkbox_include.setAutoExclusive(False)
            self.checkbox_question.setAutoExclusive(False)
            self.checkbox_exclude.setAutoExclusive(False)

            # 设置checkbox状态
            self.checkbox_include.setChecked(False)
            self.checkbox_question.setChecked(False)
            self.checkbox_exclude.setChecked(False)

            # 恢复信号
            self.checkbox_include.setAutoExclusive(True)
            self.checkbox_question.setAutoExclusive(True)
            self.checkbox_exclude.setAutoExclusive(True)

            self.checkbox_include.toggled.connect(self._checkbox_include_toggled)
            self.checkbox_question.toggled.connect(self._checkbox_question_toggled)
            self.checkbox_exclude.toggled.connect(self._checkbox_exclude_toggled)
        else:
            # 更新索引和当前选择的item
            self.curr_index = current.data(666)
            self.curr_item = current

            # 更新checkbox状态
            self._set_checkbox_status()

    def __list_view_currentItemChanged(self, current, _):
        self._list_view_itemClicked(current)

    def _switch_btn_clicked(self):
        pass

    def _disable_some_buttons(self):
        self.last_btn.setDisabled(True)
        self.checkbox_include.setDisabled(True)
        self.checkbox_question.setDisabled(True)
        self.checkbox_exclude.setDisabled(True)
        self.next_btn.setDisabled(True)
        self.save_btn.setDisabled(True)
        self.export_btn.setDisabled(True)

    def _enable_some_buttons(self):
        self.last_btn.setEnabled(True)
        self.checkbox_include.setEnabled(True)
        self.checkbox_question.setEnabled(True)
        self.checkbox_exclude.setEnabled(True)
        self.next_btn.setEnabled(True)
        self.save_btn.setEnabled(True)
        self.export_btn.setEnabled(True)

    def _export_btn_clicked(self):
        if self.saved_dir_name:
            # 先保存文件
            self._save_btn_clicked()

            curr_time = str(int(time.time()))

            saved_xml_dir = QFileDialog.getExistingDirectory(self, "导出的文件存放于哪个文件夹？", '')

            # 导出纳入文献
            included_record_list = list(map(lambda x: self.record_text_list[x], self.included_set))
            if included_record_list:
                export_selected_refs(included_record_list, '纳入', saved_xml_dir)

            # 导出问题文献
            question_record_list = list(map(lambda x: self.record_text_list[x], self.question_set))
            if question_record_list:
                export_selected_refs(question_record_list, '问题', saved_xml_dir)

            # 导出排除文献
            excluded_record_list = list(map(lambda x: self.record_text_list[x], self.excluded_set))
            if excluded_record_list:
                export_selected_refs(excluded_record_list, '排除', saved_xml_dir)
        else:
            self.status_bar.showMessage('目前还不能导出！', 2000)

    def _save_btn_clicked(self):
        included_save_path = os.path.join(self.saved_dir_name, 'included_set.pkl')
        question_save_path = os.path.join(self.saved_dir_name, 'question_set.pkl')
        excluded_save_path = os.path.join(self.saved_dir_name, 'excluded_set.pkl')
        curr_index_save_path = os.path.join(self.saved_dir_name, 'saved_curr_index.pkl')
        info_list_save_path = os.path.join(self.saved_dir_name, 'info_list.pkl')
        last_loaded_dir_path = os.path.join(AssetsPath, 'last_loaded_dir_path.pkl')

        save_pickle(self.included_set, included_save_path)
        save_pickle(self.question_set, question_save_path)
        save_pickle(self.excluded_set, excluded_save_path)
        save_pickle(self.curr_index, curr_index_save_path)
        save_pickle(self.info_list, info_list_save_path)
        save_pickle(self.saved_dir_name, last_loaded_dir_path)

        self.status_bar.showMessage('已保存!', 2000)

    def _cancel_item_icon(self, item):
        if self.checkbox_include.isChecked():
            self._add_include_item_icon(item)
        elif self.checkbox_question.isChecked():
            self._add_question_item_icon(item)
        elif self.checkbox_exclude.isChecked():
            self._add_exclude_item_icon(item)
        else:
            item.setIcon(self.non_icon)
        # item.setIcon(self.non_icon)

    def _add_include_item_icon(self, item):
        item.setIcon(self.include_icon)

    def _add_question_item_icon(self, item):
        item.setIcon(self.question_icon)

    def _add_exclude_item_icon(self, item):
        item.setIcon(self.exclude_icon)

    def _checkbox_include_toggled(self, checked):
        print('yihui')
        if len(self.selected_items) > 1:
            if checked:
                for selected_item in self.selected_items:
                    curr_index = selected_item.data(666)
                    self.included_set.add(curr_index)
                    self._add_include_item_icon(selected_item)

                    # 手动实现互斥逻辑
                    if curr_index in self.question_set:
                        self.question_set.remove(curr_index)
                    if curr_index in self.excluded_set:
                        self.excluded_set.remove(curr_index)
            else:
                for selected_item in self.selected_items:
                    curr_index = selected_item.data(666)
                    self.included_set.remove(curr_index)
                    self._cancel_item_icon(selected_item)
        else:
            if checked:
                self.included_set.add(self.curr_index)
                self._add_include_item_icon(self.curr_item)
            else:
                self.included_set.remove(self.curr_index)
                self._cancel_item_icon(self.curr_item)

    def _checkbox_question_toggled(self, checked):
        if len(self.selected_items) > 1:
            if checked:
                for selected_item in self.selected_items:
                    curr_index = selected_item.data(666)
                    self.question_set.add(curr_index)
                    self._add_question_item_icon(selected_item)

                    # 手动实现互斥逻辑
                    if curr_index in self.included_set:
                        self.included_set.remove(curr_index)
                    if curr_index in self.excluded_set:
                        self.excluded_set.remove(curr_index)
            else:
                for selected_item in self.selected_items:
                    curr_index = selected_item.data(666)
                    self.question_set.remove(curr_index)
                    self._cancel_item_icon(selected_item)
        else:
            if checked:
                self.question_set.add(self.curr_index)
                self._add_question_item_icon(self.curr_item)
            else:
                self.question_set.remove(self.curr_index)
                self._cancel_item_icon(self.curr_item)

    def _checkbox_exclude_toggled(self, checked):
        if len(self.selected_items) > 1:
            if checked:
                for selected_item in self.selected_items:
                    curr_index = selected_item.data(666)
                    self.excluded_set.add(curr_index)
                    self._add_exclude_item_icon(selected_item)

                    # 手动实现互斥逻辑
                    if curr_index in self.included_set:
                        self.included_set.remove(curr_index)
                    if curr_index in self.question_set:
                        self.question_set.remove(curr_index)
            else:
                for selected_item in self.selected_items:
                    curr_index = selected_item.data(666)
                    self.excluded_set.remove(curr_index)
                    self._cancel_item_icon(selected_item)
        else:
            if checked:
                self.excluded_set.add(self.curr_index)
                self._add_exclude_item_icon(self.curr_item)
            else:
                self.excluded_set.remove(self.curr_index)
                self._cancel_item_icon(self.curr_item)

    def initData(self):
        self.max_num = len(self.info_list)

        # 加载列表
        self._no_filters()

        # 加载当前复选框的选择
        self._set_checkbox_status()

    def _no_filters(self):
        self.items_list = []
        for i in range(self.max_num):
            item = QListWidgetItem(self.info_list[i][0].replace('\n', ' '), self.list_view)

            # 设置item的一些属性
            item.setData(666, i)
            if i in self.included_set:
                item.setIcon(self.include_icon)
            elif i in self.question_set:
                item.setIcon(self.question_icon)
            elif i in self.excluded_set:
                item.setIcon(self.exclude_icon)

            self.items_list.append(item)

            font = QFont('Times New Roman', 12)
            item.setFont(font)

        self.list_view.setCurrentItem(self.items_list[self.curr_index])
        self._list_view_itemClicked(self.items_list[self.curr_index])

    def _open_file_dialog(self):
        xml_name, _ = QFileDialog.getOpenFileName(self, "请选择要解析的XML文件", "", "XML File (*.xml)")
        if xml_name:
            return xml_name

    def _open_dir_dialog(self):
        parsed_dir = QFileDialog.getExistingDirectory(self, "请选择要加载的文件夹", "")
        if parsed_dir:
            return parsed_dir

    def _last_btn_clicked(self):
        if self.curr_index == 0:
            self.curr_index = self.max_num - 1
        else:
            self.curr_index -= 1
        self.list_view.setCurrentItem(self.items_list[self.curr_index])
        self._list_view_itemClicked(self.items_list[self.curr_index])

    def _next_btn_clicked(self):
        if self.curr_index == self.max_num - 1:
            self.curr_index = 0
        else:
            self.curr_index += 1
        self.list_view.setCurrentItem(self.items_list[self.curr_index])
        self._list_view_itemClicked(self.items_list[self.curr_index])

    def _parse_btn_clicked(self):
        xml_name = self._open_file_dialog()
        if xml_name:
            self.saved_dir_name = parse_xml(xml_name)
        else:
            self.status_bar.showMessage('未选择XML文件，请重新解析数据！', 2000)  # 持续两秒

    def _load_btn_clicked(self):
        # 先将当前列表清空
        self.list_view.itemClicked.disconnect(self._list_view_itemClicked)
        self.list_view.clear()
        self.list_view.itemClicked.connect(self._list_view_itemClicked)

        # 添加对话框，对应两种不同的加载方式
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle('加载方式选择')
        msg_box.setText('请选择一种数据的加载方法')
        load_btn1 = msg_box.addButton('使用上次解析的数据', QMessageBox.ButtonRole.ActionRole)
        load_btn2 = msg_box.addButton('加载新数据...', QMessageBox.ButtonRole.ActionRole)
        load_btn3 = msg_box.addButton('点错了, 放弃加载', QMessageBox.ButtonRole.RejectRole)
        msg_box.setDefaultButton(load_btn1)
        msg_box.exec()

        # Check which button was clicked
        clicked_button = msg_box.clickedButton()
        if clicked_button == load_btn1:
            # 加载上次解析的目录，分两种情况：刚刚解析、上一次解析
            if self.saved_dir_name:  # 刚刚解析
                self._base_load(self.saved_dir_name)
            else:  # 上一次解析
                if not os.path.exists(os.path.join(AssetsPath, 'last_loaded_dir_path.pkl')):
                    self.saved_dir_name = None
                else:
                    self.saved_dir_name = load_pickle(os.path.join(AssetsPath, 'last_loaded_dir_path.pkl'))
                self._base_load(self.saved_dir_name)
            # 恢复一些控件
            self._enable_some_buttons()
        elif clicked_button == load_btn2:
            self.saved_dir_name = self._open_dir_dialog()
            self._base_load(self.saved_dir_name)
            # 恢复一些控件
            self._enable_some_buttons()
        elif clicked_button == load_btn3:
            self.status_bar.showMessage('取消加载数据！', 2000)  # 持续两秒

    def _base_load(self, saved_dir_name):
        if saved_dir_name:
            self.info_list, self.record_text_list = load_xml(saved_dir_name)
            # 加载分组数据
            if not os.path.exists(os.path.join(saved_dir_name, 'included_set.pkl')):
                self.included_set = set()
            else:
                self.included_set = load_pickle(os.path.join(saved_dir_name, 'included_set.pkl'))

            if not os.path.exists(os.path.join(saved_dir_name, 'question_set.pkl')):
                self.question_set = set()
            else:
                self.question_set = load_pickle(os.path.join(saved_dir_name, 'question_set.pkl'))

            if not os.path.exists(os.path.join(saved_dir_name, 'excluded_set.pkl')):
                self.excluded_set = set()
            else:
                self.excluded_set = load_pickle(os.path.join(saved_dir_name, 'excluded_set.pkl'))

            # 加载上次查看索引
            if not os.path.exists(os.path.join(saved_dir_name, 'saved_curr_index.pkl')):
                self.curr_index = 0
            else:
                self.curr_index = load_pickle(os.path.join(saved_dir_name, 'saved_curr_index.pkl'))

            self.initData()
        else:
            self.status_bar.showMessage('请重新加载数据或先解析数据！', 5000)  # 持续五秒

    def _set_checkbox_status(self):
        self.trans_flag = True
        # 断开信号
        self.checkbox_include.toggled.disconnect(self._checkbox_include_toggled)
        self.checkbox_question.toggled.disconnect(self._checkbox_question_toggled)
        self.checkbox_exclude.toggled.disconnect(self._checkbox_exclude_toggled)

        self.checkbox_include.setAutoExclusive(False)
        self.checkbox_question.setAutoExclusive(False)
        self.checkbox_exclude.setAutoExclusive(False)

        # 设置checkbox状态
        self.checkbox_include.setChecked(False)
        self.checkbox_question.setChecked(False)
        self.checkbox_exclude.setChecked(False)

        if self.curr_index in self.included_set:
            self.checkbox_include.setChecked(True)
        if self.curr_index in self.question_set:
            self.checkbox_question.setChecked(True)
        if self.curr_index in self.excluded_set:
            self.checkbox_exclude.setChecked(True)

        # 恢复信号
        self.checkbox_include.setAutoExclusive(True)
        self.checkbox_question.setAutoExclusive(True)
        self.checkbox_exclude.setAutoExclusive(True)

        self.checkbox_include.toggled.connect(self._checkbox_include_toggled)
        self.checkbox_question.toggled.connect(self._checkbox_question_toggled)
        self.checkbox_exclude.toggled.connect(self._checkbox_exclude_toggled)

    def closeEvent(self, event):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle('退出前确认')
        msg_box.setText('真的要退出吗？')
        close_btn1 = msg_box.addButton('保存并退出', QMessageBox.ButtonRole.ActionRole)
        close_btn2 = msg_box.addButton('不保存并退出', QMessageBox.ButtonRole.ActionRole)
        close_btn3 = msg_box.addButton('点错了，不退出', QMessageBox.ButtonRole.RejectRole)
        msg_box.setDefaultButton(close_btn3)
        msg_box.exec()

        # Check which button was clicked
        clicked_button = msg_box.clickedButton()
        if clicked_button == close_btn1:
            if self.saved_dir_name:
                self._save_btn_clicked()
                QApplication.quit()
            else:
                QApplication.quit()
        elif clicked_button == close_btn2:
            QApplication.quit()
        elif clicked_button == close_btn3:
            event.ignore()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    # 设置样式
    with open(StyleSheet, 'r', 1, 'utf-8') as f:
        app.setStyleSheet(f.read())

    # 设置窗口图标
    app_icon = QIcon(AppIcon)
    app.setWindowIcon(app_icon)

    window = MyWindow2()
    window.show()
    sys.exit(app.exec())
