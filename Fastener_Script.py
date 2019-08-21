import csv
import os


def build_rtdc_map(path_to_csv):
	rtdc_map = {}
	#Open csv Files
	with open(path_to_csv) as csvfile:
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

			if "" != rtdc:
				rtdc_map[rtdc] = tdc

	return rtdc_map


def rename_rtdc_files(path_to_root, rtdc_map):
	for rtdc in rtdc_map:
		old_name = os.path.join(path_to_root, rtdc)
		if os.path.exists(old_name):
			tdc = rtdc_map[rtdc]
			new_name = os.path.join(path_to_root, tdc)
			print(f'rename {old_name} -> {new_name}')
			os.rename(old_name, new_name)


def main():
	rtdc_map = build_rtdc_map("Fasteners-By_TDC.csv")
	rename_rtdc_files("./test_data", rtdc_map)


if __name__ == "__main__":
	main()
