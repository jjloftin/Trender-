import cx_Oracle

def main():
	con = cx_Oracle.connect('yelp', 'yelp', 'xe')
	cur = con.cursor()

	a = list(cur.execute('select business_id, categories from business'))
	
	for item in a:
		if item[1] == '[]':
			continue
		else:
			u = (item[1][1:-1].split(','))
		
			v = item[0]
			
            

       
			for category in u:
				q = category.strip()[2:-1].replace('\'', '')
				r = "INSERT INTO categories values('{0}','{1}')".format(v, q)
				#print r
				cur.execute(r)
				#cur.execute("insert into categories (business_id, category) values ('" + v + "'," + category.strip()[1:] + ")")
	con.commit()
	cur.close()
	con.close()

main()