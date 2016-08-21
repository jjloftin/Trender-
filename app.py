import cx_Oracle
from datetime import date, timedelta as td
import time


def Main():

  print '\nWelcome to Trender - Alpha\n'
  
  filter = ['','','','','','']
  #        filter[0] == first state (location) we filter on, 
  #        filter[1] == second state we filter on
  #        filter[2] == start date we filter on 
  #        filter[3] == end date we filter on
  #        filter[4] == interval of time we filter on
  #        filter[5] == list of categories we will also filter on 
  #                     (inclusive - ie 3 categories includes more than 2 categories. 2 includes more than 1)
  
  while True:

    input = str(raw_input('Enter an action: '))
    print ''
    
    
    if input.strip().lower()[0:4] == 'help':
      print 'categories - search for categories: type categories followed by search queries \nseparated by commas. leave blank to return all categories\n'
      print 'states - search for states (in initials i.e. \'IL\' or \'QC\').\nleave blank to return all states\n - can search with cities or state initials'
      print 'set filter - set filter we apply to the data before we do statistics on it\n'
      print 'get filter - acquire the current filter\n'
      print 'go - return available statistics using the current filter\n'
      print 'exit - terminate the program\n'
    
    elif input.strip().lower()[0:10] == 'categories':
      a = input.strip()[11:].split(', ')
      cat_list = CategorySearch(a)
      
    elif input.strip().lower()[0:6] == 'states':
      b = input.strip()[7:].split(', ')
      StateSearch(b)
    
    elif input.strip().lower()[0:11] == 'set filter':
      filter = SetFilter()
      print ''
      
    
    elif input.strip().lower()[0:11] == 'get filter':
    
      print 'State 1:', filter[0]
      print 'State 2:', filter[1] 
      print 'Start Date:', filter[2]
      print 'End Date:', filter[3]
      print 'Time Interval:', filter[4]
      print 'Categories:', filter[5], '\n'
      
    
    elif input.strip().lower()[0:4] == 'exit':
      print 'Goodbye for now. See you soon.'
      break
    
    elif input.strip().lower()[0:2] == 'go':    
      GenData(filter)
    else:
      print 'Invalid input. Type help to recieve information about available actions\n'

def SetFilter():
    '''
    set filter - set filter we apply to the data before we do statistics on it\n'
    '''
    st_1 = raw_input('Enter your first state: ').strip()
    st_2 = raw_input('Enter your second state: ').strip()
    strt_date = raw_input('Enter your start date (Feb 21 2010 Format: 02-21-2010): ').strip()
    end_date = raw_input('Enter your end date (Feb 21 2010 Format: 02-21-2010): ').strip()
    int = raw_input('Enter time interval (weekly, monthly, yearly): ' ).strip()
    
    while not (int in ['weekly', 'daily', 'monthly', 'yearly']):
      print 'Invalid time interval'
      int = raw_input('Enter time interval (weekly, daily, monthly, yearly): ' ).strip()
      
    cat_list = raw_input('Enter your categories: ').strip().split(', ')
      
    return [st_1, st_2, strt_date, end_date, int, cat_list]

def StateSearch(query):
  '''
  states - search for states (in initials i.e. 'IL' or 'QC\'). leave blank to return all states
  - can search with cities or state initials
  '''
  con = cx_Oracle.connect('yelp', 'yelp', 'xe') 
  cur = con.cursor()
   
  u = ''
  for subquery in query:
    u += "lower(city) ='" + subquery.lower() + "' or lower(state) ='" + subquery.lower() + "' or "
  
  v = "select distinct state from business where "  + u[:-4]
  
  file = open('output.txt', 'w')
  file.write(v)
  
  
  print 'SEARCH RESULTS:\n'
  i = 1
  for state in cur.execute(v):
    print i, state[0]
    i += 1
  if i ==1:
    print 'No Results Found.\n'
  else:
    print ''
    
  cur.close()
  con.close()
  
def CategorySearch(query): 
  con = cx_Oracle.connect('yelp', 'yelp', 'xe')
  cur = con.cursor()
  
  u = ''
  for subquery in query:
    u += "lower(category) like '%" + subquery.lower() + "%' or "
    
  v = "select distinct category from categories where " + u[:-4]
  #print v
  i = 1
  print 'SEARCH RESULTS:\n'
  for category in cur.execute(v):
    print i,category[0]
    i += 1
  if i == 1:
    print 'No Results Found\n'
  else:
    print ''
  
  cur.close()
  con.close()
  
