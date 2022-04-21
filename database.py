import mysql.connector
from termcolor import colored

from helper import hash_password, bersihkan_console

def koneksi() :
	# sesuaikan dengan data anda
	host 		 = 'localhost'
	user 		 = 'root'
	password = ''
	database = 'praktikum_si_c_perpustakaan'

	try :
		# masukan informasi terkait database sesuai dengan punya anda
		conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
		if conn.is_connected() : return conn
			
	except Exception as error :
		bersihkan_console()

		if error : print(colored(f'Error:\n{error}.', 'red'))

		message = f"""
			\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\bSebelum menjalankan aplikasi ini, nyalakan dulu mysql di XAMPP, lalu install {colored('mysql-connector', 'yellow')} menggunakan pip.
			\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b- - - - - - - - - - - - - - - -
			\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\bpip install mysql-connector
			\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b- - - - - - - - - - - - - - - -

			\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\bBuat database dengan nama {colored(database, 'green')}."""

		print(message)

def buat_tabel(seed=False, truncate=False) :
	# buat tabel
	conn = koneksi()
	cursor = conn.cursor()

	if truncate : cursor.execute('DROP TABLE IF EXISTS pengguna, penerbit, pengadaan, detail_pengadaan, buku, peminjaman;')

	cursor.execute("""
		CREATE TABLE IF NOT EXISTS `pengguna` (
			id_pengguna int primary key auto_increment not null,
			nama varchar(100) not null,
			email varchar(100) not null,
			password text null,
			nomor_telepon varchar(15) not null,
			alamat text not null,
			role enum('admin', 'petugas', 'member') not null,
			tanggal_dibuat datetime not null
		);
	""")
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS `penerbit` (
			id_penerbit int primary key auto_increment not null,
			nama varchar(100) not null,
			email varchar(100) not null,
			nomor_telepon varchar(15) not null,
			alamat text null
		);
	""")
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS `pengadaan` (
			id_pengadaan int primary key auto_increment not null,
			id_penerbit int not null,
			tanggal date not null
		);
	""")
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS `detail_pengadaan` (
			id_detail_pengadaan int primary key auto_increment not null,
			id_pengadaan int not null,
			isbn varchar(15) not null,
			harga_satuan int not null,
			jumlah int not null
		);
	""")
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS `buku` (
			id_buku int primary key auto_increment not null,
			isbn varchar(15) not null,
			judul text not null,
			penulis text null,
			genre text null,
			jumlah_halaman int null,
			jumlah int not null
		);
	""")
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS `peminjaman` (
			id_peminjaman int primary key auto_increment not null,
			kode varchar(6),
			id_petugas int,
			id_member int,
			id_buku int,
			tanggal_mulai date not null,
			tanggal_selesai date not null,
			tanggal_kembalikan date null,
			denda int not null
		);
	""")
	cursor.execute('ALTER TABLE `pengadaan` ADD FOREIGN KEY (`id_penerbit`) REFERENCES `penerbit` (`id_penerbit`);')
	cursor.execute('ALTER TABLE `pengadaan` ADD FOREIGN KEY (`id_petugas`) REFERENCES `pengguna` (`id_pengguna`);')
	cursor.execute('ALTER TABLE `detail_pengadaan` ADD FOREIGN KEY (`id_pengadaan`) REFERENCES `pengadaan` (`id_pengadaan`);')
	cursor.execute('ALTER TABLE `peminjaman` ADD FOREIGN KEY (`id_petugas`) REFERENCES `pengguna` (`id_pengguna`);')
	cursor.execute('ALTER TABLE `peminjaman` ADD FOREIGN KEY (`id_member`) REFERENCES `pengguna` (`id_pengguna`);')
	cursor.execute('ALTER TABLE `peminjaman` ADD FOREIGN KEY (`id_buku`) REFERENCES `buku` (`id_buku`);')

	if seed :
		cursor.execute("""
			INSERT INTO pengguna VALUES
			(null, %s, %s, %s, %s, %s, %s, now()),
			(null, %s, %s, %s, %s, %s, %s, now()),
			(null, %s, %s, %s, %s, %s, %s, now());""",
			(
				'Admin', 'admin@gmail.com', hash_password('12345'), '089609233200', 'Jl. Langsat No. 64', 'admin',
				'Petugas', 'petugas@gmail.com', hash_password('12345'), '089609233200', 'Jl. Langsat No. 64', 'petugas',
				'Member', 'member@gmail.com', '', '089609233200', 'Jl. Langsat No. 64', 'member',
			)
		)

		conn.commit()

	cursor.close()