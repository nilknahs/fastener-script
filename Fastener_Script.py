#!/usr/bin/env python3
import csv
import os
import sys
import click
from PyInquirer import prompt

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


def select_dups_folder(message = "Please name your dups (duplicate) folder:"):
	questions = [{'type': 'input','name': 'dups_folder','message': message}]
	answers = prompt(questions)
	if not answers:
		raise Exception
	return answers['dups_folder']

def select_csv_file(message = "Please input your .csv location:"):
	questions = [{'type': 'input','name': 'csv_folder','message': message}]
	answers = prompt(questions)
	if not answers:
		raise Exception
	return answers ['csv_folder']

@click.command()
@click.option('--dups_folder', '-df')
@click.option('--path_to_fastener_photos', '-pfp')
@click.option('--path_to_csv', '-pcsv')
def main(path_to_csv, path_to_fastener_photos, dups_folder):
	"""
	This script renames "RTDCs" to "TDCs" of fastener photo data. First, 
	locate your fastener photo data folder.
	"""
	if not dups_folder:
		dups_folder = select_dups_folder()
	if not os.path.exists(dups_folder): 
		os.mkdir(dups_folder)

	if not path_to_csv:
		path_to_csv = select_csv_file()
	if not os.path.exists(path_to_csv):
		print (f'Hey. I can\'t seem to find a csv file called "{path_to_csv}"')
		exit()
	
	if not path_to_fastener_photos:
		return
	if not os.path.exists(path_to_fastener_photos):
		print (f'Hey. I can\'t seem to find a file called "{path_to_fastener_photos}"')
		exit()

	rtdc_map = build_rtdc_map(path_to_csv)
	rename_rtdc_files(path_to_fastener_photos, rtdc_map, dups_folder)

if __name__ == "__main__":
	main()