import math
import sys
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
        # self.pushButtonHelp.clicked.connect(self.pushHelpButton)

    def populateTable(self):
        products = ProductsList().getProducts()
        self.tableWidgetItems.setRowCount(math.ceil(len(products) / 5))
        i = 0
        j = 0
        for product in products:
            widget = ProductWidget()
            widget.setName(product["name"])
            widget.setImage(product["image"])
            self.tableWidgetItems.setCellWidget(i, j, widget)
            j = (j + 1) % 5
            i = i + 1 if j == 0 else i

    def pushButtonHelp(self):
        playsound(navSoundPath)


class ProductWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ProductWidget, self).__init__(parent)
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

# todo: widget pt lista, cu nume, pret, id(?), remove btn(?)
# todo: clase pt produse
# todo: callback pt enter cod
# todo: callback pt table cell

class SelfCheckoutMainWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(SelfCheckoutMainWidget, self).__init__()
        loadUi('selfCheckoutMainView.ui', self)

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

        self.populateList()

    def populateList(self):
        for i in range(3):
            myQCustomQWidget = ProductWidget()
            myQCustomQWidget.setName('avocado')
            myQListWidgetItem = QtWidgets.QListWidgetItem(self.listWidgetProducts)
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            self.listWidgetProducts.addItem(myQListWidgetItem)
            self.listWidgetProducts.setItemWidget(myQListWidgetItem, myQCustomQWidget)

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

    def pushFinishButton(self):
        playsound(navSoundPath)

    def pushButtonHelp(self):
        playsound(navSoundPath)


class SelfCheckoutApp(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
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

    def openMainView(self):
        playsound(navSoundPath)
        self.stack.setCurrentIndex(1)

    def openSearchView(self):
        playsound(navSoundPath)
        self.stack.setCurrentIndex(2)


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
