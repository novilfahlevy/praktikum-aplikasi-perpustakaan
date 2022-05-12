from model.model import Model

from asd.merge_sort import merge_sort
from asd.queue import Queue

class Node :
  def __init__(self, data=None) :
    self.data = data
    self.next = None

class LinkedList :
  def __init__(self, softdelete=False) :
    self.head = None
  
  def insert(self, data: Model, status='baru') :
    new_node = Node(data)
    new_node.next = self.head
    self.head = new_node
  
  def delete(self, nilai, kata_kunci=None) :
    current_node = self.head

    if self.head.data.cari(nilai, kata_kunci) :
      self.head.data.tetapkan_status('hapus')
      return

    while current_node is not None :
      if current_node.data.cari(nilai, kata_kunci) :
        current_node.data.tetapkan_status('hapus')
        break
      
      current_node = current_node.next

  # def update(self, data, nilai, atribut=None) :
  #   current_node = self.head
  #   while current_node is not None :
  #     if self.cari_data_node(current_node, nilai, atribut) :
  #       for key in data : setattr(current_node.data, key, data[key])
  #       if self.softdelete and current_node.data['status_data'] != 'baru' : current_node.data['status_data'] = 'ubah'
  #     current_node = current_node.next
  
  def cari(self, nilai, kata_kunci=None) :
    current_node = self.head
    while current_node is not None :
      if isinstance(current_node.data, Model) :
        if current_node.data.cari(nilai, kata_kunci) and current_node.data.status_data != 'hapus' :
          return current_node.data
      current_node = current_node.next
    return None
			
  def count(self) :
    if self.head is not None :
      node = self.head
      hitung = 0
      while node is not None :
        if node.data.status_data == 'hapus' :
          node = node.next
          continue
        node = node.next
        hitung = hitung + 1
      return hitung
    return 0

  def tetapkan_sebagai_tersimpan(self) :
    current_node = self.head
    while current_node is not None :
      current_node.data.tetapkan_status('lama')
      current_node = current_node.next

  def tolist(self, sort=None, semua=False) :
    result = []
    node = self.head
    while node is not None :
      if node.data.status_data == 'hapus' and semua is False :
        node = node.next
        continue
      else :
        result.append(node.data)
        node = node.next
    
    return result if sort is None else merge_sort(result, sort)

  def toqueue(self) :
    result = Queue()
    node = self.head
    while node is not None :
      if node.data.status_data == 'hapus' :
        node = node.next
        continue
      else :
        result.enqueue(node.data)
        node = node.next
    
    return result
  
  def printlist(self) :
    current = self.head
    hitung_tab = 1
    while current :
      if current.data.status_data == 'hapus' :
        current = current.next
        continue
      else :
        print('{} {}{}-> '.format(current.data, '\n', '\t' * hitung_tab), end='')
        hitung_tab = hitung_tab + 1
        current = current.next