import os.path
import time
import copy

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from someConstant import AssetsPath, IncludeIcon, QuestionIcon, ExcludeIcon, AppIcon, StyleSheet
from utils import parse_xml, load_xml, is_chinese, save_pickle, load_pickle, export_selected_refs


class MyWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super(MyWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle('文献分类')
        self.initWidgets()
        self.widgetsAdjust()
        self.bind_signal_func()

    def initWidgets(self):
        """
        初始化控件
        """
        # 左上角控件
        layout_title_zh = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        title_zh_label = QLabel('标题')
        self.copy_zh_btn = QPushButton('复制')
        self.translate_zh_btn = QPushButton('翻译')
        layout_title_zh.addWidget(title_zh_label)
        layout_title_zh.addWidget(self.copy_zh_btn)
        layout_title_zh.addWidget(self.translate_zh_btn)

        layout_title_all_zh = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self.title_text_zh = QTextEdit()
        layout_title_all_zh.addLayout(layout_title_zh)
        layout_title_all_zh.addWidget(self.title_text_zh)

        # 右上角控件
        layout_title_en = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        title_en_label = QLabel('Title')
        self.copy_en_btn = QPushButton('Copy')
        self.translate_en_btn = QPushButton('Translate')
        layout_title_en.addWidget(title_en_label)
        layout_title_en.addWidget(self.copy_en_btn)
        layout_title_en.addWidget(self.translate_en_btn)

        layout_title_all_en = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self.title_text_en = QTextEdit()
        layout_title_all_en.addLayout(layout_title_en)
        layout_title_all_en.addWidget(self.title_text_en)

        # 左下角控件
        layout_abs_zh = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        abs_zh_label = QLabel('摘要')
        self.copy_zh_abs_btn = QPushButton('复制')
        self.translate_zh_abs_btn = QPushButton('翻译')
        layout_abs_zh.addWidget(abs_zh_label)
        layout_abs_zh.addWidget(self.copy_zh_abs_btn)
        layout_abs_zh.addWidget(self.translate_zh_abs_btn)

        layout_abs_all_zh = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self.abs_text_zh = QTextEdit()
        layout_abs_all_zh.addLayout(layout_abs_zh)
        layout_abs_all_zh.addWidget(self.abs_text_zh)

        # 右下角控件
        layout_abs_en = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        abs_en_label = QLabel('Abstract')
        self.copy_en_abs_btn = QPushButton('Copy')
        self.translate_en_abs_btn = QPushButton('Translate')
        layout_abs_en.addWidget(abs_en_label)
        layout_abs_en.addWidget(self.copy_en_abs_btn)
        layout_abs_en.addWidget(self.translate_en_abs_btn)

        layout_abs_all_en = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self.abs_text_en = QTextEdit()
        layout_abs_all_en.addLayout(layout_abs_en)
        layout_abs_all_en.addWidget(self.abs_text_en)

        # 下边控件
        layout_down_btn = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self.last_btn = QPushButton('上一篇')
        self.next_btn = QPushButton('下一篇')
        self.checkbox_include = QCheckBox('纳入')
        self.checkbox_question = QCheckBox('问题')
        self.checkbox_exclude = QCheckBox('排除')
        self.save_btn = QPushButton('保存')
        self.export_btn = QPushButton('导出')
        layout_down_btn.addWidget(self.last_btn)
        layout_down_btn.addWidget(self.checkbox_include)
        layout_down_btn.addWidget(self.checkbox_question)
        layout_down_btn.addWidget(self.checkbox_exclude)
        layout_down_btn.addWidget(self.next_btn)
        layout_down_btn.addWidget(self.save_btn)
        layout_down_btn.addWidget(self.export_btn)

        layout_down = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        self.status_bar = QStatusBar()
        layout_down.addLayout(layout_down_btn)
        layout_down.addWidget(self.status_bar)

        # 右侧控件
        layout_parse_load_switch = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self.switch_btn = QPushButton('模式切换')
        self.parse_btn = QPushButton('解析')
        self.load_btn = QPushButton('加载')
        layout_parse_load_switch.addWidget(self.parse_btn)
        layout_parse_load_switch.addWidget(self.load_btn)
        layout_parse_load_switch.addWidget(self.switch_btn)

        layout_filter = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self.filter = QComboBox()
        self.label = QLabel('过滤器：')
        layout_filter.addWidget(self.label, 1)
        layout_filter.addWidget(self.filter, 9)

        layout_filter_list_switch = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        self.list_view = QListWidget()
        layout_filter_list_switch.addLayout(layout_filter)
        layout_filter_list_switch.addWidget(self.list_view)
        layout_filter_list_switch.addLayout(layout_parse_load_switch)

        # 布局合并
        layout_upper_left_and_right = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        layout_upper_left_and_right.addLayout(layout_title_all_zh)
        layout_upper_left_and_right.addLayout(layout_title_all_en)

        layout_down_left_and_right = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        layout_down_left_and_right.addLayout(layout_abs_all_zh)
        layout_down_left_and_right.addLayout(layout_abs_all_en)

        layout_four_main_widgets = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        layout_four_main_widgets.addLayout(layout_upper_left_and_right, 3)
        layout_four_main_widgets.addLayout(layout_down_left_and_right, 5)

        layout_upper_down = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        layout_upper_down.addLayout(layout_four_main_widgets)
        layout_upper_down.addLayout(layout_down)

        self.layout_final = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self.layout_final.addLayout(layout_upper_down, 8)
        self.layout_final.addLayout(layout_filter_list_switch, 2)

        self.initWidgets2()

    def initWidgets2(self):
        # 上边控件
        layout_up = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self.list_view2 = QListWidget()
        layout_up.addWidget(self.list_view2)

        # 下边控件
        layout_parse_load_switch = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self.switch_btn2 = QPushButton('模式切换')
        self.parse_btn2 = QPushButton('解析')
        self.load_btn2 = QPushButton('加载')
        layout_parse_load_switch.addWidget(self.parse_btn2)
        layout_parse_load_switch.addWidget(self.load_btn2)
        layout_parse_load_switch.addWidget(self.switch_btn2)

        layout_down_btn = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self.last_btn2 = QPushButton('上一篇')
        self.next_btn2 = QPushButton('下一篇')
        self.checkbox_include2 = QCheckBox('纳入')
        self.checkbox_question2 = QCheckBox('问题')
        self.checkbox_exclude2 = QCheckBox('排除')
        self.save_btn2 = QPushButton('保存')
        self.export_btn2 = QPushButton('导出')
        layout_down_btn.addWidget(self.last_btn2)
        layout_down_btn.addWidget(self.checkbox_include2)
        layout_down_btn.addWidget(self.checkbox_question2)
        layout_down_btn.addWidget(self.checkbox_exclude2)
        layout_down_btn.addWidget(self.next_btn2)
        layout_down_btn.addWidget(self.save_btn2)
        layout_down_btn.addWidget(self.export_btn2)

        layout_down = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        self.status_bar2 = QStatusBar()
        layout_down.addLayout(layout_down_btn)
        layout_down.addWidget(self.status_bar2)

        layout_all_down = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        layout_all_down.addLayout(layout_down)
        layout_all_down.addLayout(layout_parse_load_switch)

        self.layout_final2 = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        self.layout_final2.addLayout(layout_up)
        self.layout_final2.addLayout(layout_all_down)

        self.initWidgetsFinal()

    def initWidgetsFinal(self):
        layout_self = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self.stacked_widget = QStackedWidget()
        layout_self.addWidget(self.stacked_widget)

        # Page 1
        page1 = QWidget()
        page1.setLayout(self.layout_final)
        self.stacked_widget.addWidget(page1)

        # Page 2
        page2 = QWidget()
        page2.setLayout(self.layout_final2)
        self.stacked_widget.addWidget(page2)

        self.setLayout(layout_self)
        self.showMaximized()

    def widgetsAdjust(self):
        """
        调整控件初始化参数
        """
        self.title_text_zh.setText('你好')
        self.title_text_en.setText('hello')
        self.abs_text_zh.setText('你好，世界！')
        self.abs_text_en.setText('hello world')

        self.include_icon = QIcon(IncludeIcon)
        self.question_icon = QIcon(QuestionIcon)
        self.exclude_icon = QIcon(ExcludeIcon)
        self.app_icon = QIcon(AppIcon)
        self.non_icon = QIcon()

        self.checkbox_include.setIcon(self.include_icon)
        self.checkbox_include2.setIcon(self.include_icon)
        self.checkbox_include.setAutoExclusive(True)
        self.checkbox_include2.setAutoExclusive(True)

        self.checkbox_question.setIcon(self.question_icon)
        self.checkbox_question2.setIcon(self.question_icon)
        self.checkbox_question.setAutoExclusive(True)
        self.checkbox_question2.setAutoExclusive(True)

        self.checkbox_exclude.setIcon(self.exclude_icon)
        self.checkbox_exclude2.setIcon(self.exclude_icon)
        self.checkbox_exclude.setAutoExclusive(True)
        self.checkbox_exclude2.setAutoExclusive(True)

        self.title_text_zh.setReadOnly(True)
        self.title_text_en.setReadOnly(True)
        self.abs_text_zh.setReadOnly(True)
        self.abs_text_en.setReadOnly(True)

        # combobox初始化
        self.filter.setEditable(False)
        self.filter.setDuplicatesEnabled(False)
        self.filter.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.filter.addItem(self.non_icon, '（不过滤）')  # 0
        self.filter.addItem(self.include_icon, '纳入')  # 1
        self.filter.addItem(self.question_icon, '问题')  # 2
        self.filter.addItem(self.exclude_icon, '排除')  # 3
        self.filter.addItem(self.non_icon, '（未分类）')  # 4

        # 禁用一些控件
        self._disable_some_buttons()

        # 设置状态栏文字
        font = QFont()
        font.setPointSizeF(13.0)
        font.setFamily('微软雅黑')
        self.status_bar.setFont(font)
        self.status_bar2.setFont(font)
        self.status_bar.showMessage('Ready!')
        self.status_bar2.showMessage('Ready!')

        self.saved_dir_name = None



    def bind_signal_func(self):
        self.parse_btn.clicked.connect(self._parse_btn_clicked)
        self.load_btn.clicked.connect(self._load_btn_clicked)
        self.list_view.currentItemChanged.connect(self._item_changed)
        self.last_btn.clicked.connect(self._last_btn_clicked)
        self.next_btn.clicked.connect(self._next_btn_clicked)
        self.copy_zh_btn.clicked.connect(self._copy_zh_btn_clicked)
        self.copy_en_btn.clicked.connect(self._copy_en_btn_clicked)
        self.copy_zh_abs_btn.clicked.connect(self._copy_zh_abs_btn_clicked)
        self.copy_en_abs_btn.clicked.connect(self._copy_en_abs_btn_clicked)
        self.checkbox_include.toggled.connect(self._checkbox_include_toggled)
        self.checkbox_question.toggled.connect(self._checkbox_question_toggled)
        self.checkbox_exclude.toggled.connect(self._checkbox_exclude_toggled)
        self.save_btn.clicked.connect(self._save_btn_clicked)
        self.export_btn.clicked.connect(self._export_btn_clicked)
        self.filter.activated.connect(self._filter_activated)
        self.translate_zh_btn.clicked.connect(self._translate_zh_btn_clicked)
        self.switch_btn.clicked.connect(self._switch_btn_clicked)

        self.parse_btn2.clicked.connect(self._parse_btn_clicked2)
        self.load_btn2.clicked.connect(self._load_btn_clicked2)
        self.list_view2.currentItemChanged.connect(self._item_changed2)
        self.last_btn2.clicked.connect(self._last_btn_clicked2)
        self.next_btn2.clicked.connect(self._next_btn_clicked2)
        self.checkbox_include2.toggled.connect(self._checkbox_include_toggled2)
        self.checkbox_question2.toggled.connect(self._checkbox_question_toggled2)
        self.checkbox_exclude2.toggled.connect(self._checkbox_exclude_toggled2)
        self.save_btn.clicked2.connect(self._save_btn_clicked2)
        self.export_btn.clicked2.connect(self._export_btn_clicked2)
        self.switch_btn.clicked2.connect(self._switch_btn_clicked2)

        self._bind_key_func()

    def _parse_btn_clicked2(self):
        xml_name = self._open_file_dialog()
        if xml_name:
            self.saved_dir_name = parse_xml(xml_name)
        else:
            self.status_bar2.showMessage('未选择XML文件，请重新解析数据！', 2000)  # 持续两秒

    def _load_btn_clicked2(self):
        # 先将当前列表清空
        self.list_view2.currentItemChanged.disconnect(self._item_changed2)
        self.list_view2.clear()
        self.list_view2.currentItemChanged.connect(self._item_changed2)

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

    def _item_changed2(self):
        # 更新索引和当前选择的item
        self.curr_index = current.data(666)
        self.curr_item = current

        # 更新checkbox状态
        self._set_checkbox_status()

    def _last_btn_clicked2(self):
        pass

    def _next_btn_clicked2(self):
        pass

    def _checkbox_include_toggled2(self):
        pass

    def _checkbox_question_toggled2(self):
        pass

    def _checkbox_exclude_toggled2(self):
        pass

    def _save_btn_clicked2(self):
        pass

    def _export_btn_clicked2(self):
        pass

    def _switch_btn_clicked2(self):
        pass

    def _switch_btn_clicked(self):
            self.stacked_widget.setCurrentIndex(1)

    def _translate_zh_btn_clicked(self):
        pass

    def _filter_activated(self, index):
        if index == 1:
            self.list_view.currentItemChanged.disconnect(self._item_changed)
            self.list_view.clear()
            self._add_filtered_items('include')
        elif index == 2:
            self.list_view.currentItemChanged.disconnect(self._item_changed)
            self.list_view.clear()
            self._add_filtered_items('question')
        elif index == 3:
            self.list_view.currentItemChanged.disconnect(self._item_changed)
            self.list_view.clear()
            self._add_filtered_items('exclude')
        elif index == 4:
            self.list_view.currentItemChanged.disconnect(self._item_changed)
            self.list_view.clear()
            self._add_filtered_items('unsorted')
        elif index == 0:
            self.list_view.currentItemChanged.disconnect(self._item_changed)
            self.list_view.clear()
            self._no_filters()
            self.list_view.currentItemChanged.connect(self._item_changed)

    def _add_filtered_items(self, category):
        temp_num = set()
        if category == 'include':
            temp_num = self.included_set
        elif category == 'question':
            temp_num = self.question_set
        elif category == 'exclude':
            temp_num = self.excluded_set
        elif category == 'unsorted':
            unsorted_set = set(range(self.max_num))
            if not len(self.included_set) == 0:
                list(map(lambda x: unsorted_set.remove(x), self.included_set))
            if not len(self.question_set) == 0:
                list(map(lambda x: unsorted_set.remove(x), self.question_set))
            if not len(self.excluded_set) == 0:
                list(map(lambda x: unsorted_set.remove(x), self.excluded_set))
            temp_num = unsorted_set

        if temp_num:
            self.items_list = []
            for i in temp_num:
                item = QListWidgetItem(self.info_list[i][0].replace('\n', ' '), self.list_view)

                # 设置item的一些属性
                item.setData(666, i)
                if i in self.included_set:
                    item.setIcon(self.include_icon)
                elif i in self.question_set:
                    item.setIcon(self.question_icon)
                elif i in self.excluded_set:
                    item.setIcon(self.exclude_icon)

                font = QFont('Times New Roman', 16)
                item.setFont(font)

                self.items_list.append(item)

            self.list_view.currentItemChanged.connect(self._item_changed)
            self.list_view.setCurrentItem(self.items_list[0])
        else:
            self.list_view.clear()
            self.list_view.currentItemChanged.connect(self._item_changed)

    def _disable_some_buttons(self):
        self.last_btn.setDisabled(True)
        self.last_btn2.setDisabled(True)

        self.checkbox_include.setDisabled(True)
        self.checkbox_include2.setDisabled(True)

        self.checkbox_question.setDisabled(True)
        self.checkbox_question2.setDisabled(True)

        self.checkbox_exclude.setDisabled(True)
        self.checkbox_exclude2.setDisabled(True)

        self.next_btn.setDisabled(True)
        self.next_btn2.setDisabled(True)

        self.save_btn.setDisabled(True)
        self.save_btn2.setDisabled(True)

        self.export_btn.setDisabled(True)
        self.export_btn2.setDisabled(True)

        self.filter.setDisabled(True)

    def _enable_some_buttons(self):
        self.last_btn.setEnabled(True)
        self.last_btn2.setEnabled(True)

        self.checkbox_include.setEnabled(True)
        self.checkbox_include2.setEnabled(True)

        self.checkbox_question.setEnabled(True)
        self.checkbox_question2.setEnabled(True)

        self.checkbox_exclude.setEnabled(True)
        self.checkbox_exclude2.setEnabled(True)

        self.next_btn.setEnabled(True)
        self.next_btn2.setEnabled(True)

        self.save_btn.setEnabled(True)
        self.save_btn2.setEnabled(True)

        self.export_btn.setEnabled(True)
        self.export_btn2.setEnabled(True)

        self.filter.setEnabled(True)

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
        last_loaded_dir_path = os.path.join(AssetsPath, 'last_loaded_dir_path.pkl')

        save_pickle(self.included_set, included_save_path)
        save_pickle(self.question_set, question_save_path)
        save_pickle(self.excluded_set, excluded_save_path)
        save_pickle(self.curr_index, curr_index_save_path)
        save_pickle(self.saved_dir_name, last_loaded_dir_path)

        self.status_bar.showMessage('已保存!', 2000)

    def _cancel_item_icon(self):
        if self.checkbox_include.isChecked():
            self._add_include_item_icon()
        elif self.checkbox_question.isChecked():
            self._add_question_item_icon()
        elif self.checkbox_exclude.isChecked():
            self._add_exclude_item_icon()
        else:
            self.curr_item.setIcon(self.non_icon)

    def _add_include_item_icon(self):
        self.curr_item.setIcon(self.include_icon)

    def _add_question_item_icon(self):
        self.curr_item.setIcon(self.question_icon)

    def _add_exclude_item_icon(self):
        self.curr_item.setIcon(self.exclude_icon)

    def _checkbox_include_toggled(self, checked):
        if checked:
            self.included_set.add(self.curr_index)
            self._add_include_item_icon()
        else:
            self.included_set.remove(self.curr_index)
            self._cancel_item_icon()

    def _checkbox_question_toggled(self, checked):
        if checked:
            self.question_set.add(self.curr_index)
            self._add_question_item_icon()
        else:
            self.question_set.remove(self.curr_index)
            self._cancel_item_icon()

    def _checkbox_exclude_toggled(self, checked):
        if checked:
            self.excluded_set.add(self.curr_index)
            self._add_exclude_item_icon()
        else:
            self.excluded_set.remove(self.curr_index)
            self._cancel_item_icon()

    def _copy_zh_btn_clicked(self):
        self._copy_text(self.title_text_zh.toPlainText())

    def _copy_en_btn_clicked(self):
        self._copy_text(self.title_text_en.toPlainText())

    def _copy_zh_abs_btn_clicked(self):
        self._copy_text(self.abs_text_zh.toPlainText())

    def _copy_en_abs_btn_clicked(self):
        self._copy_text(self.abs_text_en.toPlainText())

    def initData(self):
        self.max_num = len(self.info_list)

        # 加载列表
        self._no_filters()

        # 加载当前复选框的选择
        self._set_checkbox_status()

    def initData2(self):
        self.max_num = len(self.info_list)

        # 加载列表
        self._no_filters2()

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

            font = QFont('Times New Roman', 16)
            item.setFont(font)

        self.list_view.setCurrentItem(self.items_list[self.curr_index])

    def _no_filters2(self):
        self.items_list = []
        for i in range(self.max_num):
            item = QListWidgetItem(self.info_list[i][0].replace('\n', ' '), self.list_view2)

            # 设置item的一些属性
            item.setData(666, i)
            if i in self.included_set:
                item.setIcon(self.include_icon)
            elif i in self.question_set:
                item.setIcon(self.question_icon)
            elif i in self.excluded_set:
                item.setIcon(self.exclude_icon)

            self.items_list.append(item)

            font = QFont('Times New Roman', 16)
            item.setFont(font)

        self.list_view2.setCurrentItem(self.items_list[self.curr_index])

    def _open_file_dialog(self):
        xml_name, _ = QFileDialog.getOpenFileName(self, "请选择要解析的XML文件", "", "XML File (*.xml)")
        if xml_name:
            return xml_name

    def _open_dir_dialog(self):
        parsed_dir = QFileDialog.getExistingDirectory(self, "请选择要加载的文件夹", "")
        if parsed_dir:
            return parsed_dir

    def _copy_text(self, text):
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            self.status_bar.showMessage('已成功复制！', 2000)
        else:
            self.status_bar.showMessage('复制内容为空！', 2000)

    def _last_btn_clicked(self):
        if self.curr_index == 0:
            self.curr_index = self.max_num - 1
        else:
            self.curr_index -= 1
        self.list_view.setCurrentItem(self.items_list[self.curr_index])

    def _next_btn_clicked(self):
        if self.curr_index == self.max_num - 1:
            self.curr_index = 0
        else:
            self.curr_index += 1
        self.list_view.setCurrentItem(self.items_list[self.curr_index])

    def _parse_btn_clicked(self):
        xml_name = self._open_file_dialog()
        if xml_name:
            self.saved_dir_name = parse_xml(xml_name)
        else:
            self.status_bar.showMessage('未选择XML文件，请重新解析数据！', 2000)  # 持续两秒

    def _load_btn_clicked(self):
        # 先将当前列表清空
        self.list_view.currentItemChanged.disconnect(self._item_changed)
        self.list_view.clear()
        self.list_view.currentItemChanged.connect(self._item_changed)

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

    def _update_spec_data(self, index):
        # 四大框中写入数据
        curr_title = self.info_list[index][0]

        curr_abstract = self.info_list[index][1]

        self.title_text_zh.clear()
        self.abs_text_zh.clear()
        self.title_text_en.clear()
        self.abs_text_en.clear()

        if is_chinese(curr_title[0]):
            self.title_text_zh.setText(curr_title)
            self.abs_text_zh.setText(curr_abstract)
        else:
            self.title_text_en.setText(curr_title)
            self.abs_text_en.setText(curr_abstract)

    def _item_changed(self, current, _):
        # 更新索引和当前选择的item
        self.curr_index = current.data(666)
        self.curr_item = current

        # 更新checkbox状态
        self._set_checkbox_status()

        # 更新文本框内容
        self._update_spec_data(self.curr_index)

    def _set_checkbox_status(self):
        # 断开信号
        self.checkbox_include.toggled.disconnect(self._checkbox_include_toggled)
        self.checkbox_include2.toggled.disconnect(self._checkbox_include_toggled)
        self.checkbox_question.toggled.disconnect(self._checkbox_question_toggled)
        self.checkbox_question2.toggled.disconnect(self._checkbox_question_toggled)
        self.checkbox_exclude.toggled.disconnect(self._checkbox_exclude_toggled)
        self.checkbox_exclude2.toggled.disconnect(self._checkbox_exclude_toggled)

        self.checkbox_include.setAutoExclusive(False)
        self.checkbox_include2.setAutoExclusive(False)
        self.checkbox_question.setAutoExclusive(False)
        self.checkbox_question2.setAutoExclusive(False)
        self.checkbox_exclude.setAutoExclusive(False)
        self.checkbox_exclude2.setAutoExclusive(False)

        # 设置checkbox状态
        self.checkbox_include.setChecked(False)
        self.checkbox_include2.setChecked(False)
        self.checkbox_question.setChecked(False)
        self.checkbox_question2.setChecked(False)
        self.checkbox_exclude.setChecked(False)
        self.checkbox_exclude2.setChecked(False)

        if self.curr_index in self.included_set:
            self.checkbox_include.setChecked(True)
            self.checkbox_include2.setChecked(True)
        if self.curr_index in self.question_set:
            self.checkbox_question.setChecked(True)
            self.checkbox_question2.setChecked(True)
        if self.curr_index in self.excluded_set:
            self.checkbox_exclude.setChecked(True)
            self.checkbox_exclude2.setChecked(True)

        # 恢复信号
        self.checkbox_include.setAutoExclusive(True)
        self.checkbox_include2.setAutoExclusive(True)
        self.checkbox_question.setAutoExclusive(True)
        self.checkbox_question2.setAutoExclusive(True)
        self.checkbox_exclude.setAutoExclusive(True)
        self.checkbox_exclude2.setAutoExclusive(True)

        self.checkbox_include.toggled.connect(self._checkbox_include_toggled)
        self.checkbox_include2.toggled.connect(self._checkbox_include_toggled)
        self.checkbox_question.toggled.connect(self._checkbox_question_toggled)
        self.checkbox_question2.toggled.connect(self._checkbox_question_toggled)
        self.checkbox_exclude.toggled.connect(self._checkbox_exclude_toggled)
        self.checkbox_exclude2.toggled.connect(self._checkbox_exclude_toggled)

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

        self.copy_zh_btn.setShortcut('Ctrl+V')
        self.translate_zh_btn.setShortcut(Qt.Key.Key_V)

        self.copy_en_btn.setShortcut('Ctrl+D')
        self.translate_en_btn.setShortcut(Qt.Key.Key_D)

        self.copy_zh_abs_btn.setShortcut('Ctrl+B')
        self.translate_zh_abs_btn.setShortcut(Qt.Key.Key_B)

        self.copy_en_abs_btn.setShortcut('Ctrl+F')
        self.translate_en_abs_btn.setShortcut(Qt.Key.Key_F)

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

    window = MyWindow()
    window.show()
    sys.exit(app.exec())
