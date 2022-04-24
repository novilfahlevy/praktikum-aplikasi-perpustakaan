# from database import buat_tabel

from auth import Auth
from role.admin import Admin as RoleAdmin
from role.petugas import Petugas as RolePetugas

from role.manajemen.petugas import Petugas
from role.manajemen.penerbit import Penerbit
from role.manajemen.pengadaan import Pengadaan

from role.manajemen.buku import Buku
from role.manajemen.member import Member
from role.manajemen.peminjaman import Peminjaman

class App :
	def __init__(self):
		self.auth = Auth(app=self)

		self.petugas = Petugas()
		self.penerbit = Penerbit()
		self.pengadaan = Pengadaan()
		self.member = Member()
		self.buku = Buku()
		self.peminjaman = Peminjaman()

		self.role_admin = RoleAdmin(
			auth=self.auth,
			petugas=self.petugas,
			penerbit=self.penerbit,
			pengadaan=self.pengadaan,
			buku=self.buku
		)

		self.role_petugas = RolePetugas(
			auth=self.auth,
			member=self.member,
			buku=self.buku,
			peminjaman=self.peminjaman
		)

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