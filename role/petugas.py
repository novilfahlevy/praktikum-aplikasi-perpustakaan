import sys
from database import sql
from helper import bersihkan_console, konversi_format
from termcolor import colored

from role.user import BaseUser

class RolePetugas(BaseUser) :
	"""
		Role petugas.
	"""

	def __init__(self, app) :
		self.app = app
		self.tersimpan = True

		self.ambil_database()

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

	def simpan_member(self) :
		member = self.app.member.data
		member_list = member.tolist(with_trashed=True)
		for i in range(len(member_list)) :
			member_data = member_list[i]
			if member_data['status_data'] == 'baru' :
				query = 'INSERT INTO pengguna VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'
				data = (
					member_data['kode'],
					member_data['nama'],
					member_data['email'],
					member_data['password'],
					member_data['nomor_telepon'],
					member_data['alamat'],
					'member',
					member_data['tanggal_dibuat'],
				)
				sql(query=query, data=data)
			elif member_data['status_data'] == 'hapus' :
				query = 'DELETE FROM pengguna WHERE kode = %s;'
				sql(query=query, data=(member_data['kode'],))

		self.app.member.data.tetapkan_sebagai_tersimpan()

	def simpan_buku(self) :
		buku = self.app.buku.data
		buku_list = buku.tolist(with_trashed=True)
		for i in range(len(buku_list)) :
			buku_data = buku_list[i]
			if buku_data['status_data'] == 'baru' :
				query = 'INSERT INTO buku VALUES (%s, %s, %s, %s, %s, %s, %s);'
				data = (
					buku_data['kode'],
					buku_data['isbn'],
					buku_data['judul'],
					buku_data['penulis'],
					buku_data['genre'],
					buku_data['jumlah_halaman'],
					buku_data['jumlah']
				)
				sql(query=query, data=data)
			elif buku_data['status_data'] == 'ubah' :
				query = (
					'UPDATE buku SET isbn = %s, judul = %s, penulis = %s, genre = %s, jumlah_halaman = %s, jumlah = %s '
					'WHERE kode = %s;'
				)
				data = (
					buku_data['isbn'],
					buku_data['judul'],
					buku_data['penulis'],
					buku_data['genre'],
					buku_data['jumlah_halaman'],
					buku_data['jumlah'],
					buku_data['kode']
				)
				sql(query=query, data=data)
			elif buku_data['status_data'] == 'hapus' :
				query = 'DELETE FROM buku WHERE kode = %s;'
				sql(query=query, data=(buku_data['kode'],))

		self.app.buku.data.tetapkan_sebagai_tersimpan()

	def simpan_peminjaman(self) :
		peminjaman = self.app.peminjaman.data
		peminjaman_list = peminjaman.tolist(with_trashed=True)
		for i in range(len(peminjaman_list)) :
			peminjaman_data = peminjaman_list[i]
			if peminjaman_data['status_data'] == 'baru' :
				query = 'INSERT INTO peminjaman VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'
				data = (
					peminjaman_data['kode'],
					peminjaman_data['kode_petugas'],
					peminjaman_data['kode_member'],
					peminjaman_data['kode_buku'],
					konversi_format(peminjaman_data['tanggal_mulai'], '%d-%m-%Y', '%Y-%m-%d'),
					konversi_format(peminjaman_data['tanggal_selesai'], '%d-%m-%Y', '%Y-%m-%d') if peminjaman_data['tanggal_selesai'] else None,
					konversi_format(peminjaman_data['tenggat'], '%d-%m-%Y', '%Y-%m-%d'),
					peminjaman_data['denda']
				)
				sql(query=query, data=data)
			elif peminjaman_data['status_data'] == 'ubah' :
				query = (
					'UPDATE peminjaman SET kode_petugas = %s, kode_member = %s, kode_buku = %s, tanggal_mulai = %s, tanggal_selesai = %s, tenggat = %s, denda = %s '
					'WHERE kode = %s;'
				)
				data = (
					peminjaman_data['kode_petugas'],
					peminjaman_data['kode_member'],
					peminjaman_data['kode_buku'],
					konversi_format(peminjaman_data['tanggal_mulai'], '%d-%m-%Y', '%Y-%m-%d'),
					konversi_format(peminjaman_data['tanggal_selesai'], '%d-%m-%Y', '%Y-%m-%d') if peminjaman_data['tanggal_selesai'] else None,
					konversi_format(peminjaman_data['tenggat'], '%d-%m-%Y', '%Y-%m-%d'),
					peminjaman_data['denda'],
					peminjaman_data['kode'],
				)
				sql(query=query, data=data)
			elif peminjaman_data['status_data'] == 'hapus' :
				query = 'DELETE FROM peminjaman WHERE kode = %s;'
				sql(query=query, data=(peminjaman_data['kode'],))

		self.app.peminjaman.data.tetapkan_sebagai_tersimpan()

	def ambil_database(self) :
		member = sql(query="SELECT * FROM pengguna WHERE role = 'member';", hasil=lambda cursor: cursor.fetchall())
		buku = sql(query="SELECT * FROM buku;", hasil=lambda cursor: cursor.fetchall())
		peminjaman = sql(query="SELECT * FROM peminjaman;", hasil=lambda cursor: cursor.fetchall())

		self.ambil(self.app.member, member)
		self.ambil(self.app.buku, buku)
		self.ambil(self.app.peminjaman, peminjaman)

		self.tersimpan = True