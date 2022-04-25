from data_class import LinkedListOfDict

class ManajemenPeminjaman :
  """
    Manajemen peminjaman.
  """

  def __init__(self, app) :
    self.app = app
    self.data = LinkedListOfDict(softdelete=True)