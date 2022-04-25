from datetime import datetime
import sys
from database import sql
from helper import bersihkan_console
from termcolor import colored

from role.user import BaseUser

class RoleAdmin(BaseUser) :
	"""
		Role admin.
	"""

	def __init__(self, app) :
		self.app = app
		self.tersimpan = False

		self.ambil_database()

	def menu_admin(self, pesan=None) :
		try :
			bersihkan_console()
			print(f"Halaman: {colored('Admin', 'blue')}")

			nama = self.app.auth.session['nama']
			tersimpan = self.tersimpan
			print(f'{colored("Data tersimpan" if tersimpan else "Data tidak tersimpan", "green" if tersimpan else "red")} | {nama}')
			if pesan is not None : print(pesan)
			print('[1] Petugas')
			print('[2] Penerbit')
			print('[3] Pengadaan')
			print('[4] Simpan Data')
			print('[5] Edit Profil')
			print(colored('[6] Keluar', 'yellow'))
			menu = input('Pilih:\n> ')

			if menu == '1' :
				return self.app.petugas.menu_manajemen_petugas()
			elif menu == '2' :
				return self.app.penerbit.menu_manajemen_penerbit()
			elif menu == '3' :
				return self.app.pengadaan.menu_manajemen_pengadaan()
			elif menu == '4' :
				return self.simpan_data()
			elif menu == '5' :
				return self.edit_profil()
			elif menu == '6' :
				return self.app.auth.logout()
			else :
				return self.menu_admin()

		except KeyboardInterrupt :
			return self.app.main(force_close=True)

	def simpan_data(self) :
		try :
			if input('Simpan data (Y/n)? ').lower() == 'y' :
				if self.tersimpan == False :
					self.simpan_petugas()
					self.simpan_penerbit()
					self.simpan_pengadaan()
					self.tersimpan = True
					return self.menu_admin(pesan=colored('Data berhasil disimpan.', 'green'))
				return self.menu_admin(pesan=colored('Semua data sudah tersimpan.', 'yellow'))
			return self.menu_admin()
			
		except Exception as e :
			sys.exit(e)

	def simpan_petugas(self) :
		petugas = self.app.petugas.data
		petugas_list = petugas.tolist(with_trashed=True)
		for i in range(len(petugas_list)) :
			petugas_data = petugas_list[i]
			if petugas_data['status_data'] == 'baru' :
				query = 'INSERT INTO pengguna VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'
				data = (
					petugas_data['kode'],
					petugas_data['nama'],
					petugas_data['email'],
					petugas_data['password'],
					petugas_data['nomor_telepon'],
					petugas_data['alamat'],
					'petugas',
					petugas_data['tanggal_dibuat'],
				)
				sql(query=query, data=data)
			elif petugas_data['status_data'] == 'hapus' :
				query = 'DELETE FROM pengguna WHERE kode = %s;'
				sql(query=query, data=(petugas_data['kode'],))

		self.app.petugas.data.tetapkan_sebagai_tersimpan()

	def simpan_penerbit(self) :
		penerbit = self.app.penerbit.data
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

		self.app.penerbit.data.tetapkan_sebagai_tersimpan()
	
	def simpan_pengadaan(self) :
		pengadaan = self.app.pengadaan.data
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

					buku = self.app.buku.data.search(detail_pengadaan_data['isbn'], 'isbn')

					# cek apakah buku sudah ada
					buku_lama = sql(query='SELECT jumlah FROM buku WHERE isbn = %s;', data=(buku['isbn'],), hasil=lambda cursor: cursor.fetchone())
					if buku_lama is not None :
						sql(
							query='UPDATE buku SET jumlah = %s WHERE isbn = %s;',
							data=(int(buku['jumlah']), buku['isbn'])
						)
					else :
						sql(
							query='INSERT INTO buku VALUES (%s, %s, %s, %s, %s, %s, %s);',
							data=(buku['kode'], buku['isbn'], '', '', '', 0, buku['jumlah'])
						)

					sql(query=query, data=data)
			
			elif pengadaan_data['status_data'] == 'hapus' :
				query = 'DELETE FROM pengadaan WHERE kode = %s;'
				sql(query=query, data=(pengadaan_data['kode'],))

		self.app.pengadaan.data.tetapkan_sebagai_tersimpan()

	def ambil_database(self) :
		petugas = sql(query="SELECT * FROM pengguna WHERE role = 'petugas'", hasil=lambda cursor: cursor.fetchall())
		penerbit = sql(query="SELECT * FROM penerbit", hasil=lambda cursor: cursor.fetchall())
		pengadaan = sql(query="SELECT * FROM pengadaan", hasil=lambda cursor: cursor.fetchall())

		self.ambil(self.app.petugas, petugas)
		self.ambil(self.app.penerbit, penerbit)
		self.ambil(self.app.pengadaan, pengadaan, self.ambil_detail_pengadaan)

		self.tersimpan = True

	def ambil_detail_pengadaan(self, data) :
		kode_pengadaan = data['kode']
		pengadaan = sql(query="SELECT * FROM detail_pengadaan WHERE kode_pengadaan = %s", data=(kode_pengadaan,), hasil=lambda cursor: cursor.fetchall())
		data['detail_pengadaan'] = pengadaan
