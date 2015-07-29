def read_csv(file_path, has_header = True, label = -1):
    with open(file_path) as f:
        if has_header: f.readline()
        data = []
        for line in f:
		line = line.strip().split(",")
		l = []
		for x in line :
			if x != line[label] :
            			l.append(float(x))
			else :
				l.append(x)
		data.append(l)
    return data

def write_csv(file_path, data):
    with open(file_path,"w") as f:
        for line in data: f.write(",".join(line) + "\n")
