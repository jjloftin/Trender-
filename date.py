import cx_Oracle

def main():
	con = cx_Oracle.connect('yelp', 'yelp', 'xe')
	cur = con.cursor()

	# Retrieve dates from Review or Tips
	cur.execute("select tip_date, tip_id from tips")
	#cur.execute("select review_date, review_id from review")
	id = []
	date = []
	for i in cur:
		id.append(i[1])
		# Reformat the date
		list = i[0].split('-')
		if list[1] == '01':
			list[1] = 'JAN'
		elif list[1] == '02':
			list[1] = 'FEB'
		elif list[1] == '03':
			list[1] = 'MAR'
		elif list[1] == '04':
			list[1] = 'APR'
		elif list[1] == '05':
			list[1] = 'MAY'
		elif list[1] == '06':
			list[1] = 'JUN'
		elif list[1] == '07':
			list[1] = 'JUL'
		elif list[1] == '08':
			list[1] = 'AUG'
		elif list[1] == '09':
			list[1] = 'SEP'
		elif list[1] == '10':
			list[1] = 'OCT'
		elif list[1] == '11':
			list[1] = 'NOV'
		elif list[1] == '12':
			list[1] = 'DEC'

		string = list[2] + '-' + list[1] + '-' + list[0][2:]
		date.append(string)

	num = 0
	for i in id:
		cur.execute("update tips set t_date = '" + date[num] + "' where tip_id = " + str(i))
		#cur.execute("update review set r_date = '" + date[num] + "' where review_id = '" + str(i) + "'")
		num += 1

	# Commit and close cur and con
	con.commit()
	cur.close()
	con.close()

main()