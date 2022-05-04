import sys
from time import sleep
from helper import bersihkan_console, konversi_format
from termcolor import colored

from model.buku import Buku
from model.peminjaman import Peminjaman
from model.pengguna import Pengguna

from role.role import Role

class RolePetugas(Role) :
	"""
		Role petugas.
	"""

	def __init__(self, app) -> None :
		self.app = app
		self.tersimpan = True
		self.load_data_dari_database()

	def menu_petugas(self, pesan=None) :
		try :
			bersihkan_console()
			print(f"Halaman: {colored('Petugas', 'blue')}")

			if pesan is not None : print(pesan)

			nama = self.app.auth.session['nama']
			tersimpan = self.tersimpan
			print(f'{colored("Data tersimpan" if tersimpan else "Data tidak tersimpan", "green" if tersimpan else "red")} | {nama}')
			print('[1] Member')
			print('[2] Buku')
			print('[3] Peminjaman')
			print('[4] Simpan Data')
			print('[5] Edit Profil')
			print(colored('[6] Keluar', 'yellow'))
			menu = input('Pilih:\n> ')

			if menu == '1' :
				return self.app.member.menu_manajemen_member()
			elif menu == '2' :
				return self.app.buku.menu_manajemen_buku()
			elif menu == '3' :
				return self.app.peminjaman.menu_manajemen_peminjaman()
			elif menu == '4' :
				return self.simpan_data()
			elif menu == '5' :
				return self.edit_profil()
			elif menu == '6' :
				return self.app.auth.logout()
			else :
				return self.menu_petugas()

		except KeyboardInterrupt or EOFError :
			return self.app.main(force_close=True)

	def simpan_data(self) :
		try :
			if input('Simpan data (Y/n)? ').lower() == 'y' :
				if self.tersimpan == False :
					self.simpan_member()
					self.simpan_buku()
					self.simpan_peminjaman()
					self.tersimpan = True
					return self.menu_petugas(pesan=colored('Data berhasil disimpan.', 'green'))
				return self.menu_petugas(pesan=colored('Semua data sudah tersimpan.', 'yellow'))
			return self.menu_petugas()
			
		except Exception as e :
			sys.exit(e)

	def simpan_member(self) -> None :
		for _, member in enumerate(self.app.member.data.tolist(semua=True)) :
			if member.status_data == 'baru' :
				query = 'INSERT INTO pengguna VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'
				data = (
					member.kode,
					member.nama,
					member.email,
					member.password,
					member.nomor_telepon,
					member.alamat,
					'member',
					member.tanggal_dibuat,
				)
				self.app.db.sql(query=query, data=data)
			elif member.status_data == 'ubah' :
				query = 'UPDATE pengguna SET nama = %s, email = %s, nomor_telepon = %s, alamat = %s WHERE kode = %s;'
				data = (
					member.nama,
					member.email,
					member.nomor_telepon,
					member.alamat,
					member.kode,
				)
				self.app.db.sql(query=query, data=data)
			elif member.status_data == 'hapus' :
				query = 'DELETE FROM pengguna WHERE kode = %s;'
				self.app.db.sql(query=query, data=(member.kode,))

		self.app.member.data.tetapkan_sebagai_tersimpan()

	def simpan_buku(self) -> None :
		for _, buku in enumerate(self.app.buku.data.tolist(semua=True)) :
			if buku.status_data == 'baru' :
				query = 'INSERT INTO buku VALUES (%s, %s, %s, %s, %s, %s, %s);'
				data = (
					buku.kode,
					buku.isbn,
					buku.judul,
					buku.penulis,
					buku.genre,
					buku.jumlah_halaman,
					buku.jumlah
				)
				self.app.db.sql(query=query, data=data)
			elif buku.status_data == 'ubah' :
				query = (
					'UPDATE buku SET isbn = %s, judul = %s, penulis = %s, genre = %s, jumlah_halaman = %s, jumlah = %s '
					'WHERE kode = %s;'
				)
				data = (
					buku.isbn,
					buku.judul,
					buku.penulis,
					buku.genre,
					buku.jumlah_halaman,
					buku.jumlah,
					buku.kode
				)
				self.app.db.sql(query=query, data=data)
			elif buku.status_data == 'hapus' :
				query = 'DELETE FROM buku WHERE kode = %s;'
				self.app.db.sql(query=query, data=(buku.kode,))

		self.app.buku.data.tetapkan_sebagai_tersimpan()

	def simpan_peminjaman(self) -> None :
		for _, peminjaman in enumerate(self.app.peminjaman.data.tolist(semua=True)) :
			if peminjaman.status_data == 'baru' :
				query = 'INSERT INTO peminjaman VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'
				data = (
					peminjaman.kode,
					peminjaman.kode_petugas,
					peminjaman.kode_member,
					peminjaman.kode_buku,
					konversi_format(peminjaman.tanggal_mulai, '%d-%m-%Y', '%Y-%m-%d'),
					konversi_format(peminjaman.tanggal_selesai, '%d-%m-%Y', '%Y-%m-%d') if peminjaman.tanggal_selesai else None,
					konversi_format(peminjaman.tenggat, '%d-%m-%Y', '%Y-%m-%d'),
					peminjaman.denda
				)
				self.app.db.sql(query=query, data=data)
			elif peminjaman.status_data == 'ubah' :
				query = (
					'UPDATE peminjaman SET kode_petugas = %s, kode_member = %s, kode_buku = %s, tanggal_mulai = %s, tanggal_selesai = %s, tenggat = %s, denda = %s '
					'WHERE kode = %s;'
				)
				data = (
					peminjaman.kode_petugas,
					peminjaman.kode_member,
					peminjaman.kode_buku,
					konversi_format(peminjaman.tanggal_mulai, '%d-%m-%Y', '%Y-%m-%d'),
					konversi_format(peminjaman.tanggal_selesai, '%d-%m-%Y', '%Y-%m-%d') if peminjaman.tanggal_selesai else None,
					konversi_format(peminjaman.tenggat, '%d-%m-%Y', '%Y-%m-%d'),
					peminjaman.denda,
					peminjaman.kode,
				)
				self.app.db.sql(query=query, data=data)
			elif peminjaman.status_data == 'hapus' :
				query = 'DELETE FROM peminjaman WHERE kode = %s;'
				self.app.db.sql(query=query, data=(peminjaman.kode,))

		self.app.peminjaman.data.tetapkan_sebagai_tersimpan()

	def load_data_dari_database(self) -> None :
		self.load_data_member_dari_database()
		self.load_data_buku_dari_database()
		self.load_data_peminjaman_dari_database()
		self.tersimpan = True

	def load_data_member_dari_database(self) -> None :
		member = self.app.db.sql(query="SELECT * FROM pengguna WHERE role = 'member';", hasil=lambda cursor: cursor.fetchall())
		for _, _member in enumerate(member) :
			member_model = Pengguna()
			member_model.tetapkan_kode(_member['kode'])
			member_model.nama = _member['nama']
			member_model.email = _member['email']
			member_model.nomor_telepon = _member['nomor_telepon']
			member_model.alamat = _member['alamat']
			member_model.role = _member['role']
			member_model.tanggal_dibuat = _member['tanggal_dibuat']
			member_model.status_data = 'lama'

			self.app.member.data.insert(member_model)

	def load_data_buku_dari_database(self) -> None :
		buku = self.app.db.sql(query="SELECT * FROM buku;", hasil=lambda cursor: cursor.fetchall())
		for _, _buku in enumerate(buku) :
			buku_model = Buku()
			buku_model.tetapkan_kode(_buku['kode'])
			buku_model.isbn = _buku['isbn']
			buku_model.judul = _buku['judul']
			buku_model.genre = _buku['genre']
			buku_model.penulis = _buku['penulis']
			buku_model.jumlah_halaman = _buku['jumlah_halaman']
			buku_model.jumlah = _buku['jumlah']
			buku_model.status_data = 'lama'

			self.app.buku.data.insert(buku_model)

	def load_data_peminjaman_dari_database(self) -> None :
		peminjaman = self.app.db.sql(query="SELECT * FROM peminjaman;", hasil=lambda cursor: cursor.fetchall())
		for _, _peminjaman in enumerate(peminjaman) :
			peminjaman_model = Peminjaman()
			peminjaman_model.tetapkan_kode(_peminjaman['kode'])
			peminjaman_model.kode_petugas = _peminjaman['kode_petugas']
			peminjaman_model.kode_member = _peminjaman['kode_member']
			peminjaman_model.kode_buku = _peminjaman['kode_buku']
			peminjaman_model.tanggal_mulai = _peminjaman['tanggal_mulai']
			peminjaman_model.tanggal_selesai = _peminjaman['tanggal_selesai']
			peminjaman_model.tenggat = _peminjaman['tenggat']
			peminjaman_model.denda = _peminjaman['denda']
			peminjaman_model.status_data = 'lama'

			self.app.peminjaman.data.insert(peminjaman_model)