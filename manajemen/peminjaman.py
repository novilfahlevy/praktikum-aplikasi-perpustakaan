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

		except KeyboardInterrupt :
			return self.app.role_petugas.menu_petugas()

	def tampilkan_tabel_peminjaman(self, pakai_kode=False, belum_dikembalikan=False) :
		tabel = PrettyTable()
		tabel.title = 'Daftar Peminjaman'
		tabel.field_names = ('Kode' if pakai_kode else 'No', 'Petugas', 'Member', 'ISBN', 'Dari', 'Sampai', 'Tenggat', 'Hitungan Denda')

		peminjaman = self.data.tolist(sort=lambda l, r: self.urutkan_peminjaman(l, r))

		if belum_dikembalikan == True :
			peminjaman = list(filter(lambda p: not bool(p['tanggal_selesai']), peminjaman))

		for i in range(len(peminjaman)) :
			petugas = self.app.petugas.data.search(peminjaman[i]['kode_petugas'], 'kode')
			member  = self.app.member.data.search(peminjaman[i]['kode_member'], 'kode')
			buku    = self.app.buku.data.search(peminjaman[i]['kode_buku'], 'kode')

			if peminjaman[i]['tanggal_selesai'] :
				jumlah_telat = (datetime.strptime(str(peminjaman[i]['tanggal_selesai']), '%Y-%m-%d') - datetime.strptime(str(peminjaman[i]['tenggat']), '%Y-%m-%d')).days

			tabel.add_row((
				peminjaman[i]['kode'] if pakai_kode else (i + 1),
				petugas['nama'],
				member['nama'],
				buku['isbn'],
				konversi_format(peminjaman[i]['tanggal_mulai'], '%Y-%m-%d', '%d-%m-%Y'),
				konversi_format(peminjaman[i]['tanggal_selesai'], '%Y-%m-%d', '%d-%m-%Y') if peminjaman[i]['tanggal_selesai'] else '-',
				konversi_format(peminjaman[i]['tenggat'], '%Y-%m-%d', '%d-%m-%Y'),
				jumlah_telat * peminjaman[i]['denda'] if peminjaman[i]['tanggal_selesai'] and jumlah_telat > 0 else '-',
			))

		print(tabel)

	def urutkan_peminjaman(self, l, r) :
		format_tanggal = '%Y-%m-%d'
		hari_ini = datetime.now().strftime(format_tanggal)

		tenggat_hari1 = str(l['tanggal_selesai']) if l['tanggal_selesai'] else hari_ini
		tenggat_hari1 = datetime.strptime(str(l['tenggat']), format_tanggal) - datetime.strptime(tenggat_hari1, format_tanggal)

		tenggat_hari2 = str(r['tanggal_selesai'] if r['tanggal_selesai'] else hari_ini)
		tenggat_hari2 = datetime.strptime(str(r['tenggat']), format_tanggal) - datetime.strptime(tenggat_hari2, format_tanggal)

		return tenggat_hari1.days < tenggat_hari2.days

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

			member = self.app.member.data.search(kode_member, 'kode')
			buku = self.app.buku.data.search(kode_buku, 'kode')
			if not kode_member or member is None :
				return self.tambah_peminjaman(pesan=colored('Mohon pilih member yang tersedia.', 'red'))
			if not kode_buku or buku is None :
				return self.tambah_peminjaman(pesan=colored('Mohon pilih buku yang tersedia.', 'red'))
			if buku['jumlah'] <= 0 :
				return self.tambah_peminjaman(pesan=colored('Buku tidak tersedia.', 'red'))
			if not cek_tanggal_valid(tanggal_mulai) :
				return self.tambah_peminjaman(pesan=colored('Tanggal mulai tidak valid.', 'red'))
			if not durasi_hari or not str(durasi_hari).isnumeric() :
				return self.tambah_peminjaman(pesan=colored('Durasi hari tidak valid.', 'red'))
			if not denda or not str(denda).isnumeric() :
				return self.tambah_peminjaman(pesan=colored('Nominal denda tidak valid.', 'red'))

			tenggat = datetime.strptime(tanggal_mulai, "%d-%m-%Y")
			tenggat = konversi_format(tenggat + timedelta(days=int(durasi_hari)), '%Y-%m-%d %H:%M:%S', '%Y-%m-%d')

			self.data.insert({
				'kode_member': kode_member,
				'kode_petugas': self.app.auth.session['kode'],
				'kode_buku': kode_buku,
				'tanggal_mulai': tanggal_mulai,
				'tanggal_selesai': '',
				'tenggat': tenggat,
				'denda': denda
			})
			self.pinjam_buku(kode_buku)
			self.app.role_petugas.tersimpan = False
			
			return self.tampilkan_peminjaman(pesan=colored('Peminjaman berhasil ditambah.', 'green'))
		
		except KeyboardInterrupt :
			return self.menu_manajemen_peminjaman()

	def pinjam_buku(self, kode_buku) :
		buku_lama = self.app.buku.data.search(kode_buku, 'kode')
		if buku_lama is not None :
			self.app.buku.data.update(
				{ 'jumlah': buku_lama['jumlah'] - 1 },
				buku_lama['isbn'],
				'isbn'
			)
	
	def kembalikan_buku(self, kode_buku) :
		buku_lama = self.app.buku.data.search(kode_buku, 'kode')
		if buku_lama is not None :
			self.app.buku.data.update(
				{ 'jumlah': buku_lama['jumlah'] + 1 },
				buku_lama['isbn'],
				'isbn'
			)

	def hapus_peminjaman(self, pesan=None) :
		try :
			bersihkan_console()
			print(f"Halaman: Petugas > Peminjaman > {colored('Hapus Peminjaman', 'blue')}")

			if pesan is not None : print(pesan)

			self.tampilkan_tabel_peminjaman(pakai_kode=True)
			kode_peminjaman = input('Pilih kode peminjaman:\n> ')
			peminjaman = self.data.search(kode_peminjaman, 'kode')

			if not kode_peminjaman or peminjaman is None :
				return self.hapus_peminjaman(pesan=colored('Pilih kode peminjaman yang tersedia.', 'red'))

			input(colored('Tekan untuk konfirmasi penghapusan...', 'yellow'))
			self.data.delete(kode_peminjaman, 'kode')

			buku = self.app.buku.data.search(peminjaman['kode_buku'], 'kode')
			self.kembalikan_buku(buku['kode'])
			self.app.role_petugas.tersimpan = False

			return self.tampilkan_peminjaman(pesan=colored('Peminjaman telah dihapus.', 'green'))

		except KeyboardInterrupt :
			return self.menu_manajemen_peminjaman()
	
	def pengembalian(self, pesan=None) :
		try :
			bersihkan_console()
			print(f"Halaman: Petugas > Peminjaman > {colored('Pengembalian', 'blue')}")

			if pesan is not None : print(pesan)

			self.tampilkan_tabel_peminjaman(pakai_kode=True, belum_dikembalikan=True)
			kode_peminjaman = input('Pilih kode peminjaman:\n> ')
			peminjaman = self.data.search(kode_peminjaman, 'kode')

			if not kode_peminjaman or peminjaman is None :
				return self.pengembalian(pesan=colored('Pilih kode peminjaman yang tersedia.', 'red'))

			input(colored('Tekan untuk konfirmasi pengembalian...', 'yellow'))
			self.data.update(
				{ 'tanggal_selesai': datetime.now().strftime('%Y-%m-%d') },
				kode_peminjaman,
				'kode'
			)

			buku = self.app.buku.data.search(peminjaman['kode_buku'], 'kode')
			self.kembalikan_buku(buku['kode'])
			self.app.role_petugas.tersimpan = False

			return self.tampilkan_peminjaman(pesan=colored('Buku telah dikembalikan.', 'green'))

		except KeyboardInterrupt :
			return self.menu_manajemen_peminjaman()