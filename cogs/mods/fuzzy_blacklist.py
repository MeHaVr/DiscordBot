from thefuzz import fuzz
import re
from icecream import ic
import getpass
import secrets
from crypto import password_decrypt

class FuzzyBlacklist:
  def __init__(self, bl_name, wl_name, max_score=95):
    self.max_score = max_score
    self.black_words = []
    self.white_words = []

    print(f"loading blacklist from {bl_name}")
    bl_crypted = open(bl_name).read()

    password = getpass.getpass("Password: ")
    try:
      bl = password_decrypt(bl_crypted, password).decode()
    except:
      print("decryption failed (blacklist)")
      exit()

    for line in bl.split('\n'):
      if line.strip() == '': continue
        
      self.black_words.append(line.rstrip())
   
    print(f"loading whitelist from {wl_name}")
    wl_crypted = open(wl_name).read()

    try:
      wl = password_decrypt(wl_crypted, password).decode()
    except:
      print("decryption failed (whitelist)")
      exit()

    for line in wl.split('\n'):
      if line.strip() == '': continue
      self.white_words.append(line.rstrip())

  def match(self, message):

    # remove all white listed words
    re.sub('|'.join(self.white_words),'',message)

    # prepare message
    stripped = re.sub("[^\w]",'', message).lower()
    unstripped = message.lower()

    for word in self.black_words:
      score_stripped = fuzz.partial_ratio(stripped, word)
      score_unstripped = fuzz.partial_ratio(unstripped, word)
      #ic(word, message, score_stripped, score_unstripped)
      if score_stripped > self.max_score or score_unstripped > self.max_score:
        # match
        return (score_stripped + score_unstripped)/2

    # no match
    return None


