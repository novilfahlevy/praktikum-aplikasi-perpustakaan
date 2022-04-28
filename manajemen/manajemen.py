import math
from helper import bersihkan_console
from termcolor import colored

class Manajemen :
  """
    Manajemen class.
  """

  def tampilkan_tabel_berhalaman(self, queue, tabel, data_format, title=None) :
    try :
      jumlah_data_per_halaman = 5
      jumlah_seluruh_data = queue.size()
      jumlah_halaman = math.ceil(jumlah_seluruh_data / jumlah_data_per_halaman)
      halaman = 1

      aksi = None
      while aksi != '' :
        bersihkan_console()
        if title : print(title)
        print('Jumlah data : {}'.format(colored(str(jumlah_seluruh_data), 'blue')))
        print('Halaman {} / {}'.format(halaman, colored(str(jumlah_halaman), 'blue')))
        
        data = queue.tolist(jumlah_data_per_halaman)
        if halaman >= jumlah_halaman and jumlah_seluruh_data > jumlah_data_per_halaman :
          data = data[0:-((jumlah_data_per_halaman * jumlah_halaman) - jumlah_seluruh_data)]
        
        tabel.clear_rows()
        for i in range(len(data)) :
          nomor = ((halaman * jumlah_data_per_halaman) - jumlah_data_per_halaman) + (i + 1)
          tabel.add_row([nomor, *data_format(data[i])])

        print(tabel)
        
        aksi = input('\nAksi ({}: kiri, {}: kanan, {}: kembali) : '.format(colored('l', 'yellow'), colored('r', 'yellow'), colored('enter', 'yellow')))
        if aksi == 'l' :
          if halaman > 1 :
            queue.requeue()
            halaman = halaman - 1
          else :
            halaman = 1  
        if aksi == 'r' :
          if halaman < jumlah_halaman :
            queue.requeue_reverse()
            halaman = halaman + 1
          else :
            halaman = jumlah_halaman if jumlah_halaman > 0 else 1
      
    except KeyboardInterrupt or EOFError :
      pass
        