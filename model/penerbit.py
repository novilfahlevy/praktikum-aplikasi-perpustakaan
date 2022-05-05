from model.model import Model

class Penerbit(Model) :
  def __init__(self) -> None :
    super().__init__()

    self.nama = ''
    self.email = ''
    self.nomor_telepon = ''
    self.alamat = ''