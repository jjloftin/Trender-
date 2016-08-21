import csv

def main():
	with open('yelp_academic_dataset_tip.csv', 'rb') as infile:
		reader = csv.reader(infile)
		with open('yelp_academic_dataset_tip_notext.csv', 'wb') as outfile:
			writer = csv.writer(outfile)
			num = 1
			for r in reader:
				if r[0] != 'user_id':
					r[1] = num
					num += 1
					writer.writerow(r)
					continue
				else:
					writer.writerow(r)
					continue

	infile.close()
	outfile.close()

main()