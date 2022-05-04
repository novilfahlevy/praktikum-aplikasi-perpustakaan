class QueueNode :
	def __init__(self, data): 
		self.data = data
		self.next = None
		self.prev = None
 
class Queue :
	def __init__(self) :
		self.head = None
		self.last = None

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