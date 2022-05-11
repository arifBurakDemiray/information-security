# Arif Burak Demiray - 250201022 - 28.04.2022 - hw1 - ceng418
# this class makes encrypt and decrypt ops
class Cipher:

    vector: 'int'
    shared: 'int'

    def __init__(self: 'Cipher', vector: 'int', shared: 'int') -> None:
        self.shared = shared
        self.vector = vector

    def xor_cpc_encrypt(self: 'Cipher', message: 'str') -> 'bytes':

        encryptedMessage = []
        prevKey = self.vector
        # convert to byte array
        for char in bytearray(message, 'utf-8'):
            # xor cipher them
            prevKey = (char ^ prevKey) ^ self.shared
            encryptedMessage.append(prevKey)

        return encryptedMessage

    def xor_cbc_decrypt(self: 'Cipher', cipher) -> 'bytes':
        decryptedMessage = []
        prevKey = self.vector
        # for each byte of cipher text
        for char in cipher:
            # xor them again
            tempBytes = (char ^ self.shared) ^ prevKey
            prevKey = char
            decryptedMessage.append(tempBytes)

        return bytes(decryptedMessage)
