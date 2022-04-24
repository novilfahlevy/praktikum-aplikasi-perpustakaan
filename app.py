from auth import login, ambil_session

# from database import buat_tabel

from role.admin import Admin
from role.petugas import menu_petugas

from role.manajemen.petugas import Petugas
from role.manajemen.penerbit import Penerbit

def main() :
	# buat_tabel(truncate=True, seed=True)
	if login() :
		session = ambil_session(ke_json=True)
		role = session['role']
		if role == 'admin' :
			admin = Admin(Petugas, Penerbit)
		elif role == 'petugas' :
			return menu_petugas()