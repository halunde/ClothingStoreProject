
from sqlite3.dbapi2 import Cursor
import sys
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sqlite3
from tkinter import*
from tkinter import ttk
from PyQt5.uic import loadUi, loadUiType
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
import datetime
from shutil import copyfile

from requests.models import Response
from xlwt import Workbook
import os
import random
import tempfile
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
import pyqrcode 
from pyqrcode import QRCode 
import qrcode
import cv2
import re,uuid

import json
import requests

ui,_ = loadUiType('ToolBar\Sales.ui')
class Sales(QMainWindow,ui):
    def __init__(self):
        super().__init__()  
        self.setWindowTitle("Sales")
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.setGeometry(0,0,1366,768)
        self.setupUi(self)
        self.handelbuttons()
        self.Box()
        self.Hiding_Themes()
        self.showMaximized()
        self.show()
        self.lineEdit_21.setText("Kedarling")
        self.lineEdit_23.setText("Sakshi")
        
        self.l = []

        self.z1.setText("0")
        self.z2.setText("0")
        self.z3.setText("0")
        self.z4.setText("0")
        self.z5.setText("0")
        self.z6.setText("0")
        self.lineEdit_14.setText("0")


    def handelbuttons(self):
        self.lineEdit.textChanged.connect(self.Login)
        self.lineEdit_4.textChanged.connect(self.search)
        # self.pushButton_10.clicked.connect(self.search)
        self.pushButton_17.clicked.connect(self.add_QR_data)
        self.pushButton_15.clicked.connect(self.printer_priview)
        self.pushButton_15.clicked.connect(self.save_bill)
        self.pushButton_14.clicked.connect(self.Handel_UI_Changes)
        self.pushButton_9.clicked.connect(self.add_bill)
        self.pushButton_18.clicked.connect(self.find_bill)
        self.pushButton_11.clicked.connect(self.Generate)
        self.pushButton_12.clicked.connect(self.clear)
        self.pushButton_16.clicked.connect(self.add_stock)
        self.shortcut = QShortcut(QKeySequence('Return'),self)
        self.shortcut.activated.connect(self.search)
        self.pushButton_21.clicked.connect(self.Hiding_Themes)




    def availabel_Quantity(self):
        # self.db = mysql.connector.connect(host='localhost' , user='root' , password ='shubh96S@' , db='data')
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()

        artical_no = self.lineEdit_4.text()
        print("gdghdhdhdg")
        sql = ''' SELECT * FROM add_products WHERE Artical_No = ? '''
        self.cur.execute(sql , [(artical_no)])

        data = self.cur.fetchone()

        try:   
            a = self.label_29.setText(data[9])
            print(data[9])
        except:
            buttonReply = QMessageBox.information(self,"Sorry!","No Such Artical Number In Our Product List Please Check Artical Number")

        

    def update_quantity(self):
        # self.db = mysql.connector.connect(host='localhost' , user='root' , password ='shubh96S@' , db='data')
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()
        
        artical_no = self.lineEdit_4.text()
        qty_a = self.lineEdit_3.text()
        
        a = int(self.label_29.text())
        
        if(a>0):
            try:
                self.cur.execute(f"UPDATE add_products  SET Qty = Qty-{qty_a} WHERE Artical_No = {artical_no} ")
                self.db.commit()
                self.db.close()

            except:
                sasd = QMessageBox.information(self,"Information","Please add products before generate bill")
        else:
            ss = QMessageBox.information(self,"Warning!","You have zero Quntity please add stock..")
            
            try: 
                self.db = sqlite3.connect('DB\db.db')
                self.cur = self.db.cursor()

                User_Name = self.lineEdit_23.text()

                sql = ''' SELECT * FROM contact WHERE AdminName = ? '''
                self.cur.execute(sql , [(User_Name)])

                data = self.cur.fetchone()
                
                self.sendSMS(data[1],"You have zero Quntity please add stock..")
            except:
                ss = QMessageBox.information(self,"Warning!","You have set wrong user name Or Check Your Internate Connection")
            

    def sendSMS(self,number,message):
        url = "https://www.fast2sms.com/dev/bulkV2"
        
        para = {
        "authorization" : "pb5yluXQZ63ekETG2AB9JsK74W1R8cnDaHNUI0dmiSrVhqoFMxDum5gr8LVGki3a61s9JRBnOjlcAqev",
        "sender_id" : "INVWNTORY",
        "route" : "p",
        "language" : "unicode",
        "numbers" : number,
        "message" : message  
        }
        
        resoponse = requests.get(url, params=para)
        dic = resoponse.json()
        
        
        
    
    
    
    def add_stock(self):
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()

        artical_no = self.lineEdit_4.text()
        qty_a = self.lineEdit_16.text()
        try:
            self.cur.execute(f"UPDATE add_products SET Qty = Qty+{qty_a} WHERE Artical_No = {artical_no}")
            sdfd = QMessageBox.information(self,"Updated","Stock Updated!")
            self.statusBar().showMessage("")
            self.db.commit()
            self.db.close()
        except:
            dkjf = QMessageBox.information(self,"Warning!","Please enter the valid Artical Number & Stock Quantity")




    def Handel_UI_Changes(self):
        self.Hiding_Themes()
        self.groupBox_4.setVisible(True)

        customer_Name = self.lineEdit_6.text()
        customer_Email = self.lineEdit_8.text()
        contact_number = self.lineEdit_12.text()

        total = self.lineEdit_15.text()

        self.Bill_Number = StringVar()
        z=random.randint(1,1000000)
        self.Bill_Number.set(z)

        product_name1 = self.a1.text()
        product_name2 = self.a2.text()
        product_name3 = self.a3.text()
        product_name4 = self.a4.text()
        product_name5 = self.a5.text()
        product_name6 = self.a6.text()


        MRP1 = self.x1.text()
        MRP2= self.x2.text()
        MRP3= self.x3.text()
        MRP4= self.x4.text()
        MRP5= self.x5.text()
        MRP6= self.x6.text()



        QTY1 = self.y1.text()
        QTY2 = self.y2.text()
        QTY3 = self.y3.text()
        QTY4 = self.y4.text()
        QTY5 = self.y5.text()
        QTY6 = self.y6.text()
        


        Total1 = self.z1.text()
        Total2 = self.z2.text()
        Total3 = self.z3.text()
        Total4 = self.z4.text()
        Total5 = self.z5.text()
        Total6 = self.z6.text()

        dt = datetime.datetime.now()
        # current = ("%s:%s:%s" % dt.day,dt.month,dt.year)
        
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()

        ShopeName = self.lineEdit_21.text()
        try:
            sql = ''' SELECT * FROM setting WHERE ShopName = ? '''
            self.cur.execute(sql,[(ShopeName)])
            data = self.cur.fetchone()
        except:
            ersd = QMessageBox.information(self,"Error","No Shop Name Found")
            

   
        current_date = str("%s:%s:%s" % (dt.day, dt.month, dt.year))

        # self.textEdit.delete(1.0,END)
        self.textEdit.insertPlainText("---------------------------------------------------------------------")
        try:
            self.textEdit.insertPlainText(str(f"\n                                              {data[1]}              "))   
            self.textEdit.insertPlainText(str(f"\n                                 {data[2]}         "))
            self.textEdit.insertPlainText(str(f"\n	{data[3]} - {data[4]}\n"))
            self.textEdit.insertPlainText("---------------------------------------------------------------------"  )
            self.textEdit.insertPlainText(str("\n                 Boutique & Design Studio Designer Ladies Dress\n     Ethnic Wear, Kurtis, Sarees, Lehanga, Suits, Indo Western         \n"))
            self.textEdit.insertPlainText(str("Address - 513 Near Sai Ganesh Temple Herle Kolhapur 416005           "))
            self.textEdit.insertPlainText("---------------------------------------------------------------------")

            self.textEdit.insertPlainText(f"\n Bill Number:  {self.Bill_Number.get()}")
            self.textEdit.insertPlainText(f"\n Customer Name:  {customer_Name}")
            self.textEdit.insertPlainText(f"\n Phone Number:  {contact_number}")
            self.textEdit.insertPlainText(f"\n Customer Email:  {customer_Email}")
            self.textEdit.insertPlainText(f"\n Date:  {current_date}")
            self.textEdit.insertPlainText("\n ---------------------------------------------------------------------")

            self.textEdit.insertPlainText(f"\n Sr.No.    Product Name\tRate\tQty\tTotal")
            self.textEdit.insertPlainText("\n ---------------------------------------------------------------------")

            self.textEdit.insertPlainText(f"\n 1.                {product_name1}\t{MRP1}\t{QTY1}         \t{Total1}")
            self.textEdit.insertPlainText("\n")
            self.textEdit.insertPlainText(f"\n 2.                {product_name2}\t{MRP2}\t{QTY2}         \t{Total2}")
            self.textEdit.insertPlainText("\n")
            self.textEdit.insertPlainText(f"\n 3.                {product_name3}\t{MRP3}\t{QTY3}         \t{Total3}")
            self.textEdit.insertPlainText("\n")
            self.textEdit.insertPlainText(f"\n 4.                {product_name4}\t{MRP4}\t{QTY4}         \t{Total4}")
            self.textEdit.insertPlainText("\n")
            self.textEdit.insertPlainText(f"\n 5.                {product_name5}\t{MRP5}\t{QTY5}         \t{Total5}")
            self.textEdit.insertPlainText("\n")
            self.textEdit.insertPlainText(f"\n 6.                {product_name6}\t{MRP6}\t{QTY6}         \t{Total6}")
            self.textEdit.insertPlainText("\n")
            self.textEdit.insertPlainText("\n")
            self.textEdit.insertPlainText("\n ---------------------------------------------------------------------")
            self.textEdit.insertPlainText(f"\n                                                                                   Total: {total}")
            self.textEdit.insertPlainText(str("\n Tearms & Conditions:"))
            self.textEdit.insertPlainText(str("\n No Return No Exchange"))
            self.textEdit.insertPlainText(str("\n No Guarantee No Warranty"))
        except:
            kjk = QMessageBox.information(self, "Error", "No Shop name found")

    
    def save_bill(self):
        warning = QMessageBox.warning(self , 'Save Bill' , "Do you want to save bill?" , QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes :
                 self.bill_data=self.textEdit.toPlainText()
                 f1 = open('Billing_Saved_Data/' + str(self.Bill_Number.get())+".text",'w')
                 f1.write(self.bill_data)
                 w = QMessageBox.information(self,"Success",f"Bill No:{self.Bill_Number.get()} saved successfully")
                 f1.close()

    def find_bill(self):
        found = "no"
        for i in os.listdir("Billing_Saved_Data/"):
                if i.split('.')[0]==self.lineEdit_20.text():
                        f1 = open(f'Billing_Saved_Data/{i}','r')
                        self.textEdit.setText("")
                        for d in f1:
                                self.textEdit.insertPlainText(d)
                        f1.close()
                        found = "yes"
        if found =="no":
                werwr = QMessageBox.information(self,"Error","Invalid Bill Number")
      
    def Hiding_Themes(self):
        self.groupBox_4.hide()
        self.textEdit.setText("")


    def Box(self):
        username = self.lineEdit.text()

        if username == "":
            self.groupBox.setEnabled(False) 
            self.label_10.setText("")



    def Login(self):
        # self.db = mysql.connector.connect(host='localhost' , user='root' , password ='shubh96S@' , db='data')
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()

        password = self.lineEdit.text()
        username = self.lineEdit_22.text()    
        sql = ''' SELECT * FROM user WHERE Username = ?''' 
        self.cur.execute(sql,[(username)])

        my_data = self.cur.fetchall()

        for column in my_data :
            if password == column[1] :
                self.label_10.setText("Admin")
                self.groupBox.setEnabled(True)

            else:
                self.groupBox.setEnabled(False)
                self.label_10.setText("Invalid Password ")


    def search(self):
        # self.db = mysql.connector.connect(host='localhost' , user='root' , password ='shubh96S@' , db='data')
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()
        print("sakshi")   

        artical_no = self.lineEdit_4.text()
        avalable_stock = self.label_29.text()
        
        if artical_no == "":
            uttonReply = QMessageBox.information(self,"Empty","Please Enter The Artical Number")
        else:
            sql = ''' SELECT * FROM add_products WHERE Artical_No = ? '''
            self.cur.execute(sql , [(artical_no)])
                
            data = self.cur.fetchone()

            try:   
                self.lineEdit_2.setText(data[3])
                self.lineEdit_10.setText(data[21])
                self.lineEdit_11.setText(data[20])
                self.lineEdit_5.setText(data[5])
                self.lineEdit_7.setText(data[13])
                self.comboBox.setCurrentText(data[14])
                self.availabel_Quantity()
                self.statusBar().showMessage(f" Available Quantity: {avalable_stock}")
                
        
            except:
                # buttonReply = QMessageBox.information(self,"Sorry!","No Such Artical Number In Our Product List Please Check Artical Number")
                self.statusBar().showMessage("No Such Artical Number In Our Product List Please Check Artical Number")


    def add_QR_data(self):
       
        wCam, hCam = 500, 500
        try:
            cap = cv2.VideoCapture(0)
            cap.set(3, wCam)
            cap.set(4, hCam)

            # initialize the OpenCV QRCode detector
            detector = cv2.QRCodeDetector()
            while True:
                success, img = cap.read()
                # detect and decode
                data, vertices_array, _ = detector.detectAndDecode(img)
                # check if there is a QRCode in the image
                if vertices_array is not None:
                    if data:
                        self.lineEdit_4.setText(str(data))
                        self.add_bill()
                        break
                        
                # display the result
                cv2.imshow("img", img)
                # Enter q to Quit
                if cv2.waitKey(1) == ord("q"):
                    break
            cap.release()
            cv2.destroyAllWindows()
        except:
            ButtonReaplay = QMessageBox.information(self,"Camera","Please sure to connect respective device")


    def add_bill(self):

        self.MRP = self.lineEdit_5.text()
        self.Disc = self.lineEdit_7.text()
        self.Qty = self.lineEdit_3.text()
        self.product_name = self.lineEdit_2.text()
        self.GST = self.comboBox.currentText()
        self.net_Amount = self.lineEdit_9.text()

        try:
            s1 = int(self.lineEdit_5.text())
            s2 = int(self.lineEdit_3.text())

            self.lineEdit_9.setText(str(s1*s2))
            self.total = str(self.lineEdit_9.text())

            self.l1 = []
            self.l1.append(str(self.product_name))
            self.l1.append(str(self.MRP))
            self.l1.append(str(self.Qty))
            self.l1.append(str(self.total))
            self.l.append(self.l1)

            for i in range(0,len(self.l)):
                a = 'a' + (str(i+1))
                if a == "a1":
                    self.a1.setText(str(self.l[i][0])) 
                    self.x1.setText(str(self.l[i][1]))
                    self.y1.setText(str(self.l[i][2]))
                    self.z1.setText(str(self.l[i][3]))
                    
                elif a == "a2":
                    self.a2.setText(str(self.l[i][0])) 
                    self.x2.setText(str(self.l[i][1]))
                    self.y2.setText(str(self.l[i][2]))
                    self.z2.setText(str(self.l[i][3]))
                    
                elif a == "a3":
                    self.a3.setText(str(self.l[i][0])) 
                    self.x3.setText(str(self.l[i][1]))
                    self.y3.setText(str(self.l[i][2]))
                    self.z3.setText(str(self.l[i][3]))
                    
                elif a == "a4":
                    self.a4.setText(str(self.l[i][0])) 
                    self.x4.setText(str(self.l[i][1]))
                    self.y4.setText(str(self.l[i][2]))
                    self.z4.setText(str(self.l[i][3]))
                    
                elif a == "a5":
                    self.a5.setText(str(self.l[i][0])) 
                    self.x5.setText(str(self.l[i][1]))
                    self.y5.setText(str(self.l[i][2]))
                    self.z5.setText(str(self.l[i][3]))
                    
                elif a == "a6":
                    self.a6.setText(str(self.l[i][0])) 
                    self.x6.setText(str(self.l[i][1]))
                    self.y6.setText(str(self.l[i][2]))
                    self.z6.setText(str(self.l[i][3]))
        except:
            buttdsf = QMessageBox.information(self,"Warning","Please Enter valid Artical No. then Quantity No.")
                
            
    def clear(self):
        self.a1.setText("")
        self.x1.setText("")
        self.a2.setText("")
        self.x2.setText("")
        self.a3.setText("")
        self.x3.setText("")
        self.a4.setText("")
        self.x4.setText("")
        self.a5.setText("")
        self.x5.setText("")
        self.a6.setText("")
        self.x6.setText("")
        self.y1.setText("")
        self.z1.setText("0")
        self.y2.setText("")
        self.z2.setText("0")
        self.y3.setText("")
        self.z3.setText("0")
        self.y4.setText("")
        self.z4.setText("0")
        self.y5.setText("")
        self.z5.setText("0")
        self.y6.setText("")
        self.z6.setText("0")

        self.lineEdit_2.setText("")
        self.lineEdit_4.setText("")
        self.lineEdit_10.setText("")
        self.lineEdit_11.setText("")
        self.lineEdit_13.setText("")
        self.lineEdit_15.setText("")
        self.lineEdit_3.setText("")
        self.lineEdit_6.setText("")
        self.lineEdit_12.setText("")
        self.lineEdit_8.setText("")
        self.lineEdit_5.setText("")
        self.lineEdit_7.setText("")
        self.lineEdit_9.setText("")
        self.lineEdit_17.setText("")
        self.lineEdit_18.setText("")
        self.lineEdit_19.setText("")

        self.label_29.setText("")

        self.lineEdit_20.setText("")

        self.l = []

    
    def Generate(self):
        self.update_quantity()
        self.welcome()

    def welcome(self):
        
        customer_Name = self.lineEdit_6.text()
        customer_Email = self.lineEdit_8.text()
        contact_number = self.lineEdit_12.text()

        if customer_Name =="" and contact_number =="":
            hggh = QMessageBox.information(self,"Alert!","Customer Name & Contact is mendentory")
        else:
            self.lineEdit_13.setText(customer_Name)
            self.lineEdit_18.setText(customer_Email)
            self.lineEdit_19.setText(contact_number)

            a = int(self.z1.text())
            b = int(self.z2.text())
            c = int(self.z3.text())
            d = int(self.z4.text())
            e = int(self.z5.text())
            f = int(self.z6.text())

            self.lineEdit_15.setText(str(str("Rs. ") + str(a+b+c+d+e+f)))
            self.lineEdit_17.setText(str(str("Rs. ") + str(a+b+c+d+e+f)))
      
  
    def printfile(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)

        if dialog.exec_() == QPrintDialog.accepted:
            self.textEdit.print_(printer)

    def printer_priview(self):
        printer = QPrinter(QPrinter.HighResolution)
        previewDialog = QPrintPreviewDialog(printer,self)
        previewDialog.paintRequested.connect(self.printer_priview2)
        previewDialog.exec_()
        pass
    
    def printer_priview2(self, printer):
        self.textEdit.print_(printer)


    def IExit(self):
        warning = QMessageBox.warning(self , 'Delete Product' , "are you sure you want to delete this Product?" , QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes :
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
        else:
            sys.exit(Sales())




ti,_ = loadUiType('ToolBar\View_products.ui')
class View(QMainWindow,ti):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("View")
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.setGeometry(0,0,964,566)
        self.setupUi(self)
        # self.Show_Combobox()
        # self.Purchase_Bill_No()
        self.handelbuttons()
        self.view()
        self.show()

    def handelbuttons(self):
        self.pushButton_9.clicked.connect(self.Export_Product)
        self.pushButton_11.clicked.connect(self.printer_priview)
        pass

    def view(self):
        # self.db = mysql.connector.connect(host='localhost' , user='root' , password ='shubh96S@' , db='data')
        self.db = sqlite3.connect('DB\db.db')

        self.cur = self.db.cursor()

        self.cur.execute("SELECT Purchase_Bill,Supp_Bill,Barcode,Product_Name,Artical_No,MRP,Sale_Rate,Rate,Net_Amount,Qty,Packing,Storage,Date,Discont,GST,Debit_Note,Credit_Note,Suplire_Name,City,Payment_Mode,Color,Size FROM add_products")
        data = self.cur.fetchall()

        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)

        for row, form in enumerate(data):
            for column, items in enumerate(form):
                self.tableWidget.setItem(row, column, QTableWidgetItem(str(items)))

            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)


        self.db.close()




    def printer_priview(self):
        printer = QPrinter(QPrinter.HighResolution)
        previewDialog = QPrintPreviewDialog(printer,self)
        previewDialog.paintRequested.connect(self.printer_priview2)
        previewDialog.exec_()
        pass
    
    def printer_priview2(self, printer):
        document = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(document)
        table = cursor.insertTable(self.tableWidget.rowCount(), self.tableWidget.columnCount())

        for row in range(table.rows()):
            for col in range(table.columns()):
                it = self.tableWidget.item(row,col)
                if it is not None:
                    cursor.insertText(it.text())
                cursor.movePosition(QtGui.QTextCursor.NextCell)
        document.print_(printer)



    
    def Export_Product(self):
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



    

        


