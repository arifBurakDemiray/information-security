# Arif Burak Demiray - 250201022 - 28.04.2022 - hw1 - ceng418
from PyQt5.QtWidgets import QApplication, QLineEdit, QWidget, QFormLayout, QPushButton, QMessageBox, QInputDialog
from PyQt5.QtGui import QIntValidator
import sys
from lib.gptest import primeTest
from lib.gptest import generatorTest
from lib.person import Person
from lib.test_helper import ab_test

# main app


class XORCipherApp(QWidget):
    def __init__(self, parent=None):
        self.p = 0
        self.g = 0
        self.a = 0
        self.b = 0
        super().__init__(parent)

        e1 = QLineEdit()
        e1.setValidator(QIntValidator())
        e1.textChanged.connect(self.pChanged)

        e2 = QLineEdit()
        e2.setValidator(QIntValidator())
        e2.textChanged.connect(self.gChanged)

        flo = QFormLayout()
        flo.addRow("P Value", e1)
        flo.addRow("G Value", e2)
        btn = QPushButton("Continue")
        btn.clicked.connect(self.buttonClicked)
        flo.addWidget(btn)

        self.setLayout(flo)
        self.setWindowTitle("XOR Cipher")

    def pChanged(self, num):
        try:
            self.p = int(num)
        except ValueError:
            pass

    def gChanged(self, num):
        try:
            self.g = int(num)
        except ValueError:
            pass

    def aChanged(self, num):
        try:
            self.a = int(num)
        except ValueError:
            pass

    def bChanged(self, num):
        try:
            self.b = int(num)
        except ValueError:
            pass

    def buttonClicked(self):

        pResult = primeTest(self.p)
        if(self.p == self.g or not pResult):
            self.layout().addWidget(self.showMessage("Please provide a new P", "It is not prime"))
            return
        gResult = generatorTest(self.g, self.p)
        if(not gResult):
            self.layout().addWidget(self.showMessage("Please provide a new G", None))
            return

        self.abGetter()

    def buttonClickedAb(self):

        abResult = ab_test(self.a, self.b, self.g)

        if(not abResult):
            self.layout().addWidget(self.showMessage("Provide a new set of keys", None))
            return

        vector, ok = QInputDialog.getInt(self, 'IV vector', 'Value:')
        if not ok:
            self.layout().addWidget(self.showMessage("Please provide a number for vector", None))

        self.vector = int(vector)

        self.messageDialog()
        self.alice.initVariables()
        self.bob.initVariables()
        self.exchangePublics()

    def exchangePublics(self):
        self.bob.exchange(self.alice)
        self.alice.exchange(self.bob)

    def showMessage(self, text: 'str', addon: 'str') -> 'QMessageBox':
        msg = QMessageBox()
        msg.setText(text)
        msg.setInformativeText(addon)
        msg.setStandardButtons(QMessageBox.Ok)
        return msg

    def messageDialog(self):
        self.alice = Person("Alice", self.a, self.g, self.p, self.vector)
        self.bob = Person("Bob", self.b, self.g, self.p, self.vector)

        flo = QFormLayout()
        flo.addWidget(self.alice)
        flo.addWidget(self.alice.getChildButton())
        flo.addWidget(self.bob)
        flo.addWidget(self.bob.getChildButton())

        QWidget().setLayout(self.layout())
        self.setLayout(flo)

    def abGetter(self):
        e1 = QLineEdit()
        e1.setValidator(QIntValidator())
        e1.textChanged.connect(self.aChanged)

        e2 = QLineEdit()
        e2.setValidator(QIntValidator())
        e2.textChanged.connect(self.bChanged)

        flo = QFormLayout()
        flo.addRow("A Private Key", e1)
        flo.addRow("B Private Key", e2)
        btn = QPushButton("Continue")
        btn.clicked.connect(self.buttonClickedAb)
        flo.addWidget(btn)

        QWidget().setLayout(self.layout())
        self.setLayout(flo)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = XORCipherApp()
    win.show()
    sys.exit(app.exec_())
