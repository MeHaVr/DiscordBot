from icecream import ic
import getpass
import sys
from crypto import password_encrypt

list_name = sys.argv[1]
clear = open(f"{list_name}_clear.txt").read()

password = getpass.getpass("Password: ")
crypted = password_encrypt(str.encode(clear), password)

print(f"writing new {list_name}.txt")
out = open(f'{list_name}.txt', 'wb')
out.write(crypted)
out.close()
