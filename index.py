import os
import sys
import bcrypt
import pwinput
from termcolor import colored

from helper import bersihkan_console, hash_password
from database import koneksi
from auth import login, logout, ambil_session

def menu_admin() :
	try :
		bersihkan_console()

		print('Admin')
		print('[1] Petugas')
		print('[2] Penerbit')
		print('[3] Pengadaan')
		print(colored('[4] Keluar', 'yellow'))
		menu = input('Pilih:\n> ')

		if menu == '1' :
			return menu_manajemen_petugas()
		elif menu == '2' :
			# return menu_manajemen_penerbit()
			print('Penerbit')
		elif menu == '3' :
			# return menu_manajemen_pengadaan()
			print('Pengadaan')
		elif menu == '4' :
			return logout()
		else :
			return menu_admin()

	except KeyboardInterrupt :
		return menu_admin()

def menu_manajemen_petugas() :
	try :
		bersihkan_console()

		print('Admin > Manajemen Petugas')
		print('[1] Tampilkan')
		print('[2] Tambah')
		print('[3] Edit')
		print('[4] Hapus')
		print(colored('[5] Kembali', 'yellow'))
		menu = input('Pilih:\n> ')

		if menu == '1' :
			print('Tampilkan petugas')
		elif menu == '2' :
			print('Tambah petugas')
		elif menu == '3' :
			print('Edit petugas')
		elif menu == '4' :
			print('Hapus petugas')
		elif menu == '5' :
			return menu_admin()
		else :
			return menu_manajemen_petugas()

	except KeyboardInterrupt :
		return menu_admin()

def menu_petugas() :
	print('Menu petugas')

def menu_member() :
	print('Menu member')

def app() :
	# buat_tabel()
	if login() :
		session = ambil_session(ke_json=True)
		role = session['role']
		if role == 'admin' :
			return menu_admin()
		elif role == 'petugas' :
			return menu_petugas()
		else :
			return menu_member()

app()