import sys
from PyQt4 import Qt,QtGui,QtCore,QtSql,QtWebKit
import MainWindow,MySQLdb,urllib

class My_Thread(QtCore.QThread):        # making new thread class and inheriting class QThread
    def __init__(self,parent=None):               #  class constructor
        QtCore.QThread.__init__(self)
        self.parent = parent
        db=MySQLdb.connect("localhost",'root',"",'dancebook')       # to connect to database
        sql_query ="select name from dance"                         # to make the query
        cur = db.cursor()                                           # cursor object
        cur.execute(sql_query)                                      # executing the query through cursor object
        f=cur.fetchall()    # for fetching the data of query
        db.close()
        # print f
        v = [x[0] for x in f]
        # print v
        model = QtGui.QStringListModel()
        model.setStringList(v)

        completer = QtGui.QCompleter()
        completer.setModel(model)

        lineedit = self.parent.ui.lineEdit
        lineedit.setCompleter(completer)
        lineedit.show()
        # self.emit(QtCore.SIGNAL("SearchBarValues"),v)



class App(QtGui.QMainWindow):
    def __init__(self,parent=None):
        QtGui.QMainWindow.__init__(self)

        self.ui = MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)

        self.db = QtSql.QSqlDatabase.addDatabase("QMYSQL")
        self.db.setHostName("localhost")
        self.db.setDatabaseName("dancebook")
        self.db.setUserName("root")
        self.db.setPassword("")
        self.db.open()

        self.model = QtSql.QSqlQueryModel()
        self.model.setQuery("SELECT name FROM dance",self.db)


        self.ui.dance_form_table.setModel(self.model)

        self.ui.dance_form_table.clicked.connect(self.selcon)

        self.ui.dance_form_table.setMaximumWidth(120)

        self.ui.plainTextEdit.setStyleSheet("""
            border: 2px solid black;
            background-color: #773467;
            color : #56DD35;
        """)

        self.o = My_Thread(self)     #objest of My_t=Thread class
        self.o.start()           # for starting the thread
        # QtCore.QObject.connect(self.o,QtCore.SIGNAL("SearchBarValues"),self.updateSearchBar)

    # def updateSearchBar(self,val):
    #     print "In SLot"
    #     print val

    def selcon(self):
        # QtGui.QMessageBox.about(self,"Info","Application is started")
        index = self.ui.dance_form_table.selectedIndexes()[0]
        crawler = self.model.itemData(index)
        c=crawler[0].toString()
        db=MySQLdb.connect("localhost",'root',"",'dancebook')
        sql_query="select pioneer,pioneer_name,video,about_pioneer,about_dance from dance where name='%s'"%c
        # print sql_query
        con = db.cursor()
        con.execute(sql_query)
        # print con.fetchone()
        v = con.fetchone()
        p = v[0]
        pn = v[1]
        pv = v[2]
        ap = v[3]
        ad = v[4]
        print pv
        # try:
        #     img_data=urllib.urlopen(p).read()
        #
        #     pixmap = QtGui.QPixmap()
        #     pixmap.loadFromData(img_data)
        #
        #     self.ui.label.setPixmap(pixmap)
        # except:
        #     print "Image is Not Loaded!"

        self.imgThread = MyThread(p)
        self.imgThread.start()
        QtCore.QObject.connect(self.imgThread,QtCore.SIGNAL("UpdateImage"),self.updateImage)
        # QtCore.QObject.connect(self.ui.actionExit,QtCore.SIGNAL("triggered"),self.closeApp)
        self.ui.actionExit.triggered.connect(self.closeApp)

        self.ui.plainTextEdit.clear()
        self.ui.plainTextEdit_2.clear()
        self.ui.plainTextEdit.setReadOnly(True)
        self.ui.plainTextEdit_2.setReadOnly(True)


        self.ui.plainTextEdit.appendPlainText(pn)
        self.ui.plainTextEdit.appendPlainText(ap)
        self.ui.plainTextEdit_2.appendPlainText(ad)

        self.ui.webView.settings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled,True)
        # QtWebKit.QWebSettings.globalSettings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled,True)
        self.ui.webView.setHtml(pv)
        self.ui.webView.show()



        db.close()

    def updateImage(self,pixmap):
        self.ui.label.setPixmap(pixmap)

    def closeApp(self):
        print "window should be closed"
        QtGui.QMessageBox.information(self,"Information","This Window is About to Close!!!")
        sys.exit(0)


class MyThread(QtCore.QThread):
    def __init__(self,img_url=None):
        QtCore.QThread.__init__(self)
        self.img_url=img_url
    def run(self):
         try:
            img_data=urllib.urlopen(self.img_url).read()

            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(img_data)
            self.emit(QtCore.SIGNAL("UpdateImage"),pixmap)
            # self.parent.label.setPixmap(pixmap)
         except:
             print "Image data is not Loaded!!!"


if __name__=='__main__':
    app = Qt.QApplication(sys.argv)
    main_app = App()
    main_app.show()
    app.exec_()