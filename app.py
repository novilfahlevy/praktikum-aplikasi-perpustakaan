from auth import login, ambil_session

# from database import buat_tabel

from modules.admin import menu_admin
from modules.petugas import menu_petugas
from modules.member import menu_member

def main() :
	# buat_tabel(truncate=True, seed=True)
	if login() :
		session = ambil_session(ke_json=True)
		role = session['role']
		if role == 'admin' :
			return menu_admin()
		elif role == 'petugas' :
			return menu_petugas()
		else :
			return menu_member()