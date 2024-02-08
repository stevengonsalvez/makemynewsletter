# from chatapp import hash_string

def hash_string(string):
    hashed = hash(string)
    print (type(hex(hashed)))
    return hashed

str = "https://github.com/stevengonsalvez/makemynewsletter"
print(hash_string(str))
