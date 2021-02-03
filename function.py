# -*- coding: utf-8 -*-

#Provide function logic for UI

from UI import Ui_MainWindow
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import configparser
import os
from nlp import *

class window(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        #read configs
        self.source,self.save,self.mode=self.init_configs()

        self.filename=''
        self.result=[]
        self.num=0
        self.init_window()

        #slot functions
        self.pushButton.clicked.connect(self.func_last)
        self.pushButton_2.clicked.connect(self.func_next)
        self.pushButton_3.clicked.connect(self.func_save)

        self.actionFile_Directory.triggered.connect(self.func_source_dir)
        self.actionSaveFile_Path.triggered.connect(self.func_save_dir)
        self.actionMode.triggered.connect(self.func_mode)

    #初始化options.ini（如果不存在就创建）
    def init_configs(self):
        if os.path.exists("options.ini"):
            # 实例化configParser对象
            config = configparser.ConfigParser()
            # -read读取ini文件
            config.read('options.ini')
            configs_temp=config.items('OPTIONS')

            configs=[]

            for row in configs_temp:
                configs.append(row[1])

            if len(configs)!=3:
                QMessageBox.information(self,"警告","配置文件损坏，将会重置！",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
                # 实例化configParser对象
                config = configparser.ConfigParser()

                config.add_section("OPTIONS")
                config.set("OPTIONS", "SOURCE", "./")
                config.set("OPTIONS", "SAVE", "./")
                config.set("OPTIONS", "MODE", "1")

                # write to file
                config.write(open('options.ini', "w"))
                return './','./','1'

            return configs[0],configs[1],configs[2]
        else:
            # 实例化configParser对象
            config = configparser.ConfigParser()

            config.add_section("OPTIONS")
            config.set("OPTIONS", "SOURCE", "./")
            config.set("OPTIONS", "SAVE", "./")
            config.set("OPTIONS", "MODE", "1")

            # write to file
            config.write(open('options.ini', "w"))

            return './','./','1'

    def init_window(self):
        #获取source文件夹下所有的txt文件
        self.result=[]
        self.num=0
        filter=[".txt"]
        for maindir, subdir, file_name_list in os.walk(self.source):
            for filename in file_name_list:
                apath = os.path.join(maindir, filename)#合并成一个完整路径
                ext = os.path.splitext(apath)[1]  # 获取文件后缀 [0]获取的是除了文件名以外的内容

                if ext in filter:
                    self.result.append(apath)

        self.filename=self.result[0]
        f=open(self.filename,'r',encoding='utf-8')
        data=f.read()
        self.textBrowser.setText(data)
        words=divide_words(data)
        self.textEdit.setText(words)
        f.close()


    def func_last(self):
        if 0<self.num<=len(self.result)-1:
            self.num=self.num-1
            self.filename=self.result[self.num]
            f=open(self.filename,'r',encoding='utf-8')
            data=f.read()
            self.textBrowser.setText(data)
            words=divide_words(data)
            self.textEdit.setText(words)
            f.close()
        else:
            QMessageBox.information(self,"警告","当前是第一个！",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)

    def func_next(self):
       if 0<=self.num<len(self.result)-1:
            self.num=self.num+1
            self.filename=self.result[self.num]
            f=open(self.filename,'r',encoding='utf-8')
            data=f.read()
            self.textBrowser.setText(data)
            words=divide_words(data)
            self.textEdit.setText(words)
            f.close()
       else:
            QMessageBox.information(self,"警告","当前是最后一个！",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)

    def func_save(self):
        self.savefilename=self.save+"/"+self.filename.split('\\')[-1]
        f=open(self.savefilename,'w',encoding='utf-8')
        f.write(self.textEdit.toPlainText())
        f.close()

    def func_source_dir(self):
        text = QFileDialog.getExistingDirectory(self,"choose directory",r"C:\Users\Administrator\Desktop")
        if text != '':

            # 实例化configParser对象
            config = configparser.ConfigParser()

            config.add_section("OPTIONS")
            config.set("OPTIONS", "SOURCE", text)
            config.set("OPTIONS", "SAVE",self.save)
            config.set("OPTIONS", "MODE", self.mode)

            # write to file
            config.write(open('options.ini', "w+"))

            self.source=text
            self.init_window()

    def func_save_dir(self):
        text = QFileDialog.getExistingDirectory(self,"choose directory",r"C:\Users\Administrator\Desktop")
        if text != '':
            # 实例化configParser对象
            config = configparser.ConfigParser()

            config.add_section("OPTIONS")
            config.set("OPTIONS", "SOURCE", self.source)
            config.set("OPTIONS", "SAVE", text)
            config.set("OPTIONS", "MODE", self.mode)

            # write to file
            config.write(open('options.ini', "w+"))

            self.save=text

    def func_mode(self):
        text, okPressed = QInputDialog.getText(self, "设置","模式（1-命名实体标注 2-情感标注）:", QLineEdit.Normal, "")
        if okPressed and (text == '2' or text=='1'):
            # 实例化configParser对象
            config = configparser.ConfigParser()

            config.add_section("OPTIONS")
            config.set("OPTIONS", "SOURCE", self.source)
            config.set("OPTIONS", "SAVE", self.save)
            config.set("OPTIONS", "MODE", text)

            # write to file
            config.write(open('options.ini', "w+"))

            self.mode=text
            self.init_window()