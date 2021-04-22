class library:
	def __init__(self):
		self.src = open("utils\\lib\\basic.txt", "r").read()
		self.dict = {}
		self.vars = {}
		now = "nothing"
		for x in self.src.split('\n'):
			if len(x) == 0: continue
			elif x[0] == ':':
				now = x[1:]
			elif x[0] == '/':
				before = x[1:].split()[0]
				after = x[1:].split()[1]
				params = x[1:].split()[2:]
				self.dict[before] = {"type": now, "code": after, "params": params}

	def find(self, opcode: str):
		if opcode in self.dict:
			return self.dict[opcode]
		else: return None

	def create_var(self, before, after):
		self.vars[before] = after

	def get_var(self, before):
		return self.vars[before]