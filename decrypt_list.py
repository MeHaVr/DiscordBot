from icecream import ic
import sys
import getpass
from crypto import password_decrypt

list_name = sys.argv[1]
crypted = open(f"{list_name}.txt").read()

password = getpass.getpass("Password: ")

try:
    clear = password_decrypt(crypted, password)
    print(clear.decode())
except:
    print('decrypt failed')
    
