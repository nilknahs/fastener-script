import csv

#Open csv Files

rtdc_map = {}

with open('Fasteners-By_TDC.csv') as csvfile:
	readCSV = csv.reader(csvfile, delimiter = ',')

	header = next(readCSV)
	index_by_cname = { key: index for index, key in enumerate(header) }

#Reads Data in csv
	for row in readCSV:
		tdc = row[index_by_cname["TDC"]]
		rtdc = row[index_by_cname["RTDC"]]

	#Omits Blank TDC's
		if "" == tdc:
			continue

#Prints TDC & UTDC
		print(tdc, rtdc)


		rtdc_map[rtdc] = tdc

print(rtdc_map)