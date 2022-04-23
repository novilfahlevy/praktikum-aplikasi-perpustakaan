from datetime import datetime
from helper import bersihkan_console, hash_password, LinkedList
from termcolor import colored
from auth import logout
from database import koneksi, sql
from prettytable import PrettyTable
import re

def menu_admin() :
	try :
		bersihkan_console()

		print(colored('Admin', 'blue'))
		print('[1] Petugas')
		print('[2] Penerbit')
		print('[3] Pengadaan')
		print(colored('[4] Keluar', 'yellow'))
		menu = input('Pilih:\n> ')

		if menu == '1' :
			return Petugas.menu_manajemen_petugas()
		elif menu == '2' :
			return Penerbit.menu_manajemen_penerbit()
		elif menu == '3' :
			# return Pengadaan.menu_manajemen_pengadaan()
			print('Pengadaan')
		elif menu == '4' :
			return logout()
		else :
			return menu_admin()

	except KeyboardInterrupt :
		return menu_admin()

class Petugas :
	"""
		MANAJEMEN PETUGAS
	"""

	def menu_manajemen_petugas() :
		try :
			bersihkan_console()

			print(f"Admin > {colored('Manajemen Petugas', 'blue')}")
			print('[1] Tampilkan')
			print('[2] Tambah')
			print('[3] Hapus')
			print(colored('[4] Kembali', 'yellow'))
			menu = input('Pilih:\n> ')

			if menu == '1' :
				return Petugas.tampilkan_petugas()
			elif menu == '2' :
				return Petugas.tambah_petugas()
			elif menu == '3' :
				return Petugas.hapus_petugas()
			elif menu == '4' :
				return menu_admin()
			else :
				return Petugas.menu_manajemen_petugas()

		except KeyboardInterrupt :
			return menu_admin()

	def menu_manajemen_petugas() :
		try :
			bersihkan_console()

			print(f"Admin > {colored('Manajemen Petugas', 'blue')}")
			print('[1] Tampilkan')
			print('[2] Tambah')
			print('[3] Hapus')
			print(colored('[4] Kembali', 'yellow'))
			menu = input('Pilih:\n> ')

			if menu == '1' :
				return Petugas.tampilkan_petugas()
			elif menu == '2' :
				return Petugas.tambah_petugas()
			elif menu == '3' :
				return Petugas.hapus_petugas()
			elif menu == '4' :
				return menu_admin()
			else :
				return Petugas.menu_manajemen_petugas()

		except KeyboardInterrupt :
			return menu_admin()

	def tampilkan_tabel_petugas(pakai_id=False) :
		petugas = sql(
			query='SELECT * FROM pengguna WHERE role = %s',
			data=('petugas',),
			hasil=lambda cursor: cursor.fetchall()
		)

		tabel = PrettyTable()
		tabel.title = 'Data Petugas'
		tabel.field_names = ('ID' if pakai_id else 'No.', 'Nama', 'Email', 'Nomor Telepon', 'Alamat')
		
		for i in range(len(petugas)) :
			tabel.add_row((
				petugas[i]['id_pengguna'] if pakai_id else (i + 1),
				petugas[i]['nama'],
				petugas[i]['email'],
				petugas[i]['nomor_telepon'],
				petugas[i]['alamat']
			))

		print(tabel)

	def tampilkan_petugas(pesan=None) :
		try :
			bersihkan_console()
			print(f"Admin > Manajemen Petugas > {colored('Tampilkan Petugas', 'blue')}")

			if pesan : print(pesan)

			Petugas.tampilkan_tabel_petugas()
			input('...')

			return Petugas.menu_manajemen_petugas()
			
		except KeyboardInterrupt :
			return Petugas.menu_manajemen_petugas()

	def tambah_petugas(pesan=None) :
		try :
			bersihkan_console()
			print(f"Admin > Manajemen Petugas > {colored('Tambah Petugas', 'blue')}")

			if pesan : print(pesan) # pesan tambahan, opsional
			
			# input data petugas
			nama          = input('Nama             : ')
			email         = input('Email            : ')
			password      = input('Password (12345) : ') or '12345'
			nomor_telepon = input('Nomor Telepon    : ')
			alamat        = input('Alamat           : ')
			role          = 'petugas'

			# validasi input
			aturan_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
			if not nama : return Petugas.tambah_petugas(colored('Nama tidak boleh kosong.', 'red'))
			if not email : return Petugas.tambah_petugas(colored('Email tidak boleh kosong.', 'red'))
			if not re.fullmatch(aturan_email, email) : return Petugas.tambah_petugas(colored('Email tidak valid.', 'red'))
			if not nomor_telepon : return Petugas.tambah_petugas(colored('Nomor telepon tidak boleh kosong.', 'red'))
			if not nomor_telepon.isnumeric() : return Petugas.tambah_petugas(colored('Nomor telepon tidak valid.', 'red'))
			if not alamat : return Petugas.tambah_petugas(colored('Alamat tidak boleh kosong.', 'red'))

			bersihkan_console()
			print(f"Admin > Manajemen Petugas > {colored('Tambah Petugas', 'blue')}")

			# review dan konfirmasi kembali data petugas
			tabel_review = PrettyTable()
			tabel_review.title = 'Konfirmasi Data Petugas'
			tabel_review.field_names = ('Data', 'Input')
			tabel_review.align = 'l'
			tabel_review.add_rows((
				('Nama         ', nama),
				('Email        ', email),
				('Password     ', password),
				('Nomor Telepon', nomor_telepon),
				('Alamat       ', alamat),
			))

			print(tabel_review)
			input('Tekan untuk konfirmasi...')
			print('Loading...')

			berhasil_menambah = sql(
				query='INSERT INTO pengguna VALUES (null, %s, %s, %s, %s, %s, %s, now())',
				data=(nama, email, hash_password(password), nomor_telepon, alamat, role,),
				hasil=lambda cursor: cursor.rowcount
			)

			if berhasil_menambah :
				return Petugas.tampilkan_petugas(pesan=colored('Berhasil menambah petugas.', 'green'))

			# jika gagal menyimpan data
			return Petugas.tambah_petugas(pesan=colored('Terjadi kesalahan, silakan coba lagi.', 'red'))

		except KeyboardInterrupt :
			return Petugas.menu_manajemen_petugas()

	def cek_petugas(id_petugas) :
		return sql(
			query='SELECT COUNT(id_pengguna) AS hasil FROM pengguna WHERE id_pengguna = %s AND role = %s',
			data=(id_petugas, 'petugas'),
			hasil=lambda cursor: cursor.fetchone()['hasil']
		)

	def hapus_petugas(pesan=None) :
		try :
			bersihkan_console()
			print(f"Admin > Manajemen Petugas > {colored('Hapus Petugas', 'blue')}")

			if pesan : print(pesan) # pesan tambahan, opsional

			Petugas.tampilkan_tabel_petugas(pakai_id=True)
			id_petugas = input('Pilih ID:\n> ')

			if id_petugas :
				if Petugas.cek_petugas(id_petugas) :
					# konfirmasi penghapusan
					input(colored('Tekan untuk mengonfirmasi penghapusan...', 'yellow'))
					print('Loading...')

					berhasil_menghapus = sql(
						query='DELETE FROM pengguna WHERE id_pengguna = %s',
						data=(id_petugas,),
						hasil=lambda cursor: cursor.rowcount
					)

					if berhasil_menghapus :
						return Petugas.tampilkan_petugas(pesan=colored('Petugas berhasil dihapus.', 'green'))

					# jika gagal menghapus data
					return Petugas.tampilkan_petugas(pesan=colored('Terjadi kesalahan, silakan coba lagi.', 'red'))

				else :
					return Petugas.hapus_petugas(pesan=colored('ID petugas tidak ditemukan.', 'red'))
			
			return Petugas.hapus_petugas(pesan=colored('Mohon pilih ID petugas.', 'red'))

		except KeyboardInterrupt :
			return Petugas.menu_manajemen_petugas()

