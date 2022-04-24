from datetime import datetime
from database import sql
from helper import bersihkan_console, hash_password
from termcolor import colored

from auth import Auth
from role.user import User
from role.manajemen.penerbit import Penerbit
from role.manajemen.petugas import Petugas
from role.manajemen.pengadaan import Pengadaan
from role.manajemen.buku import Buku

class Admin(User) :
	def __init__(self, auth: Auth, petugas: Petugas, penerbit: Penerbit, pengadaan: Pengadaan, buku: Buku) :
		self.auth = auth
		self.petugas = petugas
		self.penerbit = penerbit
		self.pengadaan = pengadaan
		self.buku = buku

		self.petugas.initAdmin(self)
		self.penerbit.initAdmin(self)
		self.pengadaan.initAdmin(self)

		self.tersimpan = True

		self.ambil_database()

	def menu_admin(self, pesan=None) :
		try :
			bersihkan_console()
			print(f"Halaman: {colored('Admin', 'blue')}")

			if pesan is not None : print(pesan)

			nama = self.auth.ambil_session(ke_json=True)['nama']
			tersimpan = self.tersimpan
			print(f'{colored("Data tersimpan" if tersimpan else "Data tidak tersimpan", "green" if tersimpan else "red")} | {nama}')
			print('[1] Petugas')
			print('[2] Penerbit')
			print('[3] Pengadaan')
			print('[4] Simpan Data')
			print('[5] Edit Profil')
			print(colored('[6] Keluar', 'yellow'))
			menu = input('Pilih:\n> ')

			if menu == '1' :
				return self.petugas.menu_manajemen_petugas()
			elif menu == '2' :
				return self.penerbit.menu_manajemen_penerbit()
			elif menu == '3' :
				return self.pengadaan.menu_manajemen_pengadaan()
			elif menu == '4' :
				if input('Simpan data (Y/n)? ').lower() == 'y' :
					if self.simpan_data() :
						return self.menu_admin(pesan=colored('Data berhasil disimpan.', 'green'))
					return self.menu_admin(pesan=colored('Gagal menyimpan data.', 'red'))
				return self.menu_admin()
			elif menu == '5' :
				return self.edit_profil()
			elif menu == '6' :
				return self.auth.logout()
			else :
				return self.menu_admin()

		except KeyboardInterrupt :
			return self.menu_admin()

	def simpan_data(self) :
		try :
			self.simpan_petugas()
			self.simpan_penerbit()
			self.simpan_pengadaan()
			self.tersimpan = True
			return True
		except :
			return False

	def simpan_petugas(self) :
		petugas = self.petugas.data
		petugas_list = petugas.tolist(with_trashed=True)
		for i in range(len(petugas_list)) :
			petugas_data = petugas_list[i]
			if petugas_data['status_data'] == 'baru' :
				query = 'INSERT INTO pengguna VALUES (%s, %s, %s, %s, %s, %s, %s, now());'
				data = (
					petugas_data['kode'],
					petugas_data['nama'],
					petugas_data['email'],
					petugas_data['password'],
					petugas_data['nomor_telepon'],
					petugas_data['alamat'],
					'petugas'
				)
				sql(query=query, data=data)
			elif petugas_data['status_data'] == 'hapus' :
				query = 'DELETE FROM pengguna WHERE kode = %s;'
				sql(query=query, data=(petugas_data['kode'],))

	def simpan_penerbit(self) :
		penerbit = self.penerbit.data
		penerbit_list = penerbit.tolist(with_trashed=True)
		for i in range(len(penerbit_list)) :
			penerbit_data = penerbit_list[i]
			if penerbit_data['status_data'] == 'baru' :
				query = 'INSERT INTO penerbit VALUES (%s, %s, %s, %s, %s);'
				data = (
					penerbit_data['kode'],
					penerbit_data['nama'],
					penerbit_data['email'],
					penerbit_data['nomor_telepon'],
					penerbit_data['alamat'],
				)
				sql(query=query, data=data)
			elif penerbit_data['status_data'] == 'ubah' :
				query = (
					'UPDATE penerbit SET nama = %s, email = %s, nomor_telepon = %s, alamat = %s '
					'WHERE kode = %s;'
				)
				data = (
					penerbit_data['nama'],
					penerbit_data['email'],
					penerbit_data['nomor_telepon'],
					penerbit_data['alamat'],
					penerbit_data['kode'],
				)
				sql(query=query, data=data)
			elif penerbit_data['status_data'] == 'hapus' :
				query = 'DELETE FROM penerbit WHERE kode = %s;'
				sql(query=query, data=(penerbit_data['kode'],))
	
	def simpan_pengadaan(self) :
		pengadaan = self.pengadaan.data
		pengadaan_list = pengadaan.tolist(with_trashed=True)
		
		for i in range(len(pengadaan_list)) :
			pengadaan_data = pengadaan_list[i]
			
			if pengadaan_data['status_data'] == 'baru' :
				query = 'INSERT INTO pengadaan VALUES (%s, %s, %s);'
				data = (
					pengadaan_data['kode'],
					pengadaan_data['kode_penerbit'],
					datetime.strptime(pengadaan_data['tanggal'], '%d-%m-%Y').strftime('%Y-%m-%d')
				)
				sql(query=query, data=data)

				detail_pengadaan = pengadaan_data['detail_pengadaan']
				for j in range(len(detail_pengadaan)) :
					detail_pengadaan_data = detail_pengadaan[j]
					query = 'INSERT INTO detail_pengadaan VALUES (null, %s, %s, %s, %s);'
					data = (
						pengadaan_data['kode'],
						detail_pengadaan_data['isbn'],
						detail_pengadaan_data['harga'],
						detail_pengadaan_data['jumlah'],
					)
					sql(query=query, data=data)
			
			elif pengadaan_data['status_data'] == 'hapus' :
				query = 'DELETE FROM pengadaan WHERE kode = %s;'
				sql(query=query, data=(pengadaan_data['kode'],))

	def ambil_database(self) :
		petugas = sql(query="SELECT * FROM pengguna WHERE role = 'petugas'", hasil=lambda cursor: cursor.fetchall())
		penerbit = sql(query="SELECT * FROM penerbit", hasil=lambda cursor: cursor.fetchall())
		pengadaan = sql(query="SELECT * FROM pengadaan", hasil=lambda cursor: cursor.fetchall())

		self.ambil(self.petugas, petugas)
		self.ambil(self.penerbit, penerbit)
		self.ambil(self.pengadaan, pengadaan, self.ambil_detail_pengadaan)

		self.tersimpan = True

	def ambil(self, linkedlist, list_data, nested=None) :
		for i in range(len(list_data)) :
			data = {}
			for j in list_data[i] : data[j] = list_data[i][j]
			if nested is not None : nested(data)
			linkedlist.data.insert(data, status='lama')

	def ambil_detail_pengadaan(self, data) :
		kode_pengadaan = data['kode']
		pengadaan = sql(query="SELECT * FROM detail_pengadaan WHERE kode_pengadaan = %s", data=(kode_pengadaan,), hasil=lambda cursor: cursor.fetchall())
		data['detail_pengadaan'] = pengadaan
