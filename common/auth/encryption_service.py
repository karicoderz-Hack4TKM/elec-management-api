from cryptography.fernet import Fernet


class EncryptionService:

    def encryptText(self, password, key):
        fernetObj = Fernet(key.encode())
        encPassword = (fernetObj.encrypt(password.encode()))
        return encPassword.decode("utf-8")

    def decryptText(self, passwordDigest, key):
        fernetObj = Fernet(key.encode())
        encPassword = (fernetObj.decrypt(passwordDigest.encode()))
        return encPassword.decode("utf-8")
