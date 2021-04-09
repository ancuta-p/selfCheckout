import math
import sys
import threading

import speech_recognition as sr
import pyttsx3

from playsound import playsound

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUi

from product import ProductsList

navSoundPath = './sounds/navigation_selection-complete-celebration2.wav'
tapSoundPath = './sounds/ui_tap-variant-03.wav'


class SelfCheckoutStartWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(SelfCheckoutStartWidget, self).__init__()
        loadUi('selfCheckoutStartView.ui', self)


class SelfCheckoutSearchWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(SelfCheckoutSearchWidget, self).__init__()
        loadUi('selfCheckoutSearchView.ui', self)
        self.populateTable()
        self.tableWidgetItems.cellClicked.connect(self.tableItemClicked)
        # self.pushButtonHelp.clicked.connect(self.pushHelpButton)

    def populateTable(self):
        products = ProductsList().getProducts()
        self.tableWidgetItems.setRowCount(math.ceil(len(products) / 5))
        i = 0
        j = 0
        for product in products:
            widget = TableProductWidget()
            widget.setName(product["name"])  # id  hidden?
            widget.setImage(product["image"])
            self.tableWidgetItems.setCellWidget(i, j, widget)
            j = (j + 1) % 5
            i = i + 1 if j == 0 else i

    def tableItemClicked(self, row, column):
        product = self.tableWidgetItems.cellWidget(row, column)
        if product:
            print(product.labelName.text())
            playsound(navSoundPath)
            # self.pushButtonBack.click()

    def pushButtonHelp(self):
        playsound(navSoundPath)


class TableProductWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TableProductWidget, self).__init__(parent)
        self.layout = QtWidgets.QVBoxLayout()
        self.labelName = QtWidgets.QLabel()
        self.labelImage = QtWidgets.QLabel()
        self.layout.addWidget(self.labelName)
        self.layout.addWidget(self.labelImage)
        self.setLayout(self.layout)

    def setName(self, text):
        self.labelName.setText(text)

    def setImage(self, imagePath):
        self.labelImage.setPixmap(QtGui.QPixmap(imagePath).scaled(100, 100))


class ListProductWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ListProductWidget, self).__init__(parent)
        self.layout = QtWidgets.QHBoxLayout()
        self.labelName = QtWidgets.QLabel()
        self.labelPrice = QtWidgets.QLabel()
        self.pushButtonRemove = QtWidgets.QPushButton('Remove')
        self.pushButtonRemove.setMaximumWidth(60)

        self.layout.addWidget(self.labelName)
        self.layout.addWidget(self.labelPrice)
        self.layout.addWidget(self.pushButtonRemove)
        self.setLayout(self.layout)

    def setName(self, text):
        self.labelName.setText(text)

    def setPrice(self, text):
        self.labelPrice.setText(f'{text} $')


class SelfCheckoutMainWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(SelfCheckoutMainWidget, self).__init__()
        loadUi('selfCheckoutMainView.ui', self)

        self.productList = ProductsList()
        self.total = 0

        self.pushButtonNo0.clicked.connect(lambda: self.pushNumber(0))
        self.pushButtonNo1.clicked.connect(lambda: self.pushNumber(1))
        self.pushButtonNo2.clicked.connect(lambda: self.pushNumber(2))
        self.pushButtonNo3.clicked.connect(lambda: self.pushNumber(3))
        self.pushButtonNo4.clicked.connect(lambda: self.pushNumber(4))
        self.pushButtonNo5.clicked.connect(lambda: self.pushNumber(5))
        self.pushButtonNo6.clicked.connect(lambda: self.pushNumber(6))
        self.pushButtonNo7.clicked.connect(lambda: self.pushNumber(7))
        self.pushButtonNo8.clicked.connect(lambda: self.pushNumber(8))
        self.pushButtonNo9.clicked.connect(lambda: self.pushNumber(9))

        self.pushButtonNoBack.clicked.connect(self.pushBackButton)
        self.pushButtonNoCancel.clicked.connect(self.pushCancelButton)
        self.pushButtonEnter.clicked.connect(self.pushEnterButton)
        self.pushButtonFinish.clicked.connect(self.pushFinishButton)

    def _addToList(self, item):
        listItem = ListProductWidget()
        listItem.setName(item['name'])
        listItem.setPrice(item['price'])
        listItem.pushButtonRemove.clicked.connect(self._removeFromList)
        myQListWidgetItem = QtWidgets.QListWidgetItem(self.listWidgetProducts)
        myQListWidgetItem.setSizeHint(listItem.sizeHint())
        self.listWidgetProducts.addItem(myQListWidgetItem)
        self.listWidgetProducts.setItemWidget(myQListWidgetItem, listItem)

        self.total += item['price']
        self.labelTotalValue.setText(f'{self.total} $')

    def _removeFromList(self):
        # todo: T.T
        row = self.listWidgetProducts.currentRow()
        widgetItem = self.listWidgetProducts.item(row)
        item = self.listWidgetProducts.itemWidget(widgetItem)
        print(row)
        self.listWidgetProducts.takeItem(row)

        self.total -= int(item.labelPrice.text().replace(' $', ''))
        self.labelTotalValue.setText(f'{self.total} $')

    def pushNumber(self, no):
        playsound(tapSoundPath)
        text = self.plainTextEditCode.toPlainText()
        self.plainTextEditCode.setPlainText(text + str(no))

    def pushBackButton(self):
        playsound(tapSoundPath)
        text = self.plainTextEditCode.toPlainText()
        self.plainTextEditCode.setPlainText(text[:-1])

    def pushCancelButton(self):
        playsound(tapSoundPath)
        self.plainTextEditCode.setPlainText('')

    def pushEnterButton(self):
        playsound(navSoundPath)
        code = self.plainTextEditCode.toPlainText()
        if code:
            product = self.productList.getProductById(code)
            if product:
                print(product)
                self._addToList(product)
            else:
                messageBox = QtWidgets.QMessageBox()
                messageBox.setText(f'No product found with id {code}')
                messageBox.exec_()

    def pushFinishButton(self):
        playsound(navSoundPath)

    def pushButtonHelp(self):
        playsound(navSoundPath)


