from datetime import datetime
from termcolor import colored
import os
import random
import string
import sys
import bcrypt
import math
import keyboard

def bersihkan_console() :
	os.system('clear' if sys.platform == 'linux' else 'cls')

def hash_password(password) :
	return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def currency(number) :
  return 'Rp{:0,.0f}'.format(number).replace('Rp-', '-Rp')

def cek_tanggal_valid(tanggal, format='%d-%m-%Y') :
  try :
    datetime.strptime(tanggal, format)
    return True
  except ValueError or EOFError :
    return False

def konversi_format(tanggal, dari_format, ke_format) :
  if cek_tanggal_valid(str(tanggal), dari_format) :
    return datetime.strptime(str(tanggal), dari_format).strftime(ke_format)
  return str(tanggal)

def kode_generator(size=6, chars=string.ascii_uppercase + string.digits):
  return (''.join(random.choice(chars) for _ in range(size))).lower()