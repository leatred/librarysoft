# -*- coding: utf-8 -*-
"""
Created on Thu May 21 23:31:03 2020

@author: Mustafa KAÇAR
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import *
import sys,os
import sqlite3 as sql
import datetime
from lib import Ui_MainWindow


class AnaProgram(QMainWindow,Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_Buttons()
        self.Show_Category()
        self.Show_Author()
        self.Show_Publisher()
        self.Show_All_Author()
        self.Show_All_Publisher()
        self.Show_All_Category()
        self.Show_All_Operation()
        self.Show_All_Books()
        self.Show_All_Students()
    def Handel_Buttons(self):
        self.pushButton_4.clicked.connect(self.Operations_Tab)
        self.pushButton_3.clicked.connect(self.Books_Tab)
        self.pushButton_2.clicked.connect(self.Students_Tab)
        self.pushButton_5.clicked.connect(self.Details_Tab)
        self.pushButton_8.clicked.connect(self.Add_Publisher)
        self.pushButton_9.clicked.connect(self.Add_Author)
        self.pushButton_10.clicked.connect(self.Add_Category)
        self.pushButton_14.clicked.connect(self.Add_Students)
        self.pushButton_11.clicked.connect(self.Search_Students)
        self.pushButton_13.clicked.connect(self.Delete_Students)
        self.pushButton_18.clicked.connect(self.Add_Book)
        self.pushButton_17.clicked.connect(self.Search_Book)
        self.pushButton_15.clicked.connect(self.Change_Book_Details)
        self.pushButton_16.clicked.connect(self.Delete_Book)
        self.pushButton_12.clicked.connect(self.Change_Students_Details)
        self.pushButton_6.clicked.connect(self.Add_Operation)
        self.pushButton.clicked.connect(self.Kitap_Geri_Al)
    def Operations_Tab(self):
        self.tabWidget.setCurrentIndex(0)
    def Books_Tab(self):
        self.tabWidget.setCurrentIndex(1)
    def Students_Tab(self):
        self.tabWidget.setCurrentIndex(2)
    def Details_Tab(self):
        self.tabWidget.setCurrentIndex(3)





        ######KİTABI GERİ AL######
    def Kitap_Geri_Al(self):
        adi=self.lineEdit_15.text()
        db=sql.connect("lib.db")
        cur=db.cursor()
        sorgu="UPDATE books SET status=? WHERE name=?"
        deger=(1,adi)
        cur.execute(sorgu,deger)
        db.commit()
        self.statusBar().showMessage("Kitap Başarıyla Geri Alındı!")
        self.pushButton.setEnabled(False)
        self.Search_Book()
        

        
        ######OPERATÄ°ONS######
    def Add_Operation(self):
        ogrencinumarasi=self.lineEdit.text()
        barkodu=self.lineEdit_17.text()
        gun=self.comboBox.currentText()
        tarih=datetime.datetime.now()
        tamtarih=tarih.strftime("%d.%m.%Y")
        if ogrencinumarasi!="" and barkodu!="":
            db=sql.connect("lib.db")
            cur=db.cursor()
            teslimtarihi=datetime.datetime.now() + datetime.timedelta(days=int(gun))
            tarihiduzenle=teslimtarihi.strftime("%d.%m.%Y")
            kitabibul="SELECT name,status from books where barcode=?"
            degeri=(barkodu,)
            cur.execute(kitabibul,degeri)
            kitapadi=cur.fetchall()
            if kitapadi!=[]:
                for kitaphangisi in kitapadi:
                    if kitaphangisi[1]>0:
                        ogrencibul="SELECT name from students where number=?"
                        ogrencino=(ogrencinumarasi,)
                        cur.execute(ogrencibul,ogrencino)
                        ogrencivarmi=cur.fetchall()
                        if ogrencivarmi!=[]:
                            sorgu="INSERT INTO operations(bookname,studentnumber,date,receive) VALUES (?,?,?,?)"
                            val=(kitaphangisi[0],ogrencinumarasi,tamtarih,tarihiduzenle)
                            cur.execute(sorgu,val)         
                            db.commit()
                            sorgu2="UPDATE books set status=? where barcode=?"
                            value=(0,barkodu)
                            cur.execute(sorgu2,value)
                            db.commit()
                            self.statusBar().showMessage("Kitap Başarıyla Zimmetlendi!")
                            self.lineEdit.setText("")
                            self.lineEdit_17.setText("")
                            self.tabWidget_2.setCurrentIndex(0) 
                            self.Show_All_Operation()
                        else:
                            self.statusBar().showMessage("Öğrenci Bulunamadı!")
                    else:
                        self.statusBar().showMessage("Kitap Başka Bir Öğrencide!")

            else:
                    self.statusBar().showMessage("Kitap Bulunamadı!")

        else:
            self.statusBar().showMessage("Lütfen Boş Alan Bırakmayınız!")
        
        
        
    def Show_All_Operation(self):
        db=sql.connect("lib.db")
        cur=db.cursor()
        sorgu="SELECT studentnumber,bookname, date, receive FROM operations order by id DESC"
        cur.execute(sorgu)
        data=cur.fetchall()
        if data:
            self.tableWidget.setRowCount(0)
            self.tableWidget.insertRow(0)
            for row, form in enumerate(data):
                for column, items in enumerate(form):
                    self.tableWidget.setItem(row,column,QTableWidgetItem(str(items)))
                    column+=1
                row_position=self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_position)
            
        ######BOOKS########
    def Add_Book(self):
        adi=self.lineEdit_19.text()
        barkodu=self.lineEdit_14.text()
        kategori=self.comboBox_5.currentText()
        yazar=self.comboBox_6.currentText()
        yayinci=self.comboBox_7.currentText()
        
        if adi!="" and barkodu!="":
            db=sql.connect("lib.db")
            cur=db.cursor()
            sorgu="INSERT INTO books(name,barcode,publisher,author,category,status) VALUES (?,?,?,?,?,?)"
            deger=(adi,barkodu,yayinci,yazar,kategori,1)
            cur.execute(sorgu,deger)
            db.commit()
            self.statusBar().showMessage("Kitap Başarıyla Eklendi!")
            self.lineEdit_19.setText("")
            self.lineEdit_14.setText("")
            self.tabWidget_3.setCurrentIndex(0)
            self.Show_All_Books()
        else:
            self.statusBar().showMessage("Lütfen Boş Alan Bırakmayınız!")
            
    def Search_Book(self):
        nameorbarcode=self.lineEdit_13.text()
        if nameorbarcode!="":
            db=sql.connect("lib.db")
            cur=db.cursor()
            sorgu="SELECT name,barcode,publisher,author,category,status FROM books where name=? or barcode=?"
            val=(nameorbarcode,nameorbarcode)
            cur.execute(sorgu,val)
            data=cur.fetchone()
            if data:
                self.groupBox_2.setEnabled(True)
                self.lineEdit_15.setText(data[0])
                self.lineEdit_16.setText(data[1])
                self.comboBox_2.setCurrentText(data[3])
                self.comboBox_3.setCurrentText(data[2])
                self.comboBox_4.setCurrentText(data[4])
                if data[5]==0:
                    self.lineEdit_4.setText("Zimmetli")
                    kimde="SELECT studentnumber FROM operations where bookname=? order by id DESC"
                    degeri=(data[0],)
                    cur.execute(kimde,degeri)
                    numarayibul=cur.fetchone()
                    if numarayibul!="":
                        for kim in numarayibul:
                            ogrenciadinibul="SELECT name FROM students where number=? "
                            ogrencino=(kim,)
                            cur.execute(ogrenciadinibul,ogrencino)
                    ogrenciadineymis=cur.fetchone()
                    self.pushButton.setEnabled(True)
                    for i in ogrenciadineymis:
                        self.label_27.setText("Bu kitap şuan " + i + " isimli öğrencide.")                        
                else:
                    self.lineEdit_4.setText("Rafta")
                    self.label_27.setText("")
            else:
                self.statusBar().showMessage("Kitap Bulunamadı!")
                self.groupBox_2.setEnabled(False)
                self.lineEdit_15.setText("")
                self.lineEdit_16.setText("")
                self.comboBox_2.setCurrentText("")
                self.comboBox_3.setCurrentText("")
                self.comboBox_4.setCurrentText("")
        
        else:
                self.statusBar().showMessage("Lütfen Boş Alan Bırakmayınız!")
                self.groupBox_2.setEnabled(False)
                self.lineEdit_15.setText("")
                self.lineEdit_16.setText("")
                self.comboBox_2.setCurrentText("")
                self.comboBox_3.setCurrentText("")
                self.comboBox_4.setCurrentText("")
           
    def Change_Book_Details(self):
        nameorbarcode=self.lineEdit_13.text()
        if nameorbarcode!="":
            adi=self.lineEdit_15.text()
            barkodu=self.lineEdit_16.text()
            kategori=self.comboBox_4.currentText()
            yazar=self.comboBox_2.currentText()
            yayinci=self.comboBox_3.currentText()
            db=sql.connect("lib.db")
            cur=db.cursor()
            sorgu="UPDATE books set name=?, barcode=?, category=?, author=?, publisher=? where name=? or barcode=?"
            val=(adi,barkodu,kategori,yazar,yayinci,nameorbarcode,nameorbarcode)
            cur.execute(sorgu,val)
            db.commit()
            self.statusBar().showMessage("Kitap Bilgileri Başarıyla Güncellendi!")
        else:
            self.statusBar().showMessage("Lütfen Boş Alan Bırakmayınız!")

           
    def Delete_Book(self):
        nameorbarcode=self.lineEdit_13.text()
        if nameorbarcode!="":
            onay=QMessageBox.warning(self,"Kitabı Sil","Kitabı Silmek İstediğinizden Emin Misiniz?", QMessageBox.Yes | QMessageBox.No)
            if onay==QMessageBox.Yes:
                db=sql.connect("lib.db")
                cur=db.cursor()
                sorgu="Delete from books where name=? or barcode=?"
                val=(nameorbarcode,nameorbarcode)
                cur.execute(sorgu,val)
                self.statusBar().showMessage("Kitap Başarıyla Silindi!")
                self.groupBox_2.setEnabled(False)
                self.lineEdit_15.setText("")
                self.lineEdit_16.setText("")
                self.comboBox_2.setCurrentText("")
                self.comboBox_3.setCurrentText("")
                self.comboBox_4.setCurrentText("")
        else:
            self.statusBar().showMessage("Lütfen Boş Alan Bırakmayınız!")
           
           
            
    def Show_All_Books(self):
        db=sql.connect("lib.db")
        cur=db.cursor()
        sorgu="SELECT name,barcode,publisher,author,category,status from books"
        cur.execute(sorgu)
        data=cur.fetchall()
        if data:
            self.tableWidget_6.setRowCount(0)
            self.tableWidget_6.insertRow(0)
            for row, form in enumerate(data):
                for column, items in enumerate(form):
                    self.tableWidget_6.setItem(row,column,QTableWidgetItem(str(items)))
                    column+=1
                row_position=self.tableWidget_6.rowCount()
                self.tableWidget_6.insertRow(row_position)
            ######DETAÄ°LS########
        
    def Add_Publisher(self):
        gelen=self.lineEdit_2.text()
        if gelen!="":
            db=sql.connect("lib.db")
            cur=db.cursor()
            sorgu="INSERT INTO publisher(name) VALUES (?)"
            val=(gelen,)
            cur.execute(sorgu,val)
            db.commit()
            self.statusBar().showMessage("Yayıncı Başarıyla Eklendi!")
            self.Show_All_Publisher()
            self.Show_Publisher()

        else:
            self.statusBar().showMessage("Lütfen Boş Alan Bırakmayınız!")

    def Add_Author(self):
        gelen=self.lineEdit_3.text()
        if gelen!="":
            db=sql.connect("lib.db")
            cur=db.cursor()
            sorgu="INSERT INTO author(name) VALUES (?)"
            val=(gelen,)
            cur.execute(sorgu,val)
            db.commit()
            self.statusBar().showMessage("Yazar Başarıyla Eklendi!")
            self.Show_All_Author()
            self.Show_Author()

        else:
            self.statusBar().showMessage("Lütfen Boş Alan Bırakmayınız!")

    def Add_Category(self):
        gelen=self.lineEdit_5.text()
        if gelen!="":
            db=sql.connect("lib.db")
            cur=db.cursor()
            sorgu="INSERT INTO category(name) VALUES (?)"
            val=(gelen,)
            cur.execute(sorgu,val)
            db.commit()
            self.statusBar().showMessage("Kategori Başarıyla Eklendi!")
            self.Show_All_Category()
            self.Show_Category()

        else:
            self.statusBar().showMessage("Lütfen Boş Alan Bırakmayınız!")
            
            
    def Show_All_Author(self):
        db=sql.connect("lib.db")
        cur=db.cursor()
        sorgu="SELECT name FROM author"
        cur.execute(sorgu)
        data=cur.fetchall()
        if data:
            self.tableWidget_3.setRowCount(0)
            self.tableWidget_3.insertRow(0)
            for row, form in enumerate(data):
                for column, items in enumerate(form):
                    self.tableWidget_3.setItem(row,column,QTableWidgetItem(str(items)))
                    column+=1
                row_position=self.tableWidget_3.rowCount()
                self.tableWidget_3.insertRow(row_position)
    def Show_All_Category(self):
        db=sql.connect("lib.db")
        cur=db.cursor()
        sorgu="SELECT name FROM category"
        cur.execute(sorgu)
        data=cur.fetchall()
        if data:
            self.tableWidget_4.setRowCount(0)
            self.tableWidget_4.insertRow(0)
            for row,form in enumerate(data):
                for column, items in enumerate(form):
                    self.tableWidget_4.setItem(row,column, QTableWidgetItem(str(items)))
                    column+=1
                row_position=self.tableWidget_4.rowCount()
                self.tableWidget_4.insertRow(row_position)
    def Show_All_Publisher(self):
        db=sql.connect("lib.db")
        cur=db.cursor()
        sorgu="SELECT name from publisher"
        cur.execute(sorgu)
        data=cur.fetchall()
        if data:
            self.tableWidget_2.setRowCount(0)
            self.tableWidget_2.insertRow(0)
            for row,form in enumerate(data):
                for column,items in enumerate(form):
                    self.tableWidget_2.setItem(row,column,QTableWidgetItem(str(items)))
                    column+=1
                    row_position=self.tableWidget_2.rowCount()
                    self.tableWidget_2.insertRow(row_position) 
        ###STUDENTS##
    def Delete_Students(self):
        gelen=self.lineEdit_6.text()
        if gelen!="":
            onay=QMessageBox.warning(self,"Öğrenciyi Sil","Öğrenciyi Silmek İstediğinizden Emin Misiniz?",QMessageBox.Yes | QMessageBox.No)
            if onay==QMessageBox.Yes:
                db=sql.connect("lib.db")
                cur=db.cursor()
                sorgu="DELETE FROM students where name=? or number=?"
                val=(gelen,gelen)
                cur.execute(sorgu,val)
                db.commit()
                self.statusBar().showMessage("Öğrenci Başarıyla Silindi!")
                self.groupBox.setEnabled(False)
                self.lineEdit_7.setText("")
                self.lineEdit_9.setText("")
                self.lineEdit_8.setText("")
                self.lineEdit_6.setText("")
        else:
            self.statusBar().showMessage("Lütfen Öğrenci Adı Giriniz!")
            
            
    def Add_Students(self):
        adi=self.lineEdit_11.text()
        numarasi=self.lineEdit_10.text()
        sinifi=self.lineEdit_12.text()
        if adi!="" and numarasi!="" and sinifi!="":
            db=sql.connect("lib.db")
            cur=db.cursor()
            sorgu="INSERT INTO students(name,number,class) VALUES (?,?,?)"
            val=(adi,numarasi,sinifi)
            cur.execute(sorgu,val)
            db.commit()
            self.statusBar().showMessage("Öğrenci Başarıyla Eklendi!")
            self.lineEdit_11.setText("")
            self.lineEdit_10.setText("")
            self.lineEdit_12.setText("")
            self.tabWidget_4.setCurrentIndex(0)
            self.Show_All_Students()
        else:
            self.statusBar().showMessage("Lütfen Boş Alan Bırakmayınız!")
            
            
    def Search_Students(self):
        gelen=self.lineEdit_6.text()
        if gelen!="":
            db=sql.connect("lib.db")
            cur=db.cursor()
            sorgu="SELECT name,number,class FROM students where name=? or number=?"
            val=(gelen,gelen)
            cur.execute(sorgu,val)
            data=cur.fetchone()
            if data:
                self.groupBox.setEnabled(True)
                self.lineEdit_7.setText(data[0])
                self.lineEdit_9.setText(data[1])
                self.lineEdit_8.setText(data[2])
                self.statusBar().showMessage("")
            else:
                self.statusBar().showMessage("Böyle Bir Öğrenci Bulunamadı!")
                self.groupBox.setEnabled(False)
                self.lineEdit_7.setText("")
                self.lineEdit_9.setText("")
                self.lineEdit_8.setText("")

        else:
            self.statusBar().showMessage("Lütfen Sorgulamak İstediğiniz Öğrencinin Adını Giriniz!")
            self.groupBox.setEnabled(False)
            self.lineEdit_7.setText("")
            self.lineEdit_9.setText("")
            self.lineEdit_8.setText("")


    def Change_Students_Details(self):
            gelen=self.lineEdit_6.text()
            adi= self.lineEdit_7.text()
            numarasi = self.lineEdit_9.text()
            sinifi=self.lineEdit_8.text()
            if adi!="" and numarasi!="" and sinifi!="":
                db=sql.connect("lib.db")
                cur=db.cursor()
                sorgu="UPDATE students set name=?,number=?,class=? where name=? or number=?"
                val=(adi,numarasi,sinifi,gelen,gelen)
                cur.execute(sorgu,val)
                db.commit()
                self.statusBar().showMessage("Öğrenci Bilgileri Güncellendi!")
                self.lineEdit_7.setText("")
                self.lineEdit_9.setText("")
                self.lineEdit_8.setText("")
                self.lineEdit_6.setText("")
            else: 
                self.statusBar().showMessage("Lütfen Boş Alan Bırakmayınız!")
                
                
    def Show_All_Students(self):
        db=sql.connect("lib.db")
        cur=db.cursor()
        sorgu="SELECT name,number,class FROM students"
        cur.execute(sorgu)
        data=cur.fetchall()
        if data:
            self.tableWidget_5.setRowCount(0)
            self.tableWidget_5.insertRow(0)
            for row, form in enumerate(data):
                for column, items in enumerate(form):
                    self.tableWidget_5.setItem(row,column,QTableWidgetItem(str(items)))
                    column+=1
                row_position=self.tableWidget_5.rowCount()
                self.tableWidget_5.insertRow(row_position)
                    
                    
        ###SHOW ALL COMBOBOX DETAÄ°LS######
    def Show_Category(self):
            db=sql.connect("lib.db")
            cur=db.cursor()
            sorgu="SELECT name FROM category"
            cur.execute(sorgu)
            data=cur.fetchall()
            self.comboBox_4.clear()
            self.comboBox_5.clear()
            for i in data:
                self.comboBox_4.addItem(i[0])
                self.comboBox_5.addItem(i[0])
                
        
        
    def Show_Author(self):
        db=sql.connect("lib.db")
        cur=db.cursor()
        sorgu="SELECT name FROM author"
        cur.execute(sorgu)
        data=cur.fetchall()
        self.comboBox_6.clear()
        self.comboBox_2.clear()
        for i in data:
            self.comboBox_6.addItem(i[0])
            self.comboBox_2.addItem(i[0])
            
    def Show_Publisher(self):
        db=sql.connect("lib.db")
        cur=db.cursor()
        sorgu="SELECT name FROM publisher"
        cur.execute(sorgu)
        data=cur.fetchall()
        self.comboBox_7.clear()
        self.comboBox_3.clear()
        for i in data:
            self.comboBox_3.addItem(i[0])
            self.comboBox_7.addItem(i[0])
def main():
    app=QApplication(sys.argv)
    window=AnaProgram()
    window.show()
    app.exec_()
if __name__ =="__main__":
    main()
    