class SelfCheckoutApp(QtWidgets.QMainWindow):

    def __init__(self):
        super(SelfCheckoutApp, self).__init__()
        loadUi('selfCheckoutMainForm.ui', self)

        self.startWidget = SelfCheckoutStartWidget()
        self.mainWidget = SelfCheckoutMainWidget()
        self.searchWidget = SelfCheckoutSearchWidget()
        self.stack = QtWidgets.QStackedWidget()

        self.stack.addWidget(self.startWidget)
        self.stack.addWidget(self.mainWidget)
        self.stack.addWidget(self.searchWidget)

        self.startWidget.pushButtonStart.clicked.connect(self.openMainView)
        self.mainWidget.pushButtonSearch.clicked.connect(self.openSearchView)
        self.searchWidget.pushButtonBack.clicked.connect(self.openMainView)

        self.setCentralWidget(self.stack)

        threading.Thread(target=self.listen, daemon=True).start()

    def openMainView(self):
        playsound(navSoundPath)
        self.stack.setCurrentIndex(1)

    def openSearchView(self):
        playsound(navSoundPath)
        self.stack.setCurrentIndex(2)

    def clickStart(self):
        if self.stack.currentIndex() == 0:
            self.startWidget.pushButtonStart.click()

    def clickEnter(self):
        if self.stack.currentIndex() == 1:
            self.mainWidget.pushButtonEnter.click()

    def clickSearch(self):
        if self.stack.currentIndex() == 1:
            self.mainWidget.pushButtonSearch.click()

    def clickFinish(self):
        if self.stack.currentIndex() == 1:
            self.mainWidget.pushButtonFinish.click()

    def clickBack(self):
        if self.stack.currentIndex() == 2:
            self.searchWidget.pushButtonBack.click()

    def _speechToText(self, recognizer, microphone):
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        response = {"success": True,
                    "error": None,
                    "transcription": None}
        try:
            response["transcription"] = recognizer.recognize_google(audio)
        except sr.RequestError:
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            response["success"] = False
            response["error"] = "Unable to recognize speech"
        return response

    def _runCmd(self, text):
        if text == "hello" or text == "start":
            self.clickStart()
        if text == "enter":
            self.clickEnter()
        if text == "search item":
            self.clickSearch()
        if text == "back":
            self.clickBack()
        if text.find("finish") != -1 or text.find("pay") != -1:
            self.clickFinish()
        if text == "exit":
            self.close()

    def listen(self):
        engine = pyttsx3.init()
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()

        action = 'Listening'
        print(action)

        quitFlag = True
        while (quitFlag):
            text = self._speechToText(recognizer, microphone)
            if not text["success"] and text["error"] == "API unavailable":
                print("ERROR: {}\nclose program".format(text["error"]))
                break
            while not text["success"]:
                print("I didn't catch that. What did you say?\n")
                text = self._speechToText(recognizer, microphone)

            self._runCmd(text["transcription"].lower())

            if text["transcription"].lower() == "exit":
                quitFlag = False

            print(text["transcription"].lower())
            # self._textToSpeech(engine, text["transcription"].lower())


def main():
    with open("style.qss", "r") as f:
        style = f.read()

    app = QApplication(sys.argv)
    app.setStyleSheet(style)
    form = SelfCheckoutApp()

    form.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
