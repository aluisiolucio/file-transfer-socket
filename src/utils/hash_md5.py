import hashlib

def md5(texto):
    md5 = hashlib.md5()
    md5.update(texto.encode('utf-8'))

    return md5.hexdigest()
