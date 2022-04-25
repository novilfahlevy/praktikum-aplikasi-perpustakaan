from data_class import LinkedListOfDict

class ManajemenBuku :
  """
    Manajemen buku.
  """

  def __init__(self, app) :
    self.app = app
    self.data = LinkedListOfDict(softdelete=True)