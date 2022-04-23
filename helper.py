import os
import sys
import bcrypt

def bersihkan_console() :
	os.system('clear' if sys.platform == 'linux' else 'cls')

def hash_password(password) :
	return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

class Node:
  def __init__(self, data = None, next=None): 
    self.data = data
    self.next = next

class LinkedList:
  def __init__(self):  
    self.head = None
  
  def insert(self, data):
    newNode = Node(data)
    if self.head :
      current = self.head
      while current.next :
        current = current.next
      current.next = newNode
    else :
      self.head = newNode
			
  def count(self) :
    if self.head is not None :
      node = self.head
      hitung = 1
      while node :
        node = node.next
        hitung = hitung + 1
      return hitung
    return 0

  def tolist(self) :
    result = []
    node = self.head
    while node :
      result.append(node)
      node = node.next
    return result
  
  def printlist(self):
    current = self.head
    while current :
      print(current.data)
      current = current.next