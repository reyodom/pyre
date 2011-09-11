# Tripcode generator
def Make(password):
  from crypt import crypt
  import re
  import string
  password = password.decode('utf-8')
  password = password.encode("sjis", "ignore")
  password = password.replace('"', "&quot;") \
         .replace("'", "'")      \
         .replace("<", "&lt;")   \
         .replace(">", "&gt;")   \
         .replace(",", ",")
  salt = re.sub(r"[^\.-z]", ".", (password + "H..")[1:3])
  salt = salt.translate(string.maketrans(r":;=?@[\]^_`", "ABDFGabcdef"))
  return crypt(password, salt)[-10:]