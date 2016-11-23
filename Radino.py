class Graphe(dict):
	def __init__(self,fichier):
		dict.__init__(self)
		self.fichier = fichier
		parsing(self)

	def parsing(self):
		"""
		Parsing the input file into a dict of dict.
		"""
		inFile = open(self.fichier, "r")
		line = inFile.readline()
		self.node_number = int(line)
		line = inFile.readline()
		while line:
			info = line.split()
			if info[0] not in self:#New person
				self[info[0]] = {}
			if info[1] not in self[info[0]]:#Multiple debts
				self[info[0]][info[1]] = 0
			self[info[0]][info[1]] += int(info[2])
			line = inFile.readline()

	def simplify_cycle(self,name_list):
		"""
		Simplify the debts in a cycle of people.
		"""
		if name_list[0] == name_list[-1]:
			substract(name_list, searchMin(name_list)[0])

	def simplify_graphe(self):
		"""
		Check the graphe to delete every redundant debt.
		"""
		#TODO : trouver les cycles
		for debtor in self:
			for creditor in self[debtor]:
				if debtor in self[creditor]:
					self.simplify_cycle([creditor,debtor])

	def searchMin(self, path):
		"""
		Search for the minimum debt in a path of people
		"""
		nbrMini = 0
		minimum = 9001
		for i in range(len(path) - 1):
			if self[path[i]][path[i+1]] == minimum:
				nbrMini += 1
			elif self[path[i]][path[i+1]] < minimum:
				nbrMini = 0
				minimum = self[path[i]][path[i+1]]
		return minimum, nbrMini

	def substract(self, path, value):
		"""
		Substracts value from all debts between people, following path
		"""
		for i in range(len(path) - 1):
			self[path[i]][path[i+1]] -= value

	def simplify_as_fuck(self,path1,path2):
		minimum1, nbrMini1 = searchMin(path1)
		minimum2, nbrMini2 = searchMin(path2)
		if minimum1 == minimum2:
			if nbrMini1 > nbrMini2:
				self.substract(path1, minimum1)
				self.substract(path2, -minimum1)
			else:
				self.substract(path2, minimum1)
				self.substract(path1, -minimum1)
		elif minimum1 < minimum2:
			self.substract(path1, minimum1)
			self.substract(path2, -minimum1)
		else:
			self.substract(path2, minimum2)
			self.substract(path1, -minimum2)

	def biggest_friend(self):
		#TODO

	def social_hub(self,k):
		#TODO
		
	def detect_communities(self):
		#TODO TEST HS
		communities=[]
