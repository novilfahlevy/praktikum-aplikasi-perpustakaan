from database import sql
from helper import bersihkan_console
from termcolor import colored
from auth import ambil_session, logout

class Admin :
	def __init__(self, petugas, penerbit) :
		self.petugas = petugas(self)
		self.penerbit = penerbit(self)
		# self.pengadaan = pengadaan(self)
		self.tersimpan = True

		self.menu_admin()

	def menu_admin(self, pesan=None) :
		try :
			bersihkan_console()
			print(colored('Admin', 'blue'))

			if pesan is not None : print(pesan)

			nama = ambil_session(ke_json=True)['nama']
			tersimpan = self.tersimpan
			print(f'{nama} | {colored("Data tersimpan" if tersimpan else "Data tidak tersimpan", "green" if tersimpan else "red")}')
			print('[1] Petugas')
			print('[2] Penerbit')
			print('[3] Pengadaan')
			print('[4] Simpan Data')
			print(colored('[5] Keluar', 'yellow'))
			menu = input('Pilih:\n> ')

			if menu == '1' :
				return self.petugas.menu_manajemen_petugas()
			elif menu == '2' :
				return self.penerbit.menu_manajemen_penerbit()
			elif menu == '3' :
				# return Pengadaan.menu_manajemen_pengadaan()
				print('Pengadaan')
			elif menu == '4' :
				if input('Simpan data? (Y/n)').lower() == 'y' :
					self.simpan_data()
			elif menu == '5' :
				return logout()
			else :
				return self.menu_admin()

		except KeyboardInterrupt :
			return self.menu_admin()

	def simpan_data(self) :
		sql(query='TRUNCATE TABLE IF EXTSIS pengguna, penerbit;')

		petugas = self.petugas.data
		penerbit = self.penerbit.data

		petugas_node = petugas.head
		petugas_values = ''
		hitung = 0
		while petugas_node is not None :
			hitung = hitung + 1
			id_pengguna, nama, email, password, nomor_telepon, alamat, role = petugas_node.data.values()
			petugas_values += '({}, {}, {}, {}, {}, {}, {}, now()){}'.format(id_pengguna, nama, email, password, nomor_telepon, alamat, role, ';' if hitung >= petugas.count() else ',')
			petugas_node = petugas_node.next
		
		penerbit_node = penerbit.head
		penerbit_values = ''
		hitung = 0
		while penerbit_node is not None :
			hitung = hitung + 1
			id_penerbit, nama, email, nomor_telepon, alamat = penerbit_node.data.values()
			penerbit_values += '({}, {}, {}, {}, {}){}'.format(id_penerbit, nama, email, nomor_telepon, alamat, ';' if hitung >= penerbit.count() else ',')
			penerbit_node = penerbit_node.next
			
		sql(query=f'INSERT INTO pengguna VALUES {petugas_values}')
		sql(query=f'INSERT INTO penerbit VALUES {penerbit_values}')

		self.tersimpan = True
		return self.menu_admin()