class Penerbit :
	"""
		MANAJEMEN PENERBIT
	"""
	
	def menu_manajemen_penerbit() :
		try :
			bersihkan_console()

			print(f"Admin > {colored('Manajemen Penerbit', 'blue')}")
			print('[1] Tampilkan')
			print('[2] Tambah')
			print('[3] Edit')
			print('[4] Hapus')
			print(colored('[5] Kembali', 'yellow'))
			menu = input('Pilih:\n> ')

			if menu == '1' :
				return Penerbit.tampilkan_penerbit()
			elif menu == '2' :
				return Penerbit.tambah_penerbit()
			elif menu == '3' :
				return Penerbit.edit_penerbit()
			elif menu == '4' :
				return Penerbit.hapus_penerbit()
			elif menu == '5' :
				return menu_admin()
			else :
				return Penerbit.menu_manajemen_penerbit()

		except KeyboardInterrupt :
			return menu_admin()

	def tampilkan_tabel_penerbit(pakai_id=False) :
		penerbit = sql(
			query='SELECT * FROM penerbit',
			hasil=lambda cursor: cursor.fetchall()
		)

		tabel = PrettyTable()
		tabel.title = 'Data Penerbit'
		tabel.field_names = ('ID' if pakai_id else 'No.', 'Nama', 'Email', 'Nomor Telepon', 'Alamat')
		
		for i in range(len(penerbit)) :
			tabel.add_row((
				penerbit[i]['id_penerbit'] if pakai_id else (i + 1),
				penerbit[i]['nama'],
				penerbit[i]['email'],
				penerbit[i]['nomor_telepon'],
				penerbit[i]['alamat']
			))

		print(tabel)

	def tampilkan_penerbit(pesan=None) :
		try :
			bersihkan_console()
			print(f"Admin > Manajemen Penerbit > {colored('Tampilkan Penerbit', 'blue')}")

			if pesan : print(pesan)

			Penerbit.tampilkan_tabel_penerbit()
			input('...')

			return Penerbit.menu_manajemen_penerbit()
			
		except KeyboardInterrupt :
			return Penerbit.menu_manajemen_penerbit()

	def tambah_penerbit(pesan=None) :
		try :
			bersihkan_console()
			print(f"Admin > Manajemen Penerbit > {colored('Tambah Penerbit', 'blue')}")

			if pesan : print(pesan) # pesan tambahan, opsional
			
			# input data penerbit
			nama          = input('Nama          : ')
			email         = input('Email         : ')
			nomor_telepon = input('Nomor Telepon : ')
			alamat        = input('Alamat        : ')

			# validasi input
			aturan_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
			if not nama : return Penerbit.tambah_penerbit(colored('Nama tidak boleh kosong.', 'red'))
			if not email : return Penerbit.tambah_penerbit(colored('Email tidak boleh kosong.', 'red'))
			if not re.fullmatch(aturan_email, email) : return Penerbit.tambah_penerbit(colored('Email tidak valid.', 'red'))
			if not nomor_telepon : return Penerbit.tambah_penerbit(colored('Nomor telepon tidak boleh kosong.', 'red'))
			if not nomor_telepon.isnumeric() : return Penerbit.tambah_penerbit(colored('Nomor telepon tidak valid.', 'red'))
			if not alamat : return Penerbit.tambah_penerbit(colored('Alamat tidak boleh kosong.', 'red'))

			bersihkan_console()
			print(f"Admin > Manajemen Penerbit > {colored('Tambah Penerbit', 'blue')}")

			# review dan konfirmasi kembali data penerbit
			tabel_review = PrettyTable()
			tabel_review.title = 'Konfirmasi Data Penerbit'
			tabel_review.field_names = ('Data', 'Input')
			tabel_review.align = 'l'
			tabel_review.add_rows((
				('Nama         ', nama),
				('Email        ', email),
				('Nomor Telepon', nomor_telepon),
				('Alamat       ', alamat),
			))

			print(tabel_review)
			input('Tekan untuk konfirmasi...')
			print('Loading...')
			
			berhasil_menambah = sql(
				query='INSERT INTO penerbit VALUES (null, %s, %s, %s, %s)',
				data=(nama, email, nomor_telepon, alamat),
				hasil=lambda cursor: cursor.rowcount
			)

			if berhasil_menambah :
				return Penerbit.tampilkan_penerbit(pesan=colored('Berhasil menambah penerbit.', 'green'))

			# jika gagal menyimpan data
			return Penerbit.tambah_penerbit(pesan=colored('Terjadi kesalahan, silakan coba lagi.', 'red'))

		except KeyboardInterrupt :
			return Penerbit.menu_manajemen_penerbit()

	def edit_penerbit(pesan=None) :
		try :
			bersihkan_console()
			print(f"Admin > Manajemen Penerbit > {colored('Edit Penerbit', 'blue')}")

			if pesan : print(pesan) # pesan tambahan, opsional

			Penerbit.tampilkan_tabel_penerbit(pakai_id=True)
			id_penerbit = input('Pilih ID:\n> ')

			if id_penerbit :
				penerbit = sql(
					query='SELECT * FROM penerbit WHERE id_penerbit = %s',
					data=(id_penerbit,),
					hasil=lambda cursor: cursor.fetchone()
				)
				if penerbit :
					# input data penerbit
					nama          = input(f'Nama ({penerbit["nama"]}):\n> ') or penerbit["nama"]
					email         = input(f'Email ({penerbit["email"]}):\n> ') or penerbit["email"]
					nomor_telepon = input(f'Nomor Telepon ({penerbit["nomor_telepon"]}):\n> ') or penerbit["nomor_telepon"]
					alamat        = input(f'Alamat ({penerbit["alamat"]}):\n> ') or penerbit["alamat"]

					# validasi input
					aturan_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
					if not nama : return Penerbit.edit_penerbit(colored('Nama tidak boleh kosong.', 'red'))
					if not email : return Penerbit.edit_penerbit(colored('Email tidak boleh kosong.', 'red'))
					if not re.fullmatch(aturan_email, email) : return Penerbit.edit_penerbit(colored('Email tidak valid.', 'red'))
					if not nomor_telepon : return Penerbit.edit_penerbit(colored('Nomor telepon tidak boleh kosong.', 'red'))
					if not nomor_telepon.isnumeric() : return Penerbit.edit_penerbit(colored('Nomor telepon tidak valid.', 'red'))
					if not alamat : return Penerbit.edit_penerbit(colored('Alamat tidak boleh kosong.', 'red'))

					bersihkan_console()
					print(f"Admin > Manajemen Penerbit > {colored('Edit Penerbit', 'blue')}")

					# review dan konfirmasi kembali data penerbit
					tabel_review = PrettyTable()
					tabel_review.title = 'Konfirmasi Data Penerbit'
					tabel_review.field_names = ('Data', 'Input')
					tabel_review.align = 'l'
					tabel_review.add_rows((
						('Nama         ', nama),
						('Email        ', email),
						('Nomor Telepon', nomor_telepon),
						('Alamat       ', alamat),
					))

					print(tabel_review)
					input('Tekan untuk konfirmasi...')
					print('Loading...')
					
					sql(
						query='UPDATE penerbit SET nama = %s, email = %s, nomor_telepon = %s, alamat = %s WHERE id_penerbit = %s;',
						data=(nama, email, nomor_telepon, alamat, id_penerbit)
					)

					return Penerbit.tampilkan_penerbit(pesan=colored('Berhasil mengedit penerbit.', 'green'))

				else :
					return Penerbit.edit_penerbit(pesan=colored('ID penerbit tidak ditemukan.', 'red'))
			
			return Penerbit.edit_penerbit(pesan=colored('Mohon pilih ID penerbit.', 'red'))

		except KeyboardInterrupt :
			return Penerbit.menu_manajemen_penerbit()

	def cek_penerbit(id_penerbit) :
		return sql(
			query='SELECT COUNT(id_penerbit) AS hasil FROM penerbit WHERE id_penerbit = %s',
			data=(id_penerbit,),
			hasil=lambda cursor: cursor.fetchone()['hasil']
		)

	def hapus_penerbit(pesan=None) :
		try :
			bersihkan_console()
			print(f"Admin > Manajemen Penerbit > {colored('Hapus Penerbit', 'blue')}")

			if pesan : print(pesan) # pesan tambahan, opsional

			Penerbit.tampilkan_tabel_penerbit(pakai_id=True)
			id_penerbit = input('Pilih ID:\n> ')

			if id_penerbit :
				if Penerbit.cek_penerbit(id_penerbit) :
					# konfirmasi penghapusan
					input(colored('Tekan untuk mengonfirmasi penghapusan...', 'yellow'))
					print('Loading...')

					berhasil_menghapus = sql(
						query='DELETE FROM penerbit WHERE id_penerbit = %s',
						data=(id_penerbit,),
						hasil=lambda cursor: cursor.rowcount
					)

					if berhasil_menghapus :
						return Penerbit.tampilkan_penerbit(pesan=colored('Penerbit berhasil dihapus.', 'green'))

					# jika gagal menghapus data
					return Penerbit.tampilkan_penerbit(pesan=colored('Terjadi kesalahan, silakan coba lagi.', 'red'))

				else :
					return Penerbit.hapus_penerbit(pesan=colored('ID penerbit tidak ditemukan.', 'red'))
			
			return Penerbit.hapus_penerbit(pesan=colored('Mohon pilih ID penerbit.', 'red'))

		except KeyboardInterrupt :
			return Penerbit.menu_manajemen_penerbit()

