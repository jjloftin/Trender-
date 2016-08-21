import csv

def main():
	with open('yelp_academic_dataset_review.csv', 'rb') as infile:
		reader = csv.reader(infile)
		with open('yelp_academic_dataset_review_notext.csv', 'wb') as outfile:
			writer = csv.writer(outfile)
			for r in reader:
				r.pop(2)
				writer.writerow(r)

	infile.close()
	outfile.close()

main()