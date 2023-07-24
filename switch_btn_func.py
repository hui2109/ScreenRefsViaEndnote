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