# class Pengadaan :
# 	"""
# 		PENGADAAN
# 	"""

# 	def menu_manajemen_pengadaan() :
# 		try :
# 			bersihkan_console()

# 			print(f"Admin > {colored('Pengadaan', 'blue')}")
# 			print('[1] Tampilkan')
# 			print('[2] Tambah')
# 			print('[3] Hapus')
# 			print(colored('[4] Kembali', 'yellow'))
# 			menu = input('Pilih:\n> ')

# 			if menu == '1' :
# 				return Pengadaan.tampilkan_pengadaan()
# 			elif menu == '2' :
# 				# return Petugas.tambah_petugas()
# 				print('Tambah')
# 			elif menu == '3' :
# 				# return Petugas.hapus_petugas()
# 				print('Hapus')
# 			elif menu == '4' :
# 				return menu_admin()
# 			else :
# 				return Pengadaan.menu_manajemen_petugas()

# 		except KeyboardInterrupt :
# 			return menu_admin()

# 	def tampilkan_pengadaan() :
# 		try :
# 			bersihkan_console()
# 			print(f'Admin > Pengadaan > {colored("Tampilkan Pengadaan", "blue")}')

# 			conn = koneksi()
# 			cursor = conn.cursor(dictionary=True)

# 			pengadaan = cursor.execute((
# 				'SELECT pengadaan.id_pengadaan, pengadaan.tanggal AS tanggal_pengadaan, penerbit.nama AS nama_penerbit FROM pengadaan'
# 				' JOIN penerbit ON pengadaan.id_penerbit = penerbit.id_penerbit;'
# 			))
# 			pengadaan = cursor.fetchall()

