"""
  File untuk melakukan testing
"""

from termcolor import colored
import math
from data_class import Queue

from helper import bersihkan_console

queue = Queue()

for i in range(37) :
  queue.enqueue(i + 1)

jumlah_data_per_halaman = 5
jumlah_seluruh_data = queue.size()
jumlah_halaman = math.ceil(jumlah_seluruh_data / jumlah_data_per_halaman)
halaman = 1


# print([i + 1 for i in range(5)][0:-4])
# (jumlah_data_per_halaman * jumlah_halaman) - jumlah_seluruh_data

aksi = None
while aksi != '' :
  bersihkan_console()
  print('Halaman {} / {}'.format(halaman, jumlah_halaman))
  
  data = queue.tolist(jumlah_data_per_halaman)
  if halaman >= jumlah_halaman and jumlah_seluruh_data > jumlah_data_per_halaman :
    data = data[0:-((jumlah_data_per_halaman * jumlah_halaman) - jumlah_seluruh_data)]
  print(data)
  
  aksi = input('\nAksi ({}: kiri, {}: kanan, {}: kembali) : '.format(colored('l', 'yellow'), colored('r', 'yellow'), colored('enter', 'yellow')))
  if aksi == 'l' :
    if halaman > 1 :
      queue.requeue_reverse(jumlah_data_per_halaman)
      halaman = halaman - 1
    else :
      halaman = 1  
  if aksi == 'r' :
    if halaman < jumlah_halaman :
      queue.requeue(jumlah_data_per_halaman)
      halaman = halaman + 1
    else :
      halaman = jumlah_halaman if jumlah_halaman > 0 else 1