def GenData(filter):
  '''
  'go - return available statistics using the current filter\n'
  '''
  con = cx_Oracle.connect('yelp', 'yelp', 'xe')
  cur = con.cursor()
  
  if '' in filter:
    print 'Incomplete filter'
    return

  strt_date = filter[2].split('-')
  end_date = filter[3].split('-')
  
  if len(strt_date) != 3 or len(end_date) != 3:
    print 'Invalid Date Format\n'
  elif len(strt_date[2]) != 4 or len(end_date[2]) != 4:
    print 'Invalid Date Format\n'
  elif int(strt_date[0]) < 1 or int(strt_date[0]) > 12 or int(end_date[0]) < 1 or int(end_date[0]) > 12:
    print 'Invalid Date Format\n'  
  
  
  c = []
  d = []
  
  dates = []
  '''
  ACQUIRE THE DATES TO CONSIDER
  '''
  if filter[4] == 'weekly':
    try:
      d1 = date(int(strt_date[2]), int(strt_date[0]), int(strt_date[1]))
      d2 = date(int(end_date[2]), int(end_date[0]), int(end_date[1]))
    
      delta = d2 - d1
      for i in range(delta.days):
        if i%7 == 0:
          a = str(d1 + td(days=i)).split('-')
          dates.append([a[2],a[1],a[0]] )
    except ValueError:
      print 'Invalid Date Format\n'
  
  if filter[4] == 'monthly':
    a1 = int(strt_date[0])
    a2 = int(strt_date[2])
    b1 = int(end_date[0])
    b2 = int(end_date[2])
       
    while a2 < b2:
      dates.append([strt_date[1], str(a1),str(a2)])
      a1 += 1
      if a1 > 12:
        a1 = 1
        a2 += 1
    
    while a1 < b1:
      a1 += 1
      dates.append([strt_date[1],str(a1),str(a2)])

  
  if filter[4] == 'yearly':
    a1 = int(strt_date[0])
    a2 = int(strt_date[2])
    b1 = int(end_date[0])
    b2 = int(end_date[2])
       
    while a2 < b2:
      dates.append([strt_date[1],strt_date[0],str(a2)])
      a2 += 1
    if a1 <= b1:
      dates.append([strt_date[1],strt_date[0],str(a2)])
  '''
  FIX THE DATES FOR SQL
  '''  
      
  dates2 = []
  for item in dates:
    if int(item[1]) == 1:
      item[1] = 'JAN'
    elif int(item[1]) == 2:
      item[1] = 'FEB'
    elif int(item[1]) == 3:
      item[1] = 'MAR'
    elif int(item[1]) == 4:
      item[1] = 'APR'
    elif int(item[1]) == 5:
      item[1] = 'MAY'
    elif int(item[1]) == 6:
      item[1] = 'JUN'
    elif int(item[1]) == 7:
      item[1] = 'JUL'
    elif int(item[1]) == 8:
      item[1] = 'AUG'
    elif int(item[1]) == 9:
     item[1] = 'SEP'
    elif int(item[1]) == 10:
      item[1] = 'OCT'
    elif int(item[1]) == 11:
      item[1] = 'NOV'
    elif int(item[1]) == 12:
      item[1] = 'DEC'
    
    dates2.append(str(item[0]) + '-' + item[1] + '-' + str(item[2]))
    
  dates = dates2
  '''
  QUERIES - run SQL queries. AVG and COUNT queries.
  '''
  r = ''  
  for item in filter[5]:
    r += "lower(category) = '" + item.lower() + "' or "    
  
  q = "SELECT COUNT(*) FROM REVIEW R, CATEGORIES C, BUSINESS B \n\
       WHERE  R.BUSINESS_ID = C.BUSINESS_ID AND C.BUSINESS_ID = B.BUSINESS_ID AND R.R_DATE >= '" + dates[0] + "'\n\
       AND R.R_DATE <= '" + dates[len(dates)-1] + "' AND STATE = '"
  
  
  s = q + filter[0] + "' AND " + r[:-4]
  t = q + filter[1] + "' AND " + r[:-4]
  
  
  review_total_1 = list(cur.execute(s))[0][0]
  review_total_2 = list(cur.execute(t))[0][0]
  
  for i in range(0, len(dates)-1):
    q = "SELECT COUNT(*), AVG(R.STARS) FROM REVIEW R, CATEGORIES C, BUSINESS B \n\
        WHERE R.BUSINESS_ID = C.BUSINESS_ID AND C.BUSINESS_ID = B.BUSINESS_ID AND R.R_DATE >= '" + dates[i] + "'\n\
        AND R.R_DATE <= '" + dates[i+1] + "' AND STATE = '" + filter[0] + "' AND " + r[:-4]
    c.append(list(cur.execute(q)))
     
    q = "SELECT COUNT(*), AVG(R.STARS) FROM REVIEW R, CATEGORIES C, BUSINESS B \n\
        WHERE R.BUSINESS_ID = C.BUSINESS_ID AND C.BUSINESS_ID = B.BUSINESS_ID AND R.R_DATE >= '" + dates[i] + "'\n\
        AND R.R_DATE <= '" + dates[i+1] + "' AND STATE = '" + filter[1] + "' AND " + r[:-4]
    d.append(list(cur.execute(q)))
      
      
  print(filter[0])
  for i in range(len(dates)-1):
    print 'Date Range: ' + dates[i] + ' ' + dates[i+1] 
    if review_total_1 > 0:
      print 'Review Density: ' + str(c[i][0][0]/ float(review_total_1))
    else:
      print 'Review Density: 0'
    print 'Average Review: ' + str(c[i][0][1])
    print ''
  
  print(filter[1])
  for i in range(len(dates)-1):
    print 'Date Range: ' + dates[i] + ' ' + dates[i+1]
    if review_total_2 > 0:
      print 'Review Density: ' + str(d[i][0][0]/ float(review_total_2))
    else:
      print 'Review Density: 0'
    print 'Average Review: ' + str(d[i][0][1])    
    print ''    
  cur.close()
  con.close()
  
Main()