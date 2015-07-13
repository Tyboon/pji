
def nb_occ(monom, pep, sep = ';') :
	'''
	Counts the number of occurancies of a monomer in a peptide
	'''

	occ = 0
	list_p = pep.split(sep)
	occ = list_p.count(monom)
	return occ

def add_cpt(peptides,monomers) :
	'''
	Add to the peptides list the monomers counter
	'''

	#ajout de l'entete
	for m in monomers:
		peptides[0].append(m)
	
	#ajout des donnees
	for p in peptides :
		if p != peptides[0] :
			for m in monomers:
				p.append(nb_occ(m,p[2]))
	
	return peptides


def add_cpt_clusters(peptides, clusters) :
	'''
	Add to the peptides list the cluster counter
	'''
	len_m = len(peptides[0])
	#ajout de l'entete
	for c in clusters :
		peptides[0].append(c[0])

	#ajout des donnees
	for p in peptides :
		if p != peptides[0] :
			for c in clusters :
				p.append(nb_occ_clust(c,p, peptides[0], len_m))
	return peptides


def nb_occ_clust(cluster, pep, header, len_m) :
	'''
	Counts number of occurancies of cluster 
	'''
	cpt = 0
	for i in range(4,len_m) :
		if header[i] in cluster :
			cpt += pep[i]
	return cpt


def select_activity(peptides, N):
	'''
	Select only peptides whose activity counter over N 
	'''
	activities = list(set([row[0] for row in peptides]))
	peptides_act =list([row[0] for row in peptides]) 
	count_act = []
	for a in activities :
		count_act.append((a,peptides_act.count(a)))
	list_count = []
	for c in count_act :
		if c[1] >= N :
			list_count.append(c[0])
	#print list_count
	
	list_ceil = []
	for p in peptides :
		if p[0] in list_count:
			list_ceil.append(p)
	return list_ceil

def select_default(peptides) :
	'''
		Select peptides with only one activity or 2 whose one is surfactant
	'''
	doublon = dict()
	for p in peptides	: #detail par composition
		compo = p[2]
		if compo in doublon :
			doublon[compo].append(p)
		else :
			doublon[compo] = []
			doublon[compo].append(p)
	for k in doublon.keys() :
		len_k = len(doublon[k])
		if len_k >= 3 : #plus de 2 activites
			for v in doublon[k] :
				peptides.remove(v)
		elif len_k == 2 : #2 activites
			l = doublon[k]
			if l[0][0] == 'surfactant' :
				peptides.remove(l[0])
			elif l[1][0] == 'surfactant' :
				peptides.remove(l[1])
			else :
				peptides.remove(l[0])
				peptides.remove(l[1])
		else :
			pass
	return peptides

def add_cpt_link(peptides,N) :
	'''
	Add to peptides list the link counter
	'''
	len_p = len(peptides[0])
	# Ajout de l'entete
	for i in range(1,N+1) :
		lien = 'Lien : ' + `i`
		peptides[0].append(lien)
	
	# Ajout des compteurs ,pour chaque peptide
	for p in peptides :
		if p != peptides[0] :
			links_cpt = []
			links = p[3]
			links = links.split('@')
			links = links[1:len(links)]
			for link in links :
				links_cpt.append(len(link.split(',')))
			for i in range(1,N+1) :
				p.append(links_cpt.count(i))
	return peptides


def bounding (digit,bound_init, bound_mono, bound_clust) :
	'''
		give the bound of data useless that we could remove
	'''
	bound = ""
	if digit == 'm' :
		bound = "2-%d,%d-last" % (bound_init, bound_mono+1)
	elif digit == 'c' :
		bound = "2-%d,%d-last" % (bound_mono, bound_clust+1)
	elif digit == 'l' :
		bound = "2-%d" % (bound_clust)
	elif digit == 'mc' or digit == 'cm' :
		bound = "2-%d,%d-last" % (bound_init, bound_clust+1)
	elif digit == 'ml' or digit == 'lm' :
		bound = "2-%d,%d-%d" % (bound_init, bound_mono+1, bound_clust)
	elif digit == 'lc' or digit == 'cl' :
		bound = "2-%d" % (bound_mono)
	else : # mcl
		bound = "2-%d" % (bound_init)
	return bound


