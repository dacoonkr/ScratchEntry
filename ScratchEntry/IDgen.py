id_s = 'abcdefghijklmnopqrstuvwxyz1234567890'
id_n = [ 0, 0, 0, -1 ]

def getID():
	id_n[3] += 1
	if id_n[3] == 36:
		id_n[3] = 0
		id_n[2] += 1
	if id_n[2] == 36:
		id_n[2] = 0
		id_n[1] += 1
	if id_n[1] == 36:
		id_n[1] = 0
		id_n[0] += 1

	return id_s[id_n[0]] + id_s[id_n[1]] + id_s[id_n[2]] + id_s[id_n[3]]