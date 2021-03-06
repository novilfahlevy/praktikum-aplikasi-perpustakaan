import sys
import mysql.connector
from termcolor import colored

from helper import hash_password, bersihkan_console, kode_generator

class Database :
	def __init__(self, host=None, user=None, password=None, database=None) -> None:
		self.host = host or 'localhost'
		self.user = user or 'root'
		self.password = password or ''
		self.database = database or 'praktikum_perpustakaan'
		self.koneksi = None

	def aktifkan_koneksi(self) :
		try :
			self.koneksi = mysql.connector.connect(
				host=self.host,
				user=self.user,
				password=self.password,
				database=self.database
			)

			if self.koneksi.is_connected() :
				return self.koneksi
				
		except Exception as error :
			bersihkan_console()

			if error : print(colored(f'Error:\n{error}.', 'red'))

			message = """
				{backspace}Sebelum menjalankan aplikasi ini, nyalakan dulu mysql di XAMPP, lalu install {mysql_connector} menggunakan pip.
				{backspace}- - - - - - - - - - - - - - - -
				{backspace}pip install mysql-connector
				{backspace}- - - - - - - - - - - - - - - -

				{backspace}Buat database dengan nama {database}."""

			print(message.format(
				backspace=('\b' * 24),
				mysql_connector=colored('mysql-connector', 'yellow'),
				database=colored(self.database, 'green')
			))

	def buat_tabel(self, seed=False, truncate=False) :
		self.aktifkan_koneksi()
		cursor = self.koneksi.cursor()

		# jika ingin ditruncate, drop tabel yang sudah ada
		if truncate :
			cursor.execute('DROP TABLE IF EXISTS `pengguna`;')
			cursor.execute('DROP TABLE IF EXISTS `penerbit`;')
			cursor.execute('ALTER TABLE `pengadaan` DROP FOREIGN KEY pengadaan_dari_penerbit; DROP TABLE IF EXISTS `pengadaan`;', multi=True)
			cursor.execute('ALTER TABLE `buku_pengadaan` DROP FOREIGN KEY buku_dari_pengadaan; DROP TABLE IF EXISTS `buku_pengadaan`;', multi=True)
			cursor.execute('DROP TABLE IF EXISTS `buku`;')
			cursor.execute("""
				ALTER TABLE `peminjaman` DROP FOREIGN KEY petugas_yang_menangani_peminjaman;
				ALTER TABLE `peminjaman` DROP FOREIGN KEY member_yang_meminjamn_buku;
				ALTER TABLE `peminjaman` DROP FOREIGN KEY buku_yang_dipinjam;
				DROP TABLE IF EXISTS `peminjaman`;
			""", multi=True)

		# buat tabel
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS `pengguna` (
				kode char(5) primary key not null,
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
			CREATE TABLE IF NOT EXISTS `buku_pengadaan` (
				id_buku_pengadaan int primary key auto_increment not null,
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
				judul text null,
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
				tanggal_selesai date null,
				tenggat date null,
				denda int not null
			);
		""")
		
		# definisi relasi
		cursor.execute('ALTER TABLE `pengadaan` ADD CONSTRAINT pengadaan_dari_penerbit FOREIGN KEY (`kode_penerbit`) REFERENCES `penerbit` (`kode`) ON DELETE SET NULL;', multi=True)
		cursor.execute('ALTER TABLE `buku_pengadaan` ADD CONSTRAINT buku_dari_pengadaan FOREIGN KEY (`kode_pengadaan`) REFERENCES `pengadaan` (`kode`) ON DELETE CASCADE;', multi=True)
		cursor.execute('ALTER TABLE `peminjaman` ADD CONSTRAINT petugas_yang_menangani_peminjaman FOREIGN KEY (`kode_petugas`) REFERENCES `pengguna` (`kode`) ON DELETE SET NULL;', multi=True)
		cursor.execute('ALTER TABLE `peminjaman` ADD CONSTRAINT member_yang_meminjamn_buku FOREIGN KEY (`kode_member`) REFERENCES `pengguna` (`kode`) ON DELETE SET NULL;', multi=True)
		cursor.execute('ALTER TABLE `peminjaman` ADD CONSTRAINT buku_yang_dipinjam FOREIGN KEY (`kode_buku`) REFERENCES `buku` (`kode`) ON DELETE SET NULL;', multi=True)
		
		# seed data
		if seed :
			cursor.execute("""
				INSERT INTO `pengguna` VALUES
				(%s, %s, %s, %s, %s, %s, %s, now()),
				(%s, %s, %s, %s, %s, %s, %s, now()),
				(%s, %s, %s, %s, %s, %s, %s, now());""",
				(
					kode_generator(4), 'Admin', 'admin@gmail.com', hash_password('12345'), '089609233200', 'Jl. Langsat No. 64', 'admin',
					kode_generator(4), 'Petugas', 'petugas@gmail.com', hash_password('12345'), '089609233200', 'Jl. Langsat No. 64', 'petugas',
					kode_generator(4), 'Member', 'member@gmail.com', '', '089609233200', 'Jl. Langsat No. 64', 'member',
				)
			)

			self.koneksi.commit()

		cursor.close()
		self.koneksi.close()

	def sql(self, query, data = [], hasil=None) :
		try :
			self.aktifkan_koneksi()
			cursor = self.koneksi.cursor(dictionary=True)

			cursor.execute(query, data)
			result = hasil(cursor) if hasil is not None else hasil
			self.koneksi.commit()
		
			return result
		except Exception as e :
			self.koneksi.rollback()
			sys.exit(e)
		finally :
			cursor.close()
			self.koneksi.close()