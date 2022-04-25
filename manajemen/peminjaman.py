from datetime import datetime, timedelta
from prettytable import PrettyTable
from data_class import LinkedListOfDict
from helper import bersihkan_console, cek_tanggal_valid, konversi_format
from termcolor import colored

class ManajemenPeminjaman :
	"""
		Manajemen peminjaman.
	"""

	def __init__(self, app) :
		self.app = app
		self.data = LinkedListOfDict(softdelete=True)

	def menu_manajemen_peminjaman(self) :
		try :
			bersihkan_console()

			print(f"Halaman: Petugas > {colored('Peminjaman', 'blue')}")
			print('[1] Tampilkan')
			print('[2] Tambah')
			print('[3] Edit')
			print(colored('[5] Kembali', 'yellow'))
			menu = input('Pilih:\n> ')

			if menu == '1' :
				return self.tampilkan_peminjaman()
			elif menu == '2' :
				return self.tambah_peminjaman()
			elif menu == '3' :
				return self.hapus_peminjaman()
			elif menu == '5' :
				return self.app.role_petugas.menu_petugas()
			else :
				return self.menu_manajemen_peminjaman()

		except KeyboardInterrupt :
			return self.app.role_petugas.menu_petugas()

	def tampilkan_tabel_peminjaman(self, pakai_kode=False) :
		tabel = PrettyTable()
		tabel.title = 'Daftar Peminjaman'
		tabel.field_names = ('Kode' if pakai_kode == False else 'No', 'Petugas', 'Member', 'ISBN', 'Dari', 'Sampai', 'Tenggat', 'Hitungan Denda')

		peminjaman = self.data.tolist(sort=self.urutkan_peminjaman)
		for i in range(len(peminjaman)) :
			petugas = self.app.petugas.data.search(peminjaman[i]['kode_petugas'], 'kode')
			member  = self.app.member.data.search(peminjaman[i]['kode_member'], 'kode')
			buku    = self.app.buku.data.search(peminjaman[i]['kode_buku'], 'kode')

			if peminjaman[i]['tanggal_selesai'] is not None :
				jumlah_telat = datetime.strptime(peminjaman[i]['tanggal_selesai'], '%Y-%m-%d') - datetime.strptime(peminjaman[i]['tenggat'], '%Y-%m-%d')

			tabel.add_row((
				peminjaman[i]['kode'] if pakai_kode else (i + 1),
				petugas['nama'],
				member['nama'],
				buku['isbn'],
				konversi_format(peminjaman[i]['tanggal_mulai']),
				konversi_format(peminjaman[i]['tanggal_selesai']) if peminjaman[i]['tanggal_selesai'] is not None else '-',
				konversi_format(peminjaman[i]['tenggat']),
				jumlah_telat * peminjaman[i]['denda'] if peminjaman[i]['tanggal_selesai'] is not None else '-',
			))

		print(tabel)

	def urutkan_peminjaman(l, r) :
		format_tanggal = '%Y-%m-%d'
		hari_ini = datetime.now().strftime(format_tanggal)
		tenggat_hari1 = datetime.strptime(l['tanggal_selesai'] if l['tanggal_selesai'] is not None else hari_ini, format_tanggal) - datetime.strptime(l['tenggat'], format_tanggal)
		tenggat_hari2 = datetime.strptime(r['tanggal_selesai'] if r['tanggal_selesai'] is not None else hari_ini, format_tanggal) - datetime.strptime(r['tenggat'], format_tanggal)

		return tenggat_hari1 < tenggat_hari2

	def tampilkan_peminjaman(self, pesan=None) :
		try :
			bersihkan_console()
			print(f"Halaman: Petugas > Peminjaman > {colored('Tampilkan Peminjaman', 'blue')}")

			if pesan is not None : print(pesan)
			
			self.tampilkan_tabel_peminjaman(pakai_kode=True)
			input('...')

			return self.menu_manajemen_peminjaman()

		except KeyboardInterrupt :
			return self.menu_manajemen_peminjaman()

	def tambah_peminjaman(self, pesan=None) :
		try :
			bersihkan_console()
			print(f"Halaman: Petugas > Peminjaman > {colored('Tambah Peminjaman', 'blue')}")

			if pesan is not None : print(pesan)

			self.app.member.tampilkan_tabel_member(pakai_kode=True)
			self.app.buku.tampilkan_tabel_buku(pakai_kode=True)
			print()
			kode_member   = input('Kode member              : ')
			kode_buku     = input('Kode buku                : ')
			tanggal_mulai = input('Tanggal mulai (d-m-y)    : ') or datetime.now().strftime('%d-%m-%Y')
			durasi_hari   = input('Durasi hari              : ') or 1
			denda         = input('Nominal denda (Rp10,000) : ') or 10000

			if not kode_member or self.app.member.search(kode_member, 'kode') is None :
				return self.tambah_peminjaman(pesan=colored('Mohon pilih member yang tersedia.', 'red'))
			if not kode_buku or self.app.buku.search(kode_buku, 'kode') is None :
				return self.tambah_peminjaman(pesan=colored('Mohon pilih buku yang tersedia.', 'red'))
			if not cek_tanggal_valid(tanggal_mulai) :
				return self.tambah_peminjaman(pesan=colored('Tanggal mulai tidak valid.', 'red'))
			if not durasi_hari or not durasi_hari.isnumeric() :
				return self.tambah_peminjaman(pesan=colored('Durasi hari tidak valid.', 'red'))
			if not denda or not denda.isnumeric() :
				return self.tambah_peminjaman(pesan=colored('Nominal denda tidak valid.', 'red'))

			tenggat = datetime.datetime.strptime(tanggal_mulai, "%d-%m-%Y")
			tenggat = tenggat + timedelta(days=durasi_hari)

			self.data.insert({
				'kode_member': kode_member,
				'kode_buku': kode_buku,
				'tanggal_mulai': tanggal_mulai,
				'tanggal_selesai': '',
				'tenggat': tenggat,
				'denda': denda
			})
			self.app.role_petugas.tersimpan = False
			
			return self.tampilkan_peminjaman(pesan=colored('Peminjaman berhasil ditambah.', 'green'))
		
		except KeyboardInterrupt :
			return self.menu_manajemen_peminjaman()

	def hapus_peminjaman(self, pesan=None) :
		try :
			bersihkan_console()
			print(f"Halaman: Petugas > Peminjaman > {colored('Hapus Peminjaman', 'blue')}")

			if pesan is not None : print(pesan)

			self.tampilkan_tabel_peminjaman(pakai_kode=True)
			kode_peminjaman = input('Pilih kode peminjaman:\n> ')

			if not kode_peminjaman or self.data.search(kode_peminjaman, 'kode') is None :
				return self.hapus_peminjaman(pesan=colored('Pilih kode peminjaman yang tersedia.', 'red'))

			input(colored('Tekan untuk konfirmasi penghapusan...', 'yellow'))
			self.data.delete(kode_peminjaman, 'kode')
			self.app.role_petugas.tersimpan = False

			return self.tampilkan_peminjaman(pesan=colored('Peminjaman telah dihapus.', 'green'))

		except KeyboardInterrupt :
			return self.menu_manajemen_peminjaman()