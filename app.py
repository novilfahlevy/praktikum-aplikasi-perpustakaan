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

	def main(self) :
		# buat_tabel(truncate=True, seed=True)
		if self.auth.login() :
			session = self.auth.ambil_session(ke_json=True)
			role = session['role']

			if role == 'admin' 		 : return self.role_admin.menu_admin()
			elif role == 'petugas' : return self.role_petugas.menu_petugas()