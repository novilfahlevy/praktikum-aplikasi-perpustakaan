import sys
import mysql.connector
from termcolor import colored

from helper import hash_password, bersihkan_console, kode_generator

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

		message = """
			{backspace}Sebelum menjalankan aplikasi ini, nyalakan dulu mysql di XAMPP, lalu install {mysql_connector} menggunakan pip.
			{backspace}- - - - - - - - - - - - - - - -
			{backspace}pip install mysql-connector
			{backspace}- - - - - - - - - - - - - - - -

			{backspace}Buat database dengan nama {database}."""

		print(message.format(backspace=('\b' * 24), mysql_connector=colored('mysql-connector', 'yellow'), database=colored(database, 'green')))

def buat_tabel(seed=False, truncate=False) :
	# buat tabel
	conn = koneksi()
	cursor = conn.cursor()

	if truncate : cursor.execute('DROP TABLE IF EXISTS pengguna, penerbit, pengadaan, detail_pengadaan, buku, peminjaman;')

	cursor.execute("""
		CREATE TABLE IF NOT EXISTS `pengguna` (
			kode char(5) primary key not null,
			nama varchar(100) not null,
			email varchar(100) not null,
			password text null,
			nomor_telepon varchar(15) not null,
			alamat text not null,
			role enum('admin', 'petugas', 'member') not null,
			terkonfirmasi boolean not null default 0,
			tanggal_dibuat datetime not null
		);
	""")
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS `penerbit` (
			kode char(5) primary key not null,
			nama varchar(100) not null,
			email varchar(100) not null,
			nomor_telepon varchar(15) not null,
			alamat text null
		);
	""")
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS `pengadaan` (
			kode char(5) primary key not null,
			kode_penerbit char(5) not null,
			tanggal date not null
		);
	""")
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS `detail_pengadaan` (
			id_detail_pengadaan int primary key auto_increment not null,
			kode_pengadaan char(5) not null,
			isbn varchar(15) not null,
			harga int not null,
			jumlah int not null
		);
	""")
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS `buku` (
			kode char(5) primary key not null,
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
			kode char(5) primary key not null,
			kode_petugas char(5) not null,
			kode_member char(5) not null,
			kode_buku char(5) not null,
			tanggal_mulai date not null,
			tanggal_selesai date not null,
			tanggal_kembalikan date null,
			denda int not null
		);
	""")
	cursor.execute('ALTER TABLE `pengadaan` ADD FOREIGN KEY (`kode_penerbit`) REFERENCES `penerbit` (`kode`);')
	cursor.execute('ALTER TABLE `detail_pengadaan` ADD FOREIGN KEY (`kode_pengadaan`) REFERENCES `pengadaan` (`kode`) ON DELETE CASCADE;')
	cursor.execute('ALTER TABLE `peminjaman` ADD FOREIGN KEY (`kode_petugas`) REFERENCES `pengguna` (`kode`);')
	cursor.execute('ALTER TABLE `peminjaman` ADD FOREIGN KEY (`kode_member`) REFERENCES `pengguna` (`kode`);')
	cursor.execute('ALTER TABLE `peminjaman` ADD FOREIGN KEY (`kode_buku`) REFERENCES `buku` (`kode`);')
	
	if seed :
		cursor.execute("""
			INSERT INTO pengguna VALUES
			(%s, %s, %s, %s, %s, %s, %s, 0, now()),
			(%s, %s, %s, %s, %s, %s, %s, 0, now()),
			(%s, %s, %s, %s, %s, %s, %s, 0, now());""",
			(
				kode_generator(4).lower(), 'Admin', 'admin@gmail.com', hash_password('12345'), '089609233200', 'Jl. Langsat No. 64', 'admin',
				kode_generator(4).lower(), 'Petugas', 'petugas@gmail.com', hash_password('12345'), '089609233200', 'Jl. Langsat No. 64', 'petugas',
				kode_generator(4).lower(), 'Member', 'member@gmail.com', '', '089609233200', 'Jl. Langsat No. 64', 'member',
			)
		)

		conn.commit()

	cursor.close()

def sql(query, data = [], hasil=None) :
	try :
		conn = koneksi()
		cursor = conn.cursor(dictionary=True)

		cursor.execute(query, data)
		result = hasil(cursor) if hasil is not None else hasil
		conn.commit()
	
		return result
	except Exception as e :
		conn.rollback()
		sys.exit(e)
		# return None
	finally :
		cursor.close()
		conn.close()