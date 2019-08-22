#!/usr/bin/env python3
import csv
import os
import sys
import click

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


def rename_rtdc_files(path_to_root, rtdc_map, dups_folder):

	for rtdc in rtdc_map:
		old_name = os.path.join(path_to_root, rtdc)
		if os.path.exists(old_name):
			tdc = rtdc_map[rtdc]
			new_name = os.path.join(path_to_root, tdc)

			if os.path.exists(new_name):
				print(f'{tdc} Already exists! Moving to dups folder.')
				suffix = ""
				for i in range(1, 5):
					new_name = os.path.join(dups_folder, tdc + suffix)
					if not os.path.exists(new_name):
						break
					suffix = f"-{i}"

			try:
				os.rename(old_name, new_name)
				print(f'rename {old_name} -> {new_name}')
			except OSError:
				print(f"ERROR: {rtdc} rename failed, skipping.")


@click.command()
@click.argument('path_to_csv')
@click.argument('path_to_fastener_photos')
@click.argument('dups_folder')
def main(path_to_csv, path_to_fastener_photos, dups_folder):
	if not os.path.exists(dups_folder): 
		os.mkdir(dups_folder)
	rtdc_map = build_rtdc_map(path_to_csv)
	rename_rtdc_files(path_to_fastener_photos, rtdc_map, dups_folder)

if __name__ == "__main__":
	main()