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

# 			# simpan data pengadaan di dalam LinkedListOfDict
# 			detail_pengadaan = LinkedListOfDict()

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