# 			tabel = PrettyTable()
# 			tabel.title = 'Daftar Pengadaan'
# 			tabel.field_names = ('ID', 'Tanggal', 'Penerbit')

# 			_pengadaan = []

# 			for i in range(len(pengadaan)) :
# 				_pengadaan.append((
# 					pengadaan[i]['id_pengadaan'],
# 					pengadaan[i]['tanggal_pengadaan'],
# 					pengadaan[i]['nama_penerbit']
# 				))

# 			tabel.add_rows(_pengadaan)
# 			print(tabel)

# 			if cursor.rowcount :
# 				id_pengadaan = input('Pilih ID:\n> ')
# 				pengadaan = next(filter(lambda pengadaan: pengadaan['id_pengadaan'] == id_pengadaan, _pengadaan))
# 				tanggal = pengadaan['tanggal_pengadaan']
# 				penerbit = pengadaan['nama_penerbit']

# 				detail_pengadaan = cursor.execute(
# 					(
# 						'SELECT detail.id_detail_pengadaan, buku.isbn, buku.judul, detail.jumlah, detail.harga_satuan AS harga '
# 						'FROM detail_pengadaan AS detail WHERE id_pengadaan = %s '
# 						'JOIN buku ON detail.isbn = buku.isbn;'
# 					),
# 					(id_pengadaan,)
# 				)
# 				detail_pengadaan = cursor.fetchall()

