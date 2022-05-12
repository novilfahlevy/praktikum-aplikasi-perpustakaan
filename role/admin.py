import sys
from datetime import datetime
from helper import bersihkan_console
from termcolor import colored

from role.role import Role
from model.pengguna import Pengguna
from model.penerbit import Penerbit
from model.pengadaan import Pengadaan, BukuPengadaan

class RoleAdmin(Role) :
	"""
		Role admin.
	"""

	def __init__(self, app) -> None :
		self.app = app
		self.tersimpan = False
		self.load_data_dari_database()

	def menu_admin(self, pesan=None) :
		try :
			bersihkan_console()
			print(f"Halaman: {colored('Admin', 'blue')}")

			nama = self.app.auth.session['nama']
			tersimpan = self.tersimpan
			print(f'{colored("Data tersimpan" if tersimpan else "Data tidak tersimpan", "green" if tersimpan else "red")} | {nama}')
			if pesan is not None : print(pesan)
			print('[1] Admin')
			print('[2] Petugas')
			print('[3] Penerbit')
			print('[4] Pengadaan')
			print('[5] Simpan Data')
			print('[6] Edit Profil')
			print(colored('[7] Keluar', 'yellow'))
			menu = input('Pilih:\n> ')

			if menu == '1' :
				return self.app.admin.menu_manajemen_admin()
			elif menu == '2' :
				return self.app.petugas.menu_manajemen_petugas()
			elif menu == '3' :
				return self.app.penerbit.menu_manajemen_penerbit()
			elif menu == '4' :
				return self.app.pengadaan.menu_manajemen_pengadaan()
			elif menu == '5' :
				return self.simpan_data()
			elif menu == '6' :
				return self.edit_profil()
			elif menu == '7' :
				return self.app.auth.logout()
			else :
				return self.menu_admin()

		except KeyboardInterrupt or EOFError :
			return self.app.main(force_close=True)

	def simpan_data(self) :
		try :
			if input('Simpan data (Y/n)? ').lower() == 'y' :
				if self.tersimpan == False :
					self.simpan_admin()
					self.simpan_petugas()
					self.simpan_penerbit()
					self.simpan_pengadaan()
					self.tersimpan = True
					return self.menu_admin(pesan=colored('Data berhasil disimpan.', 'green'))
				return self.menu_admin(pesan=colored('Semua data sudah tersimpan.', 'yellow'))
			return self.menu_admin()
			
		except Exception as e :
			sys.exit(e)

	def simpan_admin(self) -> None :
		for _, admin in enumerate(self.app.admin.data.tolist(semua=True)) :
			if admin.status_data == 'baru' :
				query = 'INSERT INTO pengguna VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'
				data = (
					admin.kode,
					admin.nama,
					admin.email,
					admin.password,
					admin.nomor_telepon,
					admin.alamat,
					'admin',
					admin.tanggal_dibuat,
				)
				self.app.db.sql(query=query, data=data)
			elif admin.status_data == 'hapus' :
				query = 'DELETE FROM pengguna WHERE kode = %s;'
				self.app.db.sql(query=query, data=(admin.kode,))

		self.app.admin.data.tetapkan_sebagai_tersimpan()
	
	def simpan_petugas(self) -> None :
		for _, petugas in enumerate(self.app.petugas.data.tolist(semua=True)) :
			if petugas.status_data == 'baru' :
				query = 'INSERT INTO pengguna VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'
				data = (
					petugas.kode,
					petugas.nama,
					petugas.email,
					petugas.password,
					petugas.nomor_telepon,
					petugas.alamat,
					'petugas',
					petugas.tanggal_dibuat,
				)
				self.app.db.sql(query=query, data=data)
			elif petugas.status_data == 'hapus' :
				query = 'DELETE FROM pengguna WHERE kode = %s;'
				self.app.db.sql(query=query, data=(petugas.kode,))

		self.app.petugas.data.tetapkan_sebagai_tersimpan()

	def simpan_penerbit(self) -> None :
		for _, penerbit in enumerate(self.app.penerbit.data.tolist(semua=True)) :
			if penerbit.status_data == 'baru' :
				query = 'INSERT INTO penerbit VALUES (%s, %s, %s, %s, %s);'
				data = (
					penerbit.kode,
					penerbit.nama,
					penerbit.email,
					penerbit.nomor_telepon,
					penerbit.alamat,
				)
				self.app.db.sql(query=query, data=data)
			elif penerbit.status_data == 'ubah' :
				query = (
					'UPDATE penerbit SET nama = %s, email = %s, nomor_telepon = %s, alamat = %s '
					'WHERE kode = %s;'
				)
				data = (
					penerbit.nama,
					penerbit.email,
					penerbit.nomor_telepon,
					penerbit.alamat,
					penerbit.kode,
				)
				self.app.db.sql(query=query, data=data)
			elif penerbit.status_data == 'hapus' :
				query = 'DELETE FROM penerbit WHERE kode = %s;'
				self.app.db.sql(query=query, data=(penerbit.kode,))

		self.app.penerbit.data.tetapkan_sebagai_tersimpan()
	
	def simpan_pengadaan(self) -> None :
		for _, pengadaan in enumerate(self.app.pengadaan.data.tolist(semua=True)) :
			print(pengadaan.status_data)
			if pengadaan.status_data == 'baru' :
				query = 'INSERT INTO pengadaan VALUES (%s, %s, %s);'
				data = (
					pengadaan.kode,
					pengadaan.kode_penerbit,
					datetime.strptime(pengadaan.tanggal, '%d-%m-%Y').strftime('%Y-%m-%d')
				)
				self.app.db.sql(query=query, data=data)

				buku_pengadaan = pengadaan.buku.tolist()
				for _, buku_pengadaan_data in enumerate(buku_pengadaan) :
					query = 'INSERT INTO buku_pengadaan VALUES (null, %s, %s, %s, %s);'
					data = (
						pengadaan.kode,
						buku_pengadaan_data.isbn,
						buku_pengadaan_data.harga,
						buku_pengadaan_data.jumlah,
					)

					buku = self.app.buku.data.cari(buku_pengadaan_data.isbn, 'isbn')

					# cek apakah buku sudah ada
					buku_lama = self.app.db.sql(query='SELECT jumlah FROM buku WHERE isbn = %s;', data=(buku.isbn,), hasil=lambda cursor: cursor.fetchone())
					if buku_lama is not None :
						self.app.db.sql(query='UPDATE buku SET jumlah = %s WHERE isbn = %s;', data=(int(buku.jumlah), buku.isbn))
					else :
						self.app.db.sql(query='INSERT INTO buku VALUES (%s, %s, %s, %s, %s, %s, %s);', data=(buku.kode, buku.isbn, '', '', '', 0, buku.jumlah))

					self.app.db.sql(query=query, data=data)
			
			elif pengadaan.status_data == 'hapus' :
				print(pengadaan.status_data)
				query = 'DELETE FROM pengadaan WHERE kode = %s;'
				self.app.db.sql(query=query, data=(pengadaan.kode,))

		self.app.pengadaan.data.tetapkan_sebagai_tersimpan()

	def load_data_dari_database(self) -> None :
		self.load_data_admin_dari_database()
		self.load_data_petugas_dari_database()
		self.load_data_penerbit_dari_database()
		self.load_data_pengadaan_dari_database()
		self.tersimpan = True

	def load_data_admin_dari_database(self) -> None :
		admin = self.app.db.sql(query="SELECT * FROM pengguna WHERE role = 'admin'", hasil=lambda cursor: cursor.fetchall())
		for _, _admin in enumerate(admin) :
			admin_model = Pengguna()
			admin_model.tetapkan_kode(_admin['kode'])
			admin_model.nama = _admin['nama']
			admin_model.email = _admin['email']
			admin_model.password = _admin['password']
			admin_model.nomor_telepon = _admin['nomor_telepon']
			admin_model.alamat = _admin['alamat']
			admin_model.role = _admin['role']
			admin_model.tanggal_dibuat = _admin['tanggal_dibuat']
			admin_model.status_data = 'lama'

			self.app.admin.data.insert(admin_model)

	def load_data_petugas_dari_database(self) -> None :
		petugas = self.app.db.sql(query="SELECT * FROM pengguna WHERE role = 'petugas'", hasil=lambda cursor: cursor.fetchall())
		for _, _petugas in enumerate(petugas) :
			petugas_model = Pengguna()
			petugas_model.tetapkan_kode(_petugas['kode'])
			petugas_model.nama = _petugas['nama']
			petugas_model.email = _petugas['email']
			petugas_model.password = _petugas['password']
			petugas_model.nomor_telepon = _petugas['nomor_telepon']
			petugas_model.alamat = _petugas['alamat']
			petugas_model.role = _petugas['role']
			petugas_model.tanggal_dibuat = _petugas['tanggal_dibuat']
			petugas_model.status_data = 'lama'

			self.app.petugas.data.insert(petugas_model)

	def load_data_penerbit_dari_database(self) -> None :
		penerbit = self.app.db.sql(query="SELECT * FROM penerbit", hasil=lambda cursor: cursor.fetchall())
		for _, _penerbit in enumerate(penerbit) :
			penerbit_model = Penerbit()
			penerbit_model.tetapkan_kode(_penerbit['kode'])
			penerbit_model.nama = _penerbit['nama']
			penerbit_model.email = _penerbit['email']
			penerbit_model.nomor_telepon = _penerbit['nomor_telepon']
			penerbit_model.alamat = _penerbit['alamat']
			penerbit_model.status_data = 'lama'

			self.app.penerbit.data.insert(penerbit_model)
	
	def load_data_pengadaan_dari_database(self) -> None :
		pengadaan = self.app.db.sql(query="SELECT * FROM pengadaan", hasil=lambda cursor: cursor.fetchall())
		for _, _pengadaan in enumerate(pengadaan) :
			pengadaan_model = Pengadaan()
			pengadaan_model.tetapkan_kode(_pengadaan['kode'])
			pengadaan_model.kode_penerbit = _pengadaan['kode_penerbit']
			pengadaan_model.tanggal = _pengadaan['tanggal']
			pengadaan_model.status_data = 'lama'

			buku_pengadaan = self.app.db.sql(
				query="SELECT * FROM buku_pengadaan WHERE kode_pengadaan = %s;",
				data=(_pengadaan['kode'],),
				hasil=lambda cursor: cursor.fetchall()
			)
			for _, _buku_pengadaan in enumerate(buku_pengadaan) :
				buku_pengadaan_model = BukuPengadaan()
				buku_pengadaan_model.kode_pengadaan = _pengadaan['kode']
				buku_pengadaan_model.isbn = _buku_pengadaan['isbn']
				buku_pengadaan_model.jumlah = _buku_pengadaan['jumlah']
				buku_pengadaan_model.harga = _buku_pengadaan['harga']
				buku_pengadaan_model.status_data = 'lama'

				pengadaan_model.tambah_buku(buku_pengadaan_model)

			self.app.pengadaan.data.insert(pengadaan_model)
