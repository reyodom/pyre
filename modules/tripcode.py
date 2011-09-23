# Tripcode generator.
from crypt import crypt
import re
import string

def Make(ws, Channel, password):
  password = password.decode('utf-8')
  password = password.encode("sjis", "ignore")
  password = password.replace('"', "&quot;") \
         .replace("'", "'")      \
         .replace("<", "&lt;")   \
         .replace(">", "&gt;")   \
         .replace(",", ",")
  salt = re.sub(r"[^\.-z]", ".", (password + "H..")[1:3])
  salt = salt.translate(string.maketrans(r":;=?@[\]^_`", "ABDFGabcdef"))
  ws("PRIVMSG {0} :\x02Tripcode: !\x02{1}\r\n".format(Channel, crypt(password, salt)[-10:]))
  