pi,_ = loadUiType('ToolBar\Purchase.ui')
class Purchase(QMainWindow,pi):
    count = 0
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Purchase")
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.setGeometry(0,0,1366,768)
        self.setupUi(self)
        self.lineEdit_24.setText("Sakshi")
        # self.Show_Combobox()
        # self.Purchase_Bill_No()
        dt = datetime.datetime.now()
        # current = ("%s:%s:%s" % dt.day,dt.month,dt.year)

        self.lineEdit_15.setText("%s:%s:%s" % (dt.day, dt.month, dt.year))

        self.buttonhandel()
        self.initUI()
        self.show()


    def initUI(self):
        # self.db = mysql.connector.connect(host='localhost' , user='root' , password ='shubh96S@' , db='data')
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()

        self.cur.execute("SELECT Purchase_Bill,Product_Name,Artical_No,MRP,Sale_Rate,Rate,Qty,Packing,Storage,Date,GST,Discont,Color,Size,Payment_Mode,Total,Paid,Pay FROM add_products")
        data = self.cur.fetchall()

        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)

        for row, form in enumerate(data):
            for column, items in enumerate(form):
                self.tableWidget.setItem(row, column, QTableWidgetItem(str(items)))

            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)


        self.db.close()


    def buttonhandel(self):
        self.pushButton_9.clicked.connect(self.add_products)
        self.pushButton_9.clicked.connect(self.Qr_Generator)
        # self.pushButton_11.clicked.connect(self.view_product)
        self.pushButton_12.clicked.connect(self.delete)
        self.pushButton.clicked.connect(self.search)
        self.shortcut = QShortcut(QKeySequence('Enter'),self)
        self.shortcut.activated.connect(self.search)
        self.pushButton_14.clicked.connect(self.clear)
        self.pushButton_13.clicked.connect(self.IExit)
        self.pushButton_3.clicked.connect(self.evaluate)
        self.pushButton_2.clicked.connect(self.Update_Amount)
        pass


    
    
    
    def total_balance(self):
        Quantity = int(self.lineEdit_18.text())
        product_price = int(self.lineEdit_9.text())

        self.label_23.setText(str(Quantity*product_price))
        self.label_22.setText("Rs.")

    def Qr_Generator(self):
        artical_number = self.lineEdit_7.text()
        product_name = self.lineEdit_4.text()

        QRCodefile = (f"QR_Code\{product_name}{artical_number}.png")
        qrObject = qrcode.QRCode(border=3)

        qrObject.add_data(artical_number)
        qrObject.make()
        image = qrObject.make_image()
        image.save(QRCodefile)

        pass



    def add_products(self):

        # self.db = mysql.connector.connect(host='localhost' , user='root' , password ='shubh96S@' , db='data')
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()
        
        Purchase_Bill = self.lineEdit.text()
        Supp_Bill = self.lineEdit_2.text()
        Payment_mode = self.comboBox_3.currentText()
        Date = self.lineEdit_15.text()


        Packing = self.lineEdit_11.text()
        Storage = self.lineEdit_13.text()
        Quantity = self.lineEdit_18.text()
        Supplier_Name = self.lineEdit_6.text()
        City = self.lineEdit_5.text()
        Product_Name = self.lineEdit_4.text()
        Artical_No = self.lineEdit_7.text()
        Barcode = self.lineEdit_3.text()

        MRP = self.lineEdit_9.text()
        Rate = self.lineEdit_10.text()
        Sale_Rate = self.lineEdit_8.text()
        Net_Amount = self.lineEdit_17.text()
        Discont = self.lineEdit_12.text()
        GST = self.comboBox_5.currentText()
        Debit_Note = self.lineEdit_14.text()
        Credit_Note = self.lineEdit_16.text()

        Packing = self.lineEdit_11.text()

        Color = self.lineEdit_19.text()
        Size = self.lineEdit_20.text()

        Total = self.lineEdit_21.text()
        paid = self.lineEdit_22.text()
        pay = self.lineEdit_23.text()
         
     
        
        if Purchase_Bill == "":
            buttonreplay3 = QMessageBox.information(self,"Empty!","All fields are Required!")
        else:
            try:
                sql2 = (Purchase_Bill,Supp_Bill,Barcode,Product_Name,Artical_No,MRP,Sale_Rate,Rate,Net_Amount,Quantity,Packing,Storage,Date,Discont,GST,
                        Debit_Note,Credit_Note,Supplier_Name,City, Payment_mode,Color,Size,Total,paid,pay)
                sql = ''' INSERT INTO add_products VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''

                self.cur.execute(sql,sql2)

                self.db.commit()
                self.db.close()
                self.initUI()
                self.statusBar().showMessage("Data Add")
                try: 
                    self.db = sqlite3.connect('DB\db.db')
                    self.cur = self.db.cursor()
                    User_Name = self.lineEdit_24.text()
                    sql = ''' SELECT * FROM contact WHERE AdminName = ? '''
                    self.cur.execute(sql , [(User_Name)])
                    data = self.cur.fetchone()
                    Q = int(Quantity)
                    M = int(MRP)
                    Total_Amount = (str(Q * M))
                    buttonreplay = QMessageBox.information(self,"Successful",f"Product Successfully Added!.Last purchase bill number:{Purchase_Bill}")
                    self.sendSMS(data[1],f'''You have Successfully Added New Product \n Purchase Bill:{Purchase_Bill} \n Product Name:{Product_Name} \n Total Quntity:{Quantity} \n Total Amount:{Total_Amount} \n Ammount Paid:{paid} \n Amount To Pay:{pay} ''')
                except:
                    ss = QMessageBox.information(self,"Warning!","You have set wrong user name Or Check Your Internate Connection")
            except:
                buttonreplay = QMessageBox.information(self,"Sorry!",f"Purchase Bill Number Already Exist.Last purchase bill number:{Purchase_Bill}")
            

    def sendSMS(self,number,message):
        url = "https://www.fast2sms.com/dev/bulkV2"
        
        para = {
        "authorization" : "pb5yluXQZ63ekETG2AB9JsK74W1R8cnDaHNUI0dmiSrVhqoFMxDum5gr8LVGki3a61s9JRBnOjlcAqev",
        "sender_id" : "INVWNTORY",
        "route" : "p",
        "language" : "unicode",
        "numbers" : number,
        "message" : message  
        }
        
        resoponse = requests.get(url, params=para)
        dic = resoponse.json()
   
    def evaluate(self):
        total = int(self.lineEdit_21.text())
        paid = int(self.lineEdit_22.text())

        pay = str(total - paid)

        self.lineEdit_23.setText(str(pay))






    def view_product(self):
        self.window = View()
        self.window.show()
        # window.close()


    def search(self):
        # self.db = mysql.connector.connect(host='localhost' , user='root' , password ='shubh96S@' , db='data')
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()

        artical_no = self.lineEdit_7.text()

        if artical_no == "":
            buttonReply = QMessageBox.information(self,"Empty","Please Enter The Artical Number")
        else: 
            sql = ''' SELECT * FROM add_products WHERE Artical_No = ? '''
            self.cur.execute(sql , [(artical_no)])
            
            data = self.cur.fetchone()

            try:   
                print(data)
                self.lineEdit.setText(data[0])
                self.lineEdit_2.setText(data[1])
                self.lineEdit_3.setText(data[2])
                self.lineEdit_4.setText(data[3])
                self.lineEdit_7.setText(data[4])
                self.lineEdit_9.setText(data[5])
                self.lineEdit_8.setText(data[6])
                self.lineEdit_10.setText(data[7])
                self.lineEdit_17.setText(data[8])
                self.lineEdit_18.setText(data[9])
                self.lineEdit_11.setText(data[10])
                self.lineEdit_13.setText(data[11])
                self.lineEdit_15.setText(data[12])
                self.lineEdit_12.setText(data[13])
                self.comboBox_5.setCurrentText(data[14])
                self.lineEdit_14.setText(data[15])
                self.lineEdit_16.setText(data[16])
                self.lineEdit_6.setText(data[17])
                self.lineEdit_5.setText(data[18])
                self.comboBox_3.setCurrentText(data[19])
                self.lineEdit_19.setText(data[20])
                self.lineEdit_20.setText(data[21])
                self.lineEdit_21.setText(data[22])
                self.lineEdit_22.setText(data[23])
                self.lineEdit_23.setText(data[24])
                self.total_balance()
                self.initUI()

            except:
                buttonReply = QMessageBox.information(self,"Sorry","No such Artical Number in our Product List please check Artical Number")


    def delete(self):
        # self.db = mysql.connector.connect(host='localhost' , user='root' , password ='shubh96S@' , db='data')
        self.db = sqlite3.connect('DB\db.db')

        self.cur = self.db.cursor()


        artical_no = self.lineEdit_7.text()
        if artical_no == "":
            buttonreplay = QMessageBox.information(self,"Empty!","Please Enter The Artical Number")
        else:
            warning = QMessageBox.warning(self , 'Delete Product' , "are you sure you want to delete this Product?" , QMessageBox.Yes | QMessageBox.No)
            if warning == QMessageBox.Yes :
                sql = ''' DELETE FROM add_products WHERE Artical_No = ? '''
                self.cur.execute(sql , [(artical_no)])
                self.db.commit()
                self.statusBar().showMessage('Product Deleted')
                self.initUI()


    def Update_Amount(self):
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()

        Paid = self.lineEdit_22.text()
        Pay = self.lineEdit_23.text()
        total = self.lineEdit_21.text()

        Artical_no = self.lineEdit_7.text()

        self.cur.execute(f"UPDATE add_products SET Paid = {Paid}, Pay = {Pay}, Total = {total}  WHERE Artical_No = {Artical_no}")
        self.db.commit()
        self.initUI()
        self.db.close()
        dfdsfsd = QMessageBox.information(self,"Updated","Payment Successfully Updated")
        pass

                

    def clear(self):
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit_3.setText("")
        self.lineEdit_4.setText("")
        self.lineEdit_7.setText("")
        self.lineEdit_9.setText("")
        self.lineEdit_8.setText("")
        self.lineEdit_10.setText("")
        self.lineEdit_17.setText("")
        self.lineEdit_18.setText("")
        self.lineEdit_11.setText("")
        self.lineEdit_13.setText("")
        dt = datetime.datetime.now()
        self.lineEdit_15.setText("%s:%s:%s" % (dt.day, dt.month, dt.year))
        self.lineEdit_12.setText("")
        # self.comboBox_5.setCurrentText("")
        self.lineEdit_14.setText("")
        self.lineEdit_16.setText("")
        self.lineEdit_6.setText("")
        self.lineEdit_5.setText("")
        self.label_23.setText("")
        self.label_22.setText("")
        self.lineEdit_19.setText("")
        self.lineEdit_20.setText("")
        self.lineEdit_21.setText("")
        self.lineEdit_22.setText("")
        self.lineEdit_23.setText("")

        # self.comboBox_3.setCurrentText("")
        pass

    def IExit(self):
        warning = QMessageBox.warning(self , 'Backup Data' , "Do you want to Backup today's Data?" , QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes :
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
                    sheet1.write(0,19 , 'Total')
                    sheet1.write(0,20 , 'Paid')
                    sheet1.write(0,21 , 'Pay')
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
        else:
            sys.exit(Purchase)



#***********************************************************************************************************



serial,_ = loadUiType('ToolBar\Serial_number.ui')
class Serial_Number(QMainWindow,serial):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("View")
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.setGeometry(400,200,521,236)
        self.setupUi(self)

        self.buttons()
        self.groupBox.setEnabled(False)
        self.show()


    def buttons(self):
        self.pushButton.clicked.connect(self.get_MAC)
        self.pushButton_2.clicked.connect(self.Add_MAC)
        self.pushButton_3.clicked.connect(self.login)
        self.pushButton_4.clicked.connect(self.delete)
        self.pushButton_5.clicked.connect(self.search)


    
    def get_MAC(self):
        MAC = str(':'.join(re.findall('..','%012x' % uuid.getnode())))
        self.lineEdit.setText(MAC)

    def Add_MAC(self):
        # self.db = mysql.connector.connect(host='localhost' , user='root' , password ='shubh96S@' , db='data')
        no = self.lineEdit_2.text()
        mw = self.lineEdit.text()

        if no == "" and mw == "":
            buttonReply = QMessageBox.information(self,"Sorry","Please Enter the Number Or Set MAC")
        else:
            self.db = sqlite3.connect('DB\db.db')
            self.cur = self.db.cursor()

            address = self.lineEdit.text()
            Number = self.lineEdit_2.text()
            try:
                data3 = (address,Number)
                sql = ''' INSERT INTO mac VALUES (?,?) '''

                self.cur.execute(sql,data3)
            except:
                message2 = QMessageBox.warning(self,"Cuation!","Mac Already Exist, Please Contact Customer Service")
                sys.exit(Serial_Number)

            self.db.commit()
            self.db.close()
            message3 = QMessageBox.information(self,"Successful!","MAC Added Successfully")
            self.statusBar().showMessage('MAC Added Successfully')

    def delete(self):
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor() 

        number = self.lineEdit_2.text()
        if number == "":
            buttonreplay = QMessageBox.information(self,"Empty!","Please Enter The Number")
        else:
            warning = QMessageBox.warning(self , 'Delete Product' , "Are you sure, You want to Delete this MAC?" , QMessageBox.Yes | QMessageBox.No)
            if warning == QMessageBox.Yes :
                sql = ''' DELETE FROM mac WHERE Number = ? '''
                self.cur.execute(sql , [(number)])
                self.db.commit()
                self.statusBar().showMessage('Mac Deleted')
                self.lineEdit.setText("")
                self.lineEdit_2.setText("")


        

    def search(self):
        # self.db = mysql.connector.connect(host='localhost' , user='root' , password ='shubh96S@' , db='data')
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()

        Number = self.lineEdit_2.text()

        if Number == "":
            buttonReply = QMessageBox.information(self,"Empty","Please Enter The Number")
        else: 
            sql = ''' SELECT * FROM mac WHERE Number = ? '''
            self.cur.execute(sql , [(Number)])
            
            data = self.cur.fetchone()

            try:   
                print(data)
                a = self.lineEdit.setText(data[0])
              
            
            except:
                buttonReply = QMessageBox.information(self,"Sorry","No such Mac Number in our  List please check Mac Number")


    def login(self):
        username = self.lineEdit_3.text()
        password = self.lineEdit_4.text()

        if password == "0230" and username == "shubhamlohar":
            print('user match')
            self.statusBar().showMessage('You Are Successfull Login')
            self.groupBox.setEnabled(True)
                
        else:
            self.groupBox.setEnabled(False)
            self.statusBar().showMessage('Invalid Username Or Password')



      
Stock_Manage,_ = loadUiType('ToolBar\Stock_Management.ui')
class Stock_Manager(QMainWindow,Stock_Manage):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("View")
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.setGeometry(400,200,771,301)
        self.setupUi(self)
        self.buttons()
        # self.groupBox.setEnabled(False)
        self.show()

    def buttons(self):
        self.pushButton_16.clicked.connect(self.search)

        pass


    def search(self):
        # self.db = mysql.connector.connect(host='localhost' , user='root' , password ='shubh96S@' , db='data')
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()

        Supplier_bill_No = self.lineEdit_88.text()

        if Supplier_bill_No == "":
            buttonReply = QMessageBox.information(self,"Empty","Please Enter The Artical Number")
        else: 
            sql = ''' SELECT * FROM add_products WHERE Supp_Bill = ? '''
            self.cur.execute(sql , [(Supplier_bill_No)])
            
            data = self.cur.fetchone()

            try:   
                print(data)
                a = self.lineEdit_17.setText(data[17])
                b = self.lineEdit_18.setText(data[3])
                c = self.lineEdit_19.setText(data[9])
                d = self.lineEdit_20.setText(data[11])

                e = int(self.lineEdit_19.text())
                f = int(self.lineEdit_20.text())
                    
                self.lineEdit_21.setText(str(e * f))


                g = self.lineEdit_22.setText(data[23])
                h = self.lineEdit_23.setText(data[24])

            except:
                buttonReply = QMessageBox.information(self,"Sorry","No such Bill Number in your local disk")

 
xi,_ = loadUiType('ToolBar\Claculator.ui')
class Calculator(QMainWindow,xi):
    def __init__(self):
        super().__init__()
        self.setGeometry(50,800,800,450)
        # self.setWindowIcon(QIcon,("salon.jpg"))
        self.setupUi(self)
        self.handlebutton()
        self.actions()
        self.show()


    def handlebutton(self):
        self.pushButton_10.clicked.connect(self.calculation)
        pass



    def calculation(self):
        result = self.lineEdit_2.text()
        final = eval(result)
        self.lineEdit_7.setText(str(final))
        self.lineEdit_2.setText(str(final))

    def actions(self):
        self.pushButton_21.clicked.connect(self.sum)
        self.pushButton_33.clicked.connect(self.minus)
        self.pushButton_47.clicked.connect(self.multi)
        self.pushButton_48.clicked.connect(self.div)
        self.pushButton_c.clicked.connect(self.clear)
        # self.pushButton_64.clicked.connect(self.exit)




        self.pushButton_1.clicked.connect(self.perform1)
        self.pushButton_2.clicked.connect(self.perform2)
        self.pushButton_3.clicked.connect(self.perform3)
        self.pushButton_4.clicked.connect(self.perform4)
        self.pushButton_5.clicked.connect(self.perform5)
        self.pushButton_6.clicked.connect(self.perform6)
        self.pushButton_7.clicked.connect(self.perform7)
        self.pushButton_8.clicked.connect(self.perform8)
        self.pushButton_9.clicked.connect(self.perform9)
        self.pushButton_0.clicked.connect(self.perform0)
        self.pushButton_c_3.clicked.connect(self.perform10)



    def sum(self):
        text = self.lineEdit_2.text()
        self.lineEdit_2.setText(text + "+")
    def minus(self):
        text = self.lineEdit_2.text()
        self.lineEdit_2.setText(text + "-")
    def multi(self):
        text = self.lineEdit_2.text()
        self.lineEdit_2.setText(text + "*")
    def div(self):
        text = self.lineEdit_2.text()
        self.lineEdit_2.setText(text + "/")
    def clear(self):
        self.lineEdit_2.setText("")
        self.lineEdit_7.setText("")


    def perform1(self):
        text = self.lineEdit_2.text()
        self.lineEdit_2.setText(text + "1")
    def perform2(self):
        text = self.lineEdit_2.text()
        self.lineEdit_2.setText(text + "2")
    def perform3(self):
        text = self.lineEdit_2.text()
        self.lineEdit_2.setText(text + "3")
    def perform4(self):
        text = self.lineEdit_2.text()
        self.lineEdit_2.setText(text + "4")
    def perform5(self):
        text = self.lineEdit_2.text()
        self.lineEdit_2.setText(text + "5")
    def perform6(self):
        text = self.lineEdit_2.text()
        self.lineEdit_2.setText(text + "6")
    def perform7(self):
        text = self.lineEdit_2.text()
        self.lineEdit_2.setText(text + "7")
    def perform8(self):
        text = self.lineEdit_2.text()
        self.lineEdit_2.setText(text + "8")
    def perform9(self):
        text = self.lineEdit_2.text()
        self.lineEdit_2.setText(text + "9")
    def perform0(self):
        text = self.lineEdit_2.text()
        self.lineEdit_2.setText(text + "0")
    def perform10(self):
        text = self.lineEdit_2.text()
        self.lineEdit_2.setText(text + ".")


bi,_ = loadUiType('ToolBar\Camera2.ui')
class CameraSetting(QMainWindow,bi):
    def __init__(self):
        super().__init__()
        self.setGeometry(0,0,800,450)
        # self.setWindowIcon(QIcon,("salon.jpg"))
        self.setupUi(self)
        # self.handlebutton()
        # self.actions()
        self.showNormal()
        self.show()

    






ko,_ = loadUiType('ToolBar\Setting.ui')
class Setting(QMainWindow,ko):
    def __init__(self):
        super().__init__()
        self.setGeometry(0,0,1366,768)
        # self.setWindowIcon(QIcon,("salon.jpg"))
        self.setupUi(self)
        self.handlebutton()
        # self.actions()
        self.show()
        
        
        
    def handlebutton(self):
        self.pushButton_2.clicked.connect(self.SetBill)
        self.pushButton.clicked.connect(self.search)
        self.pushButton_12.clicked.connect(self.delete)
        self.pushButton_3.clicked.connect(self.Update_BillFormat)
        pass
        
      
      
    def SetBill(self):
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()

        BillFormat = self.lineEdit_12.text()
        shopName = self.lineEdit_8.text()
        subTitle = self.lineEdit_9.text()
        shopKepperName = self.lineEdit_10.text()
        contact = self.lineEdit_11.text()
        try:
            data3 = (BillFormat,shopName,subTitle,shopKepperName,contact)
            sql = ''' INSERT INTO setting VALUES (?,?,?,?,?) '''

            self.cur.execute(sql,data3)
            message2 = QMessageBox.information(self,"Successfull!","Bill Format Save Successfully!.")
            self.db.commit()
            self.db.close()
        except:
            message2 = QMessageBox.warning(self,"Cuation!","Bill Format Already Exist, Please add new Bill Format")

        
    def search(self):
        # self.db = mysql.connector.connect(host='localhost' , user='root' , password ='shubh96S@' , db='data')
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()

        Bill_Format_No = self.lineEdit_7.text()

        if Bill_Format_No == "":
            buttonReply = QMessageBox.information(self,"Empty","Please Enter The Bill_Format_No")
        else: 
            sql = ''' SELECT * FROM setting WHERE FormatNo = ? '''
            self.cur.execute(sql , [(Bill_Format_No)])
            data = self.cur.fetchone()

            # try:   
            a = self.lineEdit_12.setText(data[0])
            b = self.lineEdit_8.setText(data[1])
            c = self.lineEdit_9.setText(data[2])
            d = self.lineEdit_10.setText(data[3])
            e = self.lineEdit_11.setText(data[4])
            # except:
            #     buttonReply = QMessageBox.information(self,"Sorry","No such Bill Number in your local disk")
                
                
                
                
    def delete(self):
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor() 

        bill_number = self.lineEdit_7.text()
        if bill_number == "":
            buttonreplay = QMessageBox.information(self,"Empty!","Please Enter The Bill Number")
        else:
            warning = QMessageBox.warning(self , 'Delete Product' , "Are you sure, You want to Delete this Bill Format?" , QMessageBox.Yes | QMessageBox.No)
            if warning == QMessageBox.Yes :
                sql = ''' DELETE FROM setting WHERE FormatNo = ? '''
                self.cur.execute(sql , [(bill_number)])
                self.db.commit()
                dfdsfsd = QMessageBox.information(self,"Updated","Bill Format Successfully Deleted!..")
                self.statusBar().showMessage('Bill Format Deleted')
                
                
    def Update_BillFormat(self):
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()

        BillNo = self.lineEdit_12.text()
        ShopN = self.lineEdit_8.text()
        Subtitle = self.lineEdit_9.text()
        ShopKepper = self.lineEdit_10.text()
        contact = self.lineEdit_11.text()
       
        UserNo = self.lineEdit_7.text()

        self.cur.execute(f"UPDATE setting SET Contact = {contact}, FormatNo = {BillNo} WHERE FormatNo = {UserNo}")
        self.db.commit()
        self.db.close()
        dfdsfsd = QMessageBox.information(self,"Updated","Bill Format Successfully Updated")