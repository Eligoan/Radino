class Graph(dict):
	"""
	Implements a graph of debts relations as a dictionnary.
	(key : person ; value : dictionnary with key : other person ; value : owed money)
	"""
	def __init__(self, fichier):
		"""
		Initialize the graph, parse the input file, determine all communities, finds all cycles and simplifies them
		and finally determine the largest group of friends.
		"""
		dict.__init__(self)
		self.fichier = fichier
		self.parsing()
		self.communities = []
		self.findCommunities()
		self.findCycles()
		self.maxFriendGroup = set()
		for community in self.communities:
			self.BronKerbosch(set(), set(community), set())

	def parsing(self):
		"""
		Parsing the input file into a graph.
		"""
		inFile = open(self.fichier, "r")
		line = inFile.readline()
		self.graphOrder = int(line)
		line = inFile.readline()
		while line:
			info = line.split()
			if info[0] not in self:#New person
				self[info[0]] = {}
			if info[1] not in self:
				self[info[1]] = {}
			if info[1] not in self[info[0]]:#Multiple debts
				self[info[0]][info[1]] = 0
			self[info[0]][info[1]] += int(info[2])
			line = inFile.readline()

	def standardOutFormat(self):
		out = str(self.graphOrder) + "\n"
		for name in self:
			for nxt in self[name]:
				out += "{0} {1} {2}".format(name, nxt, self[name][nxt])
				out += "\n"
		return out

	def printInfos(self):
		print("Processed graph: ")
		print(self.standardOutFormat())
		print("List of communities: ", self.communities)
		print("Maximum complete subgraph: ", self.maxFriendGroup)
		print("\n\n-----------------------\n\n")

	def substractFromPath(self, path, value):
		"""
		Substracts value from all debts between people, following path
		"""
		for i in range(len(path) - 1):
			self[path[i]][path[i+1]] -= value

	def simplifyCycle(self,nameList):
		"""
		Simplify the debts in a given cycle of people.
		"""
		if nameList[0] == nameList[-1]:
			self.substractFromPath(nameList, self.searchMin(nameList)[0])

	def searchMin(self, path):
		"""
		Search for the minimum debt in a path of people.
		"""
		nbrMini = 0
		minimum = float("inf")
		for i in range(len(path) - 1):
			if self[path[i]][path[i+1]] == minimum: #new encounter of min
				nbrMini += 1
			elif self[path[i]][path[i+1]] < minimum: #smaller minimum
				nbrMini = 0
				minimum = self[path[i]][path[i+1]]
		return minimum, nbrMini

	def prec(self, name):
		"""
		Returns all predecessors of node "name".
		"""
		for perhaps_prec in self: #recursively works on all predecessors
			if name in self[perhaps_prec]:
				yield perhaps_prec

	def neighbours(self, name) :
		"""
		Returns a set of all neighbours pointed by the given node.
		"""
		temp = set(self[name])
		for pre in self.prec(name):
			temp.add(pre)
		return temp

	def findCycles(self):
		"""
		Finds all cycles in the graph and simplify them all.
		"""
		visited = {i : False for i in self}
		path = []

		def parseForCycles(name):
			path.append(name)
			if visited[name]:
				try:
					self.simplifyCytcle(path[path.index(name):]) #index list method allows to parse the path only once
				except ValueError: #if name is not in path
					pass
			else:
				visited[name] = True
				for debtor in self[name]: #recursively loops over all successors
					parseForCycles(debtor)
			path.pop() #backtracks

		for name in self:
			if not visited[name]:
				parseForCycles(name)

	def findCommunities(self):
		"""
		Initialize "visited" dict (common to all recursive calls of the nested function) and loops over the graph.
		"""
		visited = {name: False for name in self}
		res = set()

		def detectCommunities(current):
			"""
			Loops recursively over all nodes reachable from current / from which current is reachable,
			and adds them to a set to be returned.
			"""
			if not visited[current]:
				visited[current] = True
				res.add(current)
				for name in self[current]: #recursively work on all successors
					detectCommunities(name)
				for preced in self.prec(current): #recursively works on all predecessors
					detectCommunities(preced)

		for name in self:
			if not visited[name]:
				detectCommunities(name)
				self.communities.append(set(res))
				res.clear()

	def BronKerbosch(self, R, P, X):
		"""
		Implements Bron–Kerbosch algorithm to find the maximum clique/complete subgraph of the master graph.
		R is the set of nodes that are in the current considered subgraph ; P is the set of candidates ;
		and X is the set of the already excluded candidates.
		"""
		if not P and not X : #if P and X are empty
			if len(self.maxFriendGroup) < len(R) :
				self.maxFriendGroup = set(R)
		namez = list(P) #copy to loop over (P modified in loop)
		for name in namez :
			self.BronKerbosch(R.union({name}),  P.intersection(self.neighbours(name)), X.intersection(self.neighbours(name)))
			P.remove(name)
			X.add(name)

	def simplifyMORE(self, path1, path2): #implemented but never used due to no search for "double" pathes
		"""
		Take two pathes from and to the same nodes and simplify these.
		"""
		minimum1, nbrMini1 = self.searchMin(path1)
		minimum2, nbrMini2 = self.searchMin(path2)
		if minimum1 == minimum2 : #find path with maximum zero after simplification
			if nbrMini1 > nbrMini2 :
				self.substractFromPath(path1, minimum1)
				self.substractFromPath(path2, -minimum1)
			else:
				self.substractFromPath(path2, minimum1)
				self.substractFromPath(path1, -minimum1)
		elif minimum1 < minimum2:
			self.substractFromPath(path1, minimum1)
			self.substractFromPath(path2, -minimum1)
		else:
			self.substractFromPath(path2, minimum2)
			self.substractFromPath(path1, -minimum2)
