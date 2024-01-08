from typing import Container
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import datetime
import sqlite3
import sys
from tkinter import *
from tkinter import ttk
from PyQt5 import QtGui,QtCore,QtWidgets
from PyQt5.uic import loadUiType

import autopy
from xlwt import Workbook
import toolmenu
import smtplib as st
from email.message import EmailMessage

import re, uuid  #This is for generating mac address of devise randomly

zi,_ = loadUiType('Login2.ui')
class Login(QWidget,zi):                # Login Code....
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.pushButton.clicked.connect(self.Handel_Login)
        self.pushButton_3.clicked.connect(self.Exit)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.Buttonhandel()


    def Buttonhandel(self):
        self.pushButton_4.clicked.connect(self.Serial_Number)
        pass

      
    
    def Handel_Login(self):
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()

        username = self.lineEdit.text()
        password = self.lineEdit_2.text()

        MAC = str(':'.join(re.findall('..','%012x' % uuid.getnode())))
        # MAC = self.
        sql = ''' SELECT * FROM user '''

        self.cur.execute(sql,)
        data = self.cur.fetchall()
        for row in data  :
            if username == row[0] and password == row[1]:
                self.db = sqlite3.connect('DB\db.db')
                self.cur = self.db.cursor()
                sql2 = '''SELECT * FROM mac'''
                self.cur.execute(sql2)
                data2 = self.cur.fetchall()

                for row in data2:
                    if MAC == row[0]:
                        self.window10 = MainApp()
                        self.window10.show()
                        self.close()
                    else:
                        message2 = QMessageBox.information(self,"Unathorized","You have not authoriesed User, Kindlly Contact the Customer Service")
                        # sys.exit(Login)
                    
            else:
                self.label_9.setText('Make Sure You Enterd Your Username\n& Password Correctly')

    def Exit(self):
        warning = QMessageBox.warning(self , 'Exit' , "You want to exit?" , QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes :
         sys.exit(Login)




         
    def Serial_Number(self):
        self.view_products = toolmenu.Serial_Number()
        # self.mdi.addSubWindow(self.view_products)
        # self.view_products.showMaximized()
        self.view_products.show()



class MainApp(QMainWindow,Tk):
    def __init__(self):
        QMainWindow.__init__(self)
        self.initUI()
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        # self.showFullScreen()
        # self.showMaximized()
       

        self.setGeometry(0, 0, 1920, 1080)
        self.setCentralWidget(self.mdi)
        self.Sales()
        self.show()



    def initUI(self):
        self.mdi = QMdiArea()
        self.toolBar()
        self.mainMenu()



# ============== Main Menu Bar =======================
    def mainMenu(self):
        self.menubar = self.menuBar()      
          
        masters_bar = self.menubar.addMenu("File")
        transaction_bar = self.menubar.addMenu("Edit")
        Acc_bar = self.menubar.addMenu("Accounts")
        Settings = self.menubar.addMenu("Settings")
        # report_bar = self.menubar.addMenu("Help")




        save = QAction("Save", self)
        save.triggered.connect(self.save_data)
        masters_bar.addAction(save)

        save_as = QAction("Save as", self)
        save_as.triggered.connect(self.save_data)
        masters_bar.addAction(save_as)


        undo = QAction("Undo", self)
        # clear_items_table.triggered.connect(self.clear_all_items)
        transaction_bar.addAction(undo)

        
        redo = QAction("Redo", self)
        # clear_items_table.triggered.connect(self.clear_all_items)
        transaction_bar.addAction(redo)

        
        cut = QAction("Cut", self)
        # clear_items_table.triggered.connect(self.clear_all_items)
        transaction_bar.addAction(cut)

        
        copy = QAction("Copy", self)
        # clear_items_table.triggered.connect(self.clear_all_items)
        transaction_bar.addAction(copy)

        
        past = QAction("Past", self)
        # clear_items_table.triggered.connect(self.clear_all_items)
        transaction_bar.addAction(past)



        User_account = QAction("Create User Account", self)
        User_account.triggered.connect(self.User_Account)
        Acc_bar.addAction(User_account)

        
        add_Contact = QAction("Add User Contact", self)
        add_Contact.triggered.connect(self.user_contact)
        Acc_bar.addAction(add_Contact)

        Camera = QAction("Camera Setting", self)
        Camera.triggered.connect(self.cameraSetting)
        Settings.addAction(Camera)

        winSetting = QAction("Window Setting", self)
        winSetting.triggered.connect(self.windowSetting)
        Settings.addAction(winSetting)


    def save_data(self):
        # self.db = mysql.connector.connect(host='localhost' , user='root' , password ='shubh96S@' , db='data')
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT Purchase_Bill,Supp_Bill,Barcode,Product_Name,Artical_No,MRP,Sale_Rate,Rate,Net_Amount,Qty,Packing,Storage,Date,GST,Debit_Note,Credit_Note,Suplire_Name,City,Payment_Mode FROM add_products''')
        data = self.cur.fetchall()
        try:
            wb = Workbook()
            path, _ = QFileDialog.getSaveFileName(self, "Save File", QDir.homePath() + "/Products.xls", "XLS Files(*.xls *.txt)")
            if path:
                sheet1 = wb.add_sheet('Product_Purchase_Details')
                sheet1.write(0,0 , 'Purchase_Bill')
                sheet1.write(0,1 , 'Supp_Bill')
                sheet1.write(0,2 , 'Barcode')
                sheet1.write(0,3 , 'Product_Name')
                sheet1.write(0,4 , 'Artical_No')
                sheet1.write(0,5 , 'MRP')
                sheet1.write(0,6 , 'Sale_Rate')
                sheet1.write(0,7 , 'Rate')
                sheet1.write(0,8 , 'Net_Amount')
                sheet1.write(0,9 , 'Qty')
                sheet1.write(0,10 , 'Packing')
                sheet1.write(0,11 , 'Storage')
                sheet1.write(0,12 , 'Date')
                sheet1.write(0,13 , 'GST')
                sheet1.write(0,14 , 'Debit_Note')
                sheet1.write(0,15 , 'Credit_Note')
                sheet1.write(0,16 , 'Suplire_Name')
                sheet1.write(0,17 , 'City')
                sheet1.write(0,18 , 'Payment_Mode')
                row_number = 1
                for row in data :
                    column_number = 0
                    for item in row :
                        sheet1.write(row_number , column_number , str(item))
                        column_number += 1
                    row_number += 1
                self.statusBar().showMessage('Products Report Created Successfully')
            wb.save(path)
        except:
            buttonreplay = QMessageBox.information(self,"Try Again!","Please Try to Export again")


    def toolBar(self):
        self.tb = self.addToolBar("Tool Bar")
        self.tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.addActions
        
        # Tool Bar Buttons
        self.sales = QAction(QIcon('src/icons/sales.png'), "F5-Sales", self)
        self.sales.setShortcut("F5")
        self.sales.setFont(QFont("Liberation Mono", 12))
        self.sales.triggered.connect(self.Sales)
        self.tb.addAction(self.sales)
        self.tb.addSeparator()

        self.purchase = QAction(QIcon('src/icons/purchase.png'), "F6-Purchase", self)
        self.purchase.setShortcut("F6")
        self.purchase.setFont(QFont("Liberation Mono",12))
        self.purchase.triggered.connect(self.Purchase)
        self.tb.addAction(self.purchase)
        self.tb.addSeparator()

        self.view_products = QAction(QIcon('src/icons/ledger.png'), "F7-Product List", self)
        self.view_products.setShortcut("F7")
        self.view_products.setFont(QFont("Liberation Mono",12))
        self.view_products.triggered.connect(self.View_Product)
        self.tb.addAction(self.view_products)
        self.tb.addSeparator()


        self.stock_Manage = QAction(QIcon('src/icons/payment.png'), "F8-Stock Managament", self)
        self.stock_Manage.setShortcut("F7")
        self.stock_Manage.setFont(QFont("Liberation Mono",12))
        self.stock_Manage.triggered.connect(self.Stock_Manmagament)
        self.tb.addAction(self.stock_Manage)
        self.tb.addSeparator()


        self.calculator = QAction(QIcon('src/icons/calculator.png'), "F9-Calculator", self)
        self.calculator.setShortcut("F8")
        self.calculator.setFont(QFont("Liberation Mono",12))
        self.calculator.triggered.connect(self.Calcu)
        self.tb.addAction(self.calculator)
        self.tb.addSeparator()

        self.usersetting = QAction(QIcon('src/icons/receipt.png'), "F10-User Setting", self)
        self.usersetting.setShortcut("F10")
        self.usersetting.setFont(QFont("Liberation Mono",12))
        self.usersetting.triggered.connect(self.Setting)
        self.tb.addAction(self.usersetting)
        self.tb.addSeparator()



    def Sales(self):
        self.saleswindow = toolmenu.Sales()
        self.mdi.addSubWindow(self.saleswindow)
        self.saleswindow.showMaximized()
        self.saleswindow.show()
        
    def Setting(self):
        self.saleswindow = toolmenu.Setting()
        self.mdi.addSubWindow(self.saleswindow)
        self.saleswindow.showMaximized()
        self.saleswindow.show()


    def Purchase(self):
        self.purchasewindow = toolmenu.Purchase()
        self.mdi.addSubWindow(self.purchasewindow)
        self.purchasewindow.showMaximized()
        self.purchasewindow.show()

    def View_Product(self):
        self.view_products = toolmenu.View()
        self.mdi.addSubWindow(self.view_products)
        self.view_products.showMaximized()
        self.view_products.show()

    def Stock_Manmagament(self):
        self.stock = toolmenu.Stock_Manager()
        self.mdi.addSubWindow(self.stock)
        self.stock.show()

    def Calcu(self):
        self.cal = toolmenu.Calculator()
        self.mdi.addSubWindow(self.cal)
        # self.cal.showMinimized()
        self.cal.show()



    def User_Account(self):
        self.window2 = User()
        self.window2.show()
        pass
    
    def user_contact(self):
        self.window2 = addContact()
        self.window2.show()
        pass
    
    def cameraSetting(self):
        self.camera = toolmenu.CameraSetting()
        self.mdi.addSubWindow(self.camera)
        self.camera.show()
        pass
    
    def windowSetting(self):
        self.window2 = addContact()
        self.window2.show()
        pass

bo,_ = loadUiType('ToolBar/SMS.ui')
class addContact(QMainWindow,bo):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Contact")
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.setGeometry(300,100,817,441)
        self.setupUi(self)
        self.handelbuttons()
        self.show()
        
    def handelbuttons(self):
        self.pushButton_2.clicked.connect(self.CreateUser) 
        pass  
    
    def CreateUser(self):
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()
        
        
        Name = self.lineEdit_12.text()
        Contact = self.lineEdit_11.text()
        
        try:
            data1 = (Name,Contact)
            sql = ''' INSERT INTO contact VALUES (?,?) '''

            self.cur.execute(sql,data1)

            self.db.commit()
            self.db.close()
            self.statusBar().showMessage("Contact Added Successfully!.")
        except:
            sdfsd = QMessageBox.information(self,"Sorry!","This user contact is already exist, Please try again!")
         
        
        
        
        

mi,_ = loadUiType('user.ui')
class User(QMainWindow,mi):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sales")
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.setGeometry(300,100,611,251)
        self.setupUi(self)
        self.handelbuttons()
        # self.Box()
        # self.Hiding_Themes()
        self.show()

    def handelbuttons(self):
        self.pushButton.clicked.connect(self.create_account)


    def create_account(self):
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()


        username = self.lineEdit.text()
        password = self.lineEdit_4.text()

        try:
            data1 = (username,password)
            sql = ''' INSERT INTO user VALUES (?,?) '''

            self.cur.execute(sql,data1)

            self.db.commit()
            self.db.close()
            self.statusBar().showMessage("User Added")
        except:
            sdfsd = QMessageBox.information(self,"Sorry!","This user name is already exist, Please try again!")
         

def main():
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    sys.exit(app.exec_())
    # app.exec_()


if __name__ == '__main__':
    main()
    
    