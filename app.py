# from database import buat_tabel

from auth import Auth
from role.admin import RoleAdmin
from role.petugas import RolePetugas

from manajemen.petugas import ManajemenPetugas
from manajemen.penerbit import ManajemenPenerbit
from manajemen.pengadaan import ManajemenPengadaan

from manajemen.buku import ManajemenBuku
from manajemen.member import ManajemenMember
from manajemen.peminjaman import ManajemenPeminjaman

class App :
	def __init__(self):
		self.auth = Auth(self)

		self.petugas = ManajemenPetugas(self)
		self.penerbit = ManajemenPenerbit(self)
		self.pengadaan = ManajemenPengadaan(self)
		self.member = ManajemenMember(self)
		self.buku = ManajemenBuku(self)
		self.peminjaman = ManajemenPeminjaman(self)

		self.role_admin = RoleAdmin(self)
		self.role_petugas = RolePetugas(self)

		self.main()

	def main(self, force_close=False) :
		# buat_tabel(truncate=True, seed=True)
		if force_close is not True :
			session = self.auth.ambil_session(ke_json=True)
			if session is not None :
				self.auth.session = session
				return self.menu(self.auth.session['role'])

		akun = self.auth.login()
		if akun is not None :
			self.auth.session = akun
			return self.menu(self.auth.session['role'])

	def menu(self, role) :
		if role == 'admin' 		 : return self.role_admin.menu_admin()
		elif role == 'petugas' : return self.role_petugas.menu_petugas()