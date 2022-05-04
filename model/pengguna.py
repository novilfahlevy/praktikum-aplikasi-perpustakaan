from model.model import Model

class Pengguna(Model) :
  def __init__(self) -> None :
    super().__init__()

    self.nama = ''
    self.email = ''
    self.password = ''
    self.nomor_telepon = ''
    self.alamat = ''
    self.role = ''
    self.tanggal_dibuat = ''