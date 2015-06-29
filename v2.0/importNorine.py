import json
import sys
import urllib2

def get_monomers() :
	'''
	Permits to get monomers list
	'''

	url = 'http://bioinfo.lifl.fr/norine/rest/monomers/flat/json'
	response = urllib2.urlopen(url).read()
	json_struct = json.loads(response)
	list_monomers = []
	for i in json_struct :
		if 'code' in i :
			list_monomers.append(i['code'])
	return list_monomers


def get_peptide(i) :
	'''
	Permits to get a peptide description in Json file
	'''

	url = 'http://bioinfo.lifl.fr/norine/rest/id/json/NOR'+`i`
	response = urllib2.urlopen(url).read()
	return response

def get_list_peptides() :
	'''
	Permits to get peptides'list without unknown activity
	'''

	# Header
	liste = [['activity','id','composition','link']]
	# For all peptides in ddb
	for i in range(1174) :  #1174 peptides
		print i
		json_data = get_peptide(i)
		json_struct = json.loads(json_data)
		if 'peptides' in json_struct :
			# If there is peptide description continue ... 
			if (len(json_struct['peptides']) >= 1) :
				# If there is activity description continue ...
				if ('activity' in json_struct['peptides'][0]['general']) :
						#Test if there is only 1 activity, or 2 with 'surfactant', and different of 'unknown'
						activity = json_struct['peptides'][0]['general']['activity']
						if (((len(activity) == 1) and (activity[0] != 'unknown') and (activity[0] != 'surfactant')) or ((len(activity) == 2) and (((activity[0]=='surfactant') or (activity[1]=='surfactant')) and ('unknown' not in activity )))) :
							# If there is 'surfactant' remove it from the activity list
							if 'surfactant' in activity :
								activity.remove('surfactant')
								print len(activity)
							# If there is id continue ...
							if 'id' in json_struct['peptides'][0]['general'] :
								# If there is composition description continue ...
								if 'composition' in json_struct['peptides'][0]['structure'] :
									# If ther is link description continue ...
									if 'graph' in json_struct['peptides'][0]['structure'] :
										composition = json_struct['peptides'][0]['structure']['composition']
										composition = "'" + composition.replace(', ',';') + "'"
										lien = json_struct['peptides'][0]['structure']['graph']
										lien = lien.replace(', ',';')
										# Put activity, id, composition and link at the list
										liste.append([activity[0], json_struct['peptides'][0]['general']['id'], composition, lien])
	return liste


