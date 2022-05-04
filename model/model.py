from helper import kode_generator

class Model :
	def __init__(self) -> None :
		self.tetapkan_kode()
		self.kode = None
		self.status_data = 'baru'
	
	def tetapkan_kode(self, kode=None) -> None :
		self.kode = kode_generator(4) if kode is None else kode
	
	def cari(self, value, atribut=None) -> any :
		if atribut is None :
			for _, val in enumerate(self.__dict__.values()) :
				if val == value :
					return True
			return False
		else :
			val = getattr(self, atribut)
			return val == value

	def tetapkan_status(self, status) :
		if status == 'ubah' :
			if self.status_data == 'lama' :
				self.status_data = 'ubah'
		else :
			self.status_data = status