# 				tabel = PrettyTable()
# 				tabel.title = f'Pengadaan tanggal {tanggal} dari {penerbit}'
# 				tabel.field_names = ('ID', 'ISBN', 'Judul Buku', 'Jumlah', 'Harga', 'Sub Harga')

# 				for i in range(len(detail_pengadaan)) :
# 					jumlah = detail_pengadaan[i]['jumlah']
# 					harga = detail_pengadaan[i]['harga']
# 					tabel.add_row((
# 						detail_pengadaan[i]['id_detail_pengadaan'],
# 						detail_pengadaan[i]['isbn'],
# 						detail_pengadaan[i]['judul'],
# 						jumlah,
# 						harga,
# 						harga * jumlah
# 					))

# 				bersihkan_console()
# 				print(f'Admin > Pengadaan > Tampilkan Pengadaan > {colored(f"Pengadaan tanggal {tanggal}", "blue")}')
# 				print(tabel)
			
# 			else: input('...')

# 			return Pengadaan.menu_manajemen_pengadaan()

# 		except KeyboardInterrupt :
# 			return Pengadaan.menu_manajemen_pengadaan()

# 	def tambah_pengadaan() :
# 		try :
# 			bersihkan_console()
# 			print(f'Admin > Pengadaan > {colored("Tambah Pengadaan", "blue")}')

