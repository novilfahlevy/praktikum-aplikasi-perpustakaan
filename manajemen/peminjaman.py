from datetime import datetime, timedelta
from prettytable import PrettyTable
from helper import bersihkan_console, cek_tanggal_valid, currency, konversi_format
from termcolor import colored
from asd.linked_list import LinkedList
from asd.binary_search import binary_search

from manajemen.manajemen import Manajemen
from model.peminjaman import Peminjaman

class ManajemenPeminjaman(Manajemen) :
	"""
		Manajemen peminjaman.
	"""

	def __init__(self, app) :
		self.app = app
		self.data = LinkedList()

	def menu_manajemen_peminjaman(self) :
		try :
			bersihkan_console()

			print(f"Halaman: Petugas > {colored('Peminjaman', 'blue')}")
			print('[1] Tampilkan')
			print('[2] Tambah')
			print('[3] Hapus')
			print('[4] Pengembalian')
			print(colored('[5] Kembali', 'yellow'))
			menu = input('Pilih:\n> ')

			if menu == '1' :
				return self.tampilkan_peminjaman()
			elif menu == '2' :
				return self.tambah_peminjaman()
			elif menu == '3' :
				return self.hapus_peminjaman()
			elif menu == '4' :
				return self.pengembalian()
			elif menu == '5' :
				return self.app.role_petugas.menu_petugas()
			else :
				return self.menu_manajemen_peminjaman()

		except KeyboardInterrupt or EOFError :
			return self.app.role_petugas.menu_petugas()

	def tampilkan_tabel_peminjaman(self, berhalaman=True, judul_halaman=None, belum_dikembalikan=False) :
		tabel = PrettyTable()
		tabel.judul_halaman = 'Daftar Peminjaman'
		tabel.field_names = ('No', 'Kode', 'Petugas', 'Member', 'ISBN', 'Dari', 'Sampai', 'Tenggat', 'Nominal Denda')

		peminjaman = self.data.tolist(sort=lambda l, r: self.urutkan_peminjaman(l, r))

		if belum_dikembalikan == True :
			peminjaman = list(filter(lambda p: not bool(p.tanggal_selesai), peminjaman))

		if berhalaman :
			self.tampilkan_tabel_berhalaman(
				queue=self.data.toqueue(),
				tabel=tabel,
				data_format=lambda data: self.format_data_tabel(data),
				judul_halaman=judul_halaman
			)
		else :
			for i in range(len(peminjaman)) :
				petugas = self.app.petugas.data.cari(peminjaman[i].kode_petugas, 'kode')
				member  = self.app.member.data.cari(peminjaman[i].kode_member, 'kode')
				buku    = self.app.buku.data.cari(peminjaman[i].kode_buku, 'kode')

				tabel.add_row((
					(i + 1),
					peminjaman[i].kode,
					petugas.nama,
					member.nama,
					buku.isbn,
					konversi_format(peminjaman[i].tanggal_mulai, '%Y-%m-%d', '%d-%m-%Y'),
					konversi_format(peminjaman[i].tanggal_selesai, '%Y-%m-%d', '%d-%m-%Y') if peminjaman[i].tanggal_selesai else '-',
					konversi_format(peminjaman[i].tenggat, '%Y-%m-%d', '%d-%m-%Y'),
					peminjaman.jumlah_denda(konversi=True),
				))

			print(tabel)

	def format_data_tabel(self, data) :
		petugas = self.app.petugas.data.cari(data.kode_petugas, 'kode')
		member  = self.app.member.data.cari(data.kode_member, 'kode')
		buku    = self.app.buku.data.cari(data.kode_buku, 'kode')
		
		return (
			data.kode,
			petugas.nama,
			member.nama,
			buku.isbn,
			konversi_format(data.tanggal_mulai, '%Y-%m-%d', '%d-%m-%Y'),
			konversi_format(data.tanggal_selesai, '%Y-%m-%d', '%d-%m-%Y') if data.tanggal_selesai else '-',
			konversi_format(data.tenggat, '%Y-%m-%d', '%d-%m-%Y'),
			data.jumlah_denda(konversi=True),
		)

	def urutkan_peminjaman(self, l, r) :
		format_tanggal = '%Y-%m-%d'
		hari_ini = datetime.now().strftime(format_tanggal)

		tenggat_hari1 = str(l.tanggal_selesai) if l.tanggal_selesai else hari_ini
		tenggat_hari1 = datetime.strptime(str(l.tenggat), format_tanggal) - datetime.strptime(tenggat_hari1, format_tanggal)

		tenggat_hari2 = str(r.tanggal_selesai if r.tanggal_selesai else hari_ini)
		tenggat_hari2 = datetime.strptime(str(r.tenggat), format_tanggal) - datetime.strptime(tenggat_hari2, format_tanggal)

		return tenggat_hari1.days < tenggat_hari2.days

	def tampilkan_peminjaman(self, pesan=None) :
		try :
			bersihkan_console()

			judul_halaman = f"Halaman: Petugas > Peminjaman > {colored('Tampilkan Peminjaman', 'blue')}"
			print(judul_halaman)

			if pesan is not None : print(pesan)
			
			self.tampilkan_tabel_peminjaman(berhalaman=True, judul_halaman=judul_halaman)

			return self.menu_manajemen_peminjaman()

		except KeyboardInterrupt or EOFError :
			return self.menu_manajemen_peminjaman()

	def tambah_peminjaman(self, pesan=None) :
		try :
			bersihkan_console()
			print(f"Halaman: Petugas > Peminjaman > {colored('Tambah Peminjaman', 'blue')}")

			if pesan is not None : print(pesan)

			self.app.member.tampilkan_tabel_member()
			self.app.buku.tampilkan_tabel_buku()
			print()
			kode_member   = input('Kode member              : ')
			kode_buku     = input('Kode buku                : ')
			tanggal_mulai = input('Tanggal mulai (d-m-y)    : ') or datetime.now().strftime('%d-%m-%Y')
			durasi_hari   = input('Durasi hari              : ') or 1
			denda         = input('Nominal denda (Rp10,000) : ') or 10000

			member = self.app.member.data.cari(kode_member, 'kode')
			buku = self.app.buku.data.cari(kode_buku, 'kode')
			if not kode_member or member is None :
				return self.tambah_peminjaman(pesan=colored('Mohon pilih member yang tersedia.', 'red'))
			if not kode_buku or buku is None :
				return self.tambah_peminjaman(pesan=colored('Mohon pilih buku yang tersedia.', 'red'))
			if buku.jumlah <= 0 :
				return self.tambah_peminjaman(pesan=colored('Buku tidak tersedia.', 'red'))
			if not cek_tanggal_valid(tanggal_mulai) :
				return self.tambah_peminjaman(pesan=colored('Tanggal mulai tidak valid.', 'red'))
			if not durasi_hari or not str(durasi_hari).isnumeric() :
				return self.tambah_peminjaman(pesan=colored('Durasi hari tidak valid.', 'red'))
			if not denda or not str(denda).isnumeric() :
				return self.tambah_peminjaman(pesan=colored('Nominal denda tidak valid.', 'red'))

			peminjaman = Peminjaman()
			peminjaman.tetapkan_kode()
			peminjaman.kode_member = kode_member
			peminjaman.kode_petugas = self.app.auth.session['kode']
			peminjaman.kode_buku = kode_buku
			peminjaman.tanggal_mulai = tanggal_mulai
			peminjaman.tanggal_selesai = ''
			peminjaman.denda = denda
			peminjaman.tetapkan_tenggat(durasi_hari)

			buku = self.app.buku.data.cari(kode_buku, 'kode')
			buku.pinjam()

			self.data.insert(peminjaman)
			self.app.role_petugas.tersimpan = False
			
			return self.tampilkan_peminjaman(pesan=colored('Peminjaman berhasil ditambah.', 'green'))
		
		except KeyboardInterrupt or EOFError :
			return self.menu_manajemen_peminjaman()

	def hapus_peminjaman(self, pesan=None) :
		try :
			bersihkan_console()

			judul_halaman = f"Halaman: Petugas > Peminjaman > {colored('Hapus Peminjaman', 'blue')}"
			print(judul_halaman)

			if pesan is not None : print(pesan)

			self.tampilkan_tabel_peminjaman(berhalaman=True, judul_halaman=judul_halaman)
			kode_peminjaman = input('\nPilih kode peminjaman:\n> ')
			peminjaman = self.data.cari(kode_peminjaman, 'kode')

			if not kode_peminjaman or peminjaman is None :
				return self.hapus_peminjaman(pesan=colored('Pilih kode peminjaman yang tersedia.', 'red'))

			input(colored('Tekan untuk konfirmasi penghapusan...', 'yellow'))
			self.data.delete(kode_peminjaman, 'kode')

			buku = self.app.buku.data.cari(peminjaman.kode_buku, 'kode')
			buku.kembalikan()
			
			self.app.role_petugas.tersimpan = False

			return self.tampilkan_peminjaman(pesan=colored('Peminjaman telah dihapus.', 'green'))

		except KeyboardInterrupt or EOFError :
			return self.menu_manajemen_peminjaman()
	
	def pengembalian(self, pesan=None) :
		try :
			bersihkan_console()

			judul_halaman = f"Halaman: Petugas > Peminjaman > {colored('Pengembalian', 'blue')}"
			print(judul_halaman)

			if pesan is not None : print(pesan)

			self.tampilkan_tabel_peminjaman(belum_dikembalikan=True, berhalaman=True, judul_halaman=judul_halaman)
			kode_peminjaman = input('\nPilih kode peminjaman:\n> ')
			peminjaman = self.data.tolist(sort=lambda l, r: l.kode < r.kode)
			peminjaman = binary_search(peminjaman, kode_peminjaman, 'kode')

			if not kode_peminjaman or peminjaman is None :
				return self.pengembalian(pesan=colored('Pilih kode peminjaman yang tersedia.', 'red'))

			input(colored('Tekan untuk konfirmasi pengembalian...', 'yellow'))
			self.data.update(
				{ 'tanggal_selesai': datetime.now().strftime('%Y-%m-%d') },
				kode_peminjaman,
				'kode'
			)

			buku = self.app.buku.data.cari(peminjaman.kode_buku, 'kode')
			buku.kembalikan()

			self.app.role_petugas.tersimpan = False

			return self.tampilkan_peminjaman(pesan=colored('Buku telah dikembalikan.', 'green'))

		except KeyboardInterrupt or EOFError :
			return self.menu_manajemen_peminjaman()