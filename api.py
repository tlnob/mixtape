import glob, os, re, json, csv

data = 'datasets/gtfs_emtu/'

def unquote(str):
	if str[0] == '"' and str[-1] == '"':
		return str[1:-1]
	else:
		return str

def parse(nomearq):
	first = True
	attr = []
	arr = []
	with open(nomearq) as arq:
		for line in csv.reader(arq, delimiter=','):
			if first:
				attr = line
				first = False
			else:
				obj = {}
				for i in range(len(attr)):
					obj[attr[i]] = line[i]
				arr.append(obj)
	return arr
			

def primarykey(db, table, key):
	arr = db[table]
	out = {}
	for obj in arr:
		out[obj[key]] = obj
	db[table] = out

def join(db, str, table, key):
	for i in db[str].keys():
		trip = db[str][i]
		obj_id = trip[key]
		obj = db[table][obj_id]
		obj.setdefault(str, [])
		obj[str].append(i)

db = {}
for datafile in glob.glob(os.path.join(data, '*.txt')):
	table = datafile.replace(data,'')[:-4]
	db[table] = parse(datafile)


primarykey(db, "trips", "trip_id")
primarykey(db, "shapes", "shape_id")
primarykey(db, "routes", "route_id")
primarykey(db, "agency", "agency_id")
primarykey(db, "frequencies", "trip_id")
primarykey(db, "stop_times", "trip_id")
primarykey(db, "fare_attributes", "fare_id")
primarykey(db, "fare_rules", "fare_id")
primarykey(db, "stops", "stop_id")

join(db, "trips", "shapes", "shape_id")
join(db, "trips", "routes", "route_id")
join(db, "frequencies", "trips", "trip_id")
join(db, "stop_times", "trips", "trip_id")	
join(db, "routes", "agency", "agency_id")	
join(db, "fare_attributes", "fare_rules", "fare_id")	
join(db, "stop_times", "stops", "stop_id")


print(json.dumps(db, sort_keys=True, indent=4))