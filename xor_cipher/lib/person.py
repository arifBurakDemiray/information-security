# Arif Burak Demiray - 250201022 - 28.04.2022 - hw1 - ceng418
from PyQt5.QtWidgets import QInputDialog, QPushButton, QPlainTextEdit
from lib.cipher import Cipher
from lib.test_helper import pow_custom

# this class holds person related datas


class Person(QPlainTextEdit):
    def __init__(self, name: 'str', key: 'int', g: 'int', p: 'int', vector: 'int', parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setPlainText(name)
        self.name = name
        self.__key = key
        self.g = g
        self.p = p
        self.public = 0
        self.receivedPublics = dict()
        self.vector = vector

    def getChildButton(self):
        btn = QPushButton("Message")
        btn.clicked.connect(self.__buttonClicked)

        return btn

    def __buttonClicked(self):
        text, ok = QInputDialog.getText(self, 'Chat', 'Enter your message:')
        if ok:
            self.__sendMessageToAll(str(text))

    def __sendMessageToAll(self, text: 'str'):
        subscriptions: 'list[Person]' = self.receivedPublics.values()

        for receiver in subscriptions:  # calc shared to encrytp
            cipher = Cipher(self.vector, pow_custom(receiver.public, self.__key, self.p))
            cipherMessage = cipher.xor_cpc_encrypt(text)
            self.__log(["Sending message <..|" + text + "|..> to user <..|" + receiver.name + "|..>",
                        "Encrypted message <..|" + self.__makePrintable(cipherMessage) + "|..>"])
            receiver.handleMessage(cipherMessage, self.name)

    def __log(self, messages: 'list[str]') -> None:
        for message in messages:
            self.appendPlainText(message)

        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

    def handleMessage(self, message, sender: 'str'):
        senderEx = self.receivedPublics[sender]

        if(senderEx is None):
            self.__log(["There is no person named " + sender])
            return

        cipher = Cipher(self.vector, pow_custom(senderEx.public, self.__key, self.p))
        decryptedMessage = cipher.xor_cbc_decrypt(message)

        self.__log(["Received message <..|" + self.__makePrintable(message) + "|..> from user <..|" + sender + "|..>",
                    "Received decrypted message <..|" + decryptedMessage.decode('utf-8') + "|..>"])

    def __makePrintable(self, message: 'list[int]'):
        text = ""
        for i in message:
            if(i > 0x10ffff):
                text += hex(i)
            else:
                text += chr(i)

        return text

    def initVariables(self):
        self.public = pow_custom(self.g, self.__key, self.p)
        self.__log(["Private Key: " + str(self.__key), "Public Key: " + str(self.public)])

    def exchange(self, person: 'Person'):
        self.receivedPublics[person.name] = person
        self.__log(["Received public key " + str(person.public) + " from " + person.name,
                    "Calculated shared key " + str(pow_custom(person.public, self.__key, self.p))])
