from helper import kode_generator

class Node:
  def __init__(self, data=None): 
    self.data = data
    self.next = Node

class LinkedListOfDict:
  def __init__(self, softdelete=False):  
    self.head = None
    self.softdelete = softdelete
  
  def insert(self, data, status='baru'):
    if type(data) != dict : raise('Type of data must be dictionary')
    new_node = Node(data)
    new_node.next = self.head
    self.head = new_node
    if status == 'baru' : self.head.data['kode'] = kode_generator(4).lower()
    if self.softdelete : self.head.data['status_data'] = status

  def delete(self, data, key=None) :
    if self.softdelete : self.soft_delete(data, key)
    else               : self.hard_delete(data, key)

  def hard_delete(self, data, key=None):
    current_node = self.head
    previous_node = None

    if self.search_data_in_node(self.head, data, key) :
      previous_node = self.head.next
      self.head = previous_node
      return

    while current_node is not None :
      if self.search_data_in_node(current_node, data, key) :
        break
      
      previous_node = current_node
      current_node = current_node.next

    if previous_node is not None :
      previous_node.next = current_node.next
  
  def soft_delete(self, data, key=None) :
    current_node = self.head

    if self.search_data_in_node(self.head, data, key) :
      self.head.data['status_data'] = 'hapus'
      return

    while current_node is not None :
      if self.search_data_in_node(current_node, data, key) :
        current_node.data['status_data'] = 'hapus'
        break
      
      current_node = current_node.next

  def update(self, data, search_data, key=None) :
    current_node = self.head
    while current_node is not None :
      if self.search_data_in_node(current_node, search_data, key) :
        for key in data : current_node.data[key] = data[key]
        if self.softdelete and current_node.data['status_data'] != 'baru' : current_node.data['status_data'] = 'ubah'
      current_node = current_node.next
  
  def search(self, data, key=None, with_trashed=False) :
    current_node = self.head
    while current_node is not None :
      if self.search_data_in_node(current_node, data, key, with_trashed=with_trashed) :
        return current_node.data
      current_node = current_node.next
    return None
  
  def search_data_in_node(self, node, data, key_search=None, with_trashed=False) :
    if self.softdelete and node.data['status_data'] == 'hapus' and not with_trashed : return False
    for key, value in node.data.items() :
      if key_search is None :
        if value == data : return True
      else :
        if key == key_search and value == data : return True
    return False
			
  def count(self, with_trashed=False) :
    if self.head is not None :
      node = self.head
      hitung = 0
      while node is not None :
        if self.softdelete and (node.data['status_data'] == 'hapus') and not with_trashed :
          node = node.next
          continue
        node = node.next
        hitung = hitung + 1
      return hitung
    return 0

  def tolist(self, with_trashed=False) :
    result = []
    node = self.head
    while node is not None :
      if self.softdelete and (node.data['status_data'] == 'hapus') and not with_trashed :
        node = node.next
        continue
      else :
        result.append(node.data)
        node = node.next
    return result
  
  def printlist(self, with_trashed=False):
    current = self.head
    hitung_tab = 1
    while current :
      if self.softdelete and (current.data['status_data'] == 'hapus') and not with_trashed :
        current = current.next
        continue
      else :
        print('{} {}{}-> '.format(current.data, '\n', '\t' * hitung_tab), end='')
        hitung_tab = hitung_tab + 1
        current = current.next