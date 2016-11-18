class Graphe(dict):

	def __init__(self,fichier):
		dict.__init__(self)
		self.fichier=fichier

	def parsing(self):
		"""
		Parsing the input file into a dict of dict.
		"""
		line=fichier.readline()
		self.node_number=int(line)
		line=fichier.readline()
		while line:
			info=line.split()
			if info[0] not in self:#New person
				self[info[0]]={}
			if info[1] not in self[info[0]]:#Multiple debts
				self[info[0]][info[1]]=0
			self[info[0]][info[1]]+=int(info[2])
			line=fichier.readline()

	def simplify_cycle(self,name_list):
		"""
		Simplify the debts between two people.
		"""
		minima = 9001 #It's over 9000
		for i in range(len(name_list)):
			minimum = min(self[name_list[i-1]][name_list[i]],minimum)
		for i in range(len(name_list)):
			self[name_list[i-1]][name_list[i]]-=minimum

	def simplify_graphe(self):
		"""
		Check the graphe to delete every redundant debt.
		"""
		#TODO : trouver les cycles
		for debtor in self:
			for creditor in self[debtor]:
				if debtor in self[creditor]:
					self.simplify_cycle([creditor,debtor])

	def detect_communities(self):
		#TODO TEST
		communities=[]

	def simplify_as_fuck(self,chemin1,chemin2):
		#TODO : Trouver celui qui a le plus de minimums et soustraire le minimum à tout ce chemin, pour l'ajouter à tout l'autre.

	def biggest_friend(self):
		#TODO

	def social_hub(self,k):
		#TODO