# 			Penerbit.tampilkan_tabel_penerbit(pakai_id=True)
# 			id_penerbit = input('Pilih ID penerbit:\n> ')

# 			# cek apakah penerbit ada
# 			if id_penerbit and Penerbit.cek_penerbit(id_penerbit) :
# 				tanggal = datetime.now()
# 				tanggal = input(f'Tanggal ({tanggal}):\n> ') or tanggal
				
# 				conn = koneksi()
# 				cursor = conn.cursor(dictionary=True)

# 				cursor.execute('INSERT INTO pengadaan VALUES (null, %s, %s)', (id_penerbit, tanggal))
				
# 				if cursor.rowcount :
# 					return Pengadaan.tambah_detail_pengadaan(cursor)

# 		except KeyboardInterrupt :
# 			return Pengadaan.menu_manajemen_pengadaan()

# 	def tambah_detail_pengadaan(cursor) :
# 		try :
# 			bersihkan_console()
# 			print(f'Admin > Pengadaan > {colored("Tambah Pengadaan", "blue")}')

# 			pengadaan_id = cursor.lastrowid
# 			pengadaan = cursor.execute(
# 				'SELECT pengadaan.tanggal AS tanggal, penerbit.nama AS nama_penerbit FROM pengadaan WHERE id_pengadaan = %s '
# 				'JOIN penerbit ON pengadaan.id_penerbit = penerbit.id_penerbit;', 
# 				(pengadaan_id,)
# 			)
# 			pengadaan = cursor.fetchone()
			
# 			print(f'Penerbit : {pengadaan["nama_penerbit"]}')
# 			print(f'Tanggal  : {pengadaan["tanggal"]}')

# 			# simpan data pengadaan di dalam linkedlist
# 			detail_pengadaan = LinkedList()

# 			input_lagi = True
# 			while input_lagi :
# 				jumlah_pengadaan = detail_pengadaan.count()
# 				if jumlah_pengadaan == 0 : print('- ' * 20)

# 				isbn 				 = input('ISBN   : ')
# 				harga_satuan = input('Harga  : ')
# 				jumlah 			 = input('Jumlah : ')
# 				detail_pengadaan.insert({ 'isbn': isbn, 'harga_satuan': harga_satuan, 'jumlah': jumlah })
				
# 				print('- ' * 20)
# 				input_lagi = input('Tambah (Enter\\n):\n>').lower() != 'n'

# 			bersihkan_console()
# 			print(f'Admin > Pengadaan > {colored("Tambah Pengadaan", "blue")}')

# 			tabel_review = PrettyTable()
# 			tabel_review.title = f'Pengadaan tanggal {pengadaan["tanggal"]} dari {pengadaan["penerbit"]}'
# 			tabel_review.field_names = ('No', 'ISBN', 'Harga', 'Jumlah', 'Sub Harga')

# 			detail_pengadaan = detail_pengadaan.tolist()
# 			for i in range(len(detail_pengadaan)) :
# 				harga = detail_pengadaan[i]['harga']
# 				jumlah = detail_pengadaan[i]['jumlah']
# 				tabel_review.add_row((
# 					(i + 1),
# 					detail_pengadaan[i]['isbn'],
# 					harga,
# 					jumlah,
# 					harga * jumlah
# 				))

# 			print(tabel_review)
# 			input('Konfirmasi pengadaan...')

# 			for i in range(len(detail_pengadaan)) :
# 				isbn = detail_pengadaan[i]['isbn']
# 				harga = detail_pengadaan[i]['harga']
# 				jumlah = detail_pengadaan[i]['jumlah']
				
# 				buku = cursor.execute('SELECT COUNT(id_buku) FROM buku WHERE isbn = %s;', (isbn,))
# 				buku = buku.fetchone()

# 				# jika buku sudah ada, maka update data buku
		
# 		except KeyboardInterrupt :
# 			return Pengadaan.menu_manajemen_pengadaan()