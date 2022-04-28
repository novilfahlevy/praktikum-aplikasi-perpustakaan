
from helper import kode_generator


class LinkedListNode :
  def __init__(self, data=None) :
    self.data = data
    self.next = None

class LinkedListOfDict :
  def __init__(self, softdelete=False) :
    self.head = None
    self.softdelete = softdelete
  
  def insert(self, data, status='baru') :
    if type(data) != dict : raise('Type of data must be dictionary')
    new_node = LinkedListNode(data)
    new_node.next = self.head
    self.head = new_node
    if status == 'baru' : self.head.data['kode'] = kode_generator(4)
    if self.softdelete : self.head.data['status_data'] = status

  def delete(self, data, key=None) :
    if self.softdelete : self.soft_delete(data, key)
    else               : self.hard_delete(data, key)

  def hard_delete(self, data, key=None) :
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

  def tetapkan_sebagai_tersimpan(self) :
    current_node = self.head
    while current_node is not None :
      if self.softdelete : current_node.data['status_data'] = 'lama'
      current_node = current_node.next

  def tolist(self, sort=None, with_trashed=False) :
    result = []
    node = self.head
    while node is not None :
      if self.softdelete and (node.data['status_data'] == 'hapus') and not with_trashed :
        node = node.next
        continue
      else :
        result.append(node.data)
        node = node.next
    
    return result if sort is None else merge_sort(result, sort)

  def toqueue(self, with_trashed=False) :
    result = Queue()
    node = self.head
    while node is not None :
      if self.softdelete and (node.data['status_data'] == 'hapus') and not with_trashed :
        node = node.next
        continue
      else :
        result.enqueue(node.data)
        node = node.next
    
    return result
  
  def printlist(self, with_trashed=False) :
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

class QueueNode :
	def __init__(self, data): 
		self.data = data
		self.next = None
		self.prev = None
 
class Queue :
	def __init__(self, softdelete=False) :
		self.head = None
		self.last = None
		self.softdelete = softdelete

	def enqueue(self, data) :
		new_node = QueueNode(data)
		if self.last is None :
			self.head = new_node
			self.last = self.head
		else :
			self.last.next = new_node
			self.last.next.prev = self.last
			self.last = self.last.next

	def dequeue(self) :
		if self.head is None :
			return None
		else :
			temp = self.head
			if self.head.next is not None :
				self.head = self.head.next
				self.head.prev = temp
			else :
				self.head = None
				self.last = None
			return temp.data

	def requeue(self, count = 1) :
		results = []
		for _ in range(count) :
			result = self.dequeue()
			if result is not None :
				self.enqueue(result)
				results.append(result)
			else : break

		return results

	def enqueue_reverse(self, data) :
		new_node = QueueNode(data)
		if self.last is None :
			self.head = new_node
			self.last = self.head
		else :
			temp = self.head
			self.head = new_node
			temp.prev = self.head
			self.head.next = temp
			self.head.prev = None

	def dequeue_reverse(self) :
		if self.last is None :
			return None
		else :
			temp = self.last.data
			if self.last.prev is not None :
				self.last = self.last.prev
				self.last.next = None
			else :
				self.last = None
			return temp

	def requeue_reverse(self, count = 1) :
		results = []
		for _ in range(count) :
			result = self.dequeue_reverse()
			if result is not None :
				self.enqueue_reverse(result)
				results.append(result)
			else :
				break

		return results

	def first(self) :    
		return self.head.data 

	def size(self) :
		temp = self.head 
		count = 0
		while temp is not None :
			count = count + 1
			temp = temp.next
		return count

	def isEmpty(self) :
		if self.head is None :
			return True
		else :
			return False
  
	def printqueue(self) :
		print("queue elements are:") 
		temp = self.head 
		while temp is not None :
			print(temp.data, end="->")
			temp = temp.next
	
	def tolist(self, count=None) :
		results = []
		node = self.head
		if count is None :
			while node is not None :
				results.append(node.data)
				node = node.next
		else :
			hitung = 0
			while node is not None :
				hitung = hitung + 1
				results.append(node.data)
				node = node.next

				if hitung >= count : break

		return results

def merge_sort(lst, compare):
  if len(lst) <= 1 :
    return lst

  mid = len(lst) // 2

  left = merge_sort(lst[0:mid], compare)
  right = merge_sort(lst[mid:len(lst)], compare)
  
  return merge(left, right, compare)

def merge(left, right, compare) :
  result = []
  i, j = 0, 0

  while i < len(left) and j < len(right) :
    if compare(left[i], right[j]) :
      result.append(left[i])
      i += 1
    else :
      result.append(right[j])
      j += 1

  result += left[i:]
  result += right[j:]

  return result

def binary_search(lys, val, key) :
  """
    Pencarian untuk list of dict.
  """
  first = 0
  last = len(lys) - 1
  row = -1

  while (first <= last) and (row == -1) :
    mid = (first + last) // 2

    if lys[mid][key] == val :
      row = mid
    else :
      if val < lys[mid][key] :
        last = mid - 1
      else:
        first = mid + 1
  
  return lys[mid]