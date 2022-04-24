import os
import sys
import bcrypt

def bersihkan_console() :
	os.system('clear' if sys.platform == 'linux' else 'cls')

def hash_password(password) :
	return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

class Node:
  def __init__(self, data=None): 
    self.data = data
    self.next = Node

class LinkedList:
  def __init__(self):  
    self.head = None
  
  def insert(self, data):
    new_node = Node(data)
    new_node.next = self.head
    self.head = new_node

  def delete(self, data, key=None):
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
  
  def search(self, data, key=None):
    current_node = self.head
    while current_node is not None :
      if self.search_data_in_node(current_node, data, key) :
        return current_node.data
      current_node = current_node.next
    return None
  
  def update(self, data, search_data, key=None):
    current_node = self.head
    while current_node is not None :
      if self.search_data_in_node(current_node, search_data, key) :
        for key in data : current_node.data[key] = data[key]
      current_node = current_node.next
  
  def search_data_in_node(self, node, data, key_search=None) :
    for key, value in node.data.items() :
      if key_search is None :
        if value == data : return True
      else :
        if key == key_search and value == data : return True
    return False
			
  def count(self) :
    if self.head is not None :
      node = self.head
      hitung = 0
      while node :
        node = node.next
        hitung = hitung + 1
      return hitung
    return 0

  def tolist(self) :
    result = []
    node = self.head
    while node :
      result.append(node.data)
      node = node.next
    return result
  
  def printlist(self):
    current = self.head
    while current :
      print(f'{current.data} ->', end='')
      current = current.next