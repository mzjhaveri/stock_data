import urllib2
import datetime
import time
import os
import csv
import sys
from optparse import OptionParser



parser = OptionParser()
parser.set_defaults(var_give_date=False)
parser.add_option("--givedate","-g", action="store_true", dest="var_give_date")
(options, args) = parser.parse_args()


if options.var_give_date == False:
    Current_date = datetime.date.today()
    Current_date = Current_date.strftime('%d-%m-%Y')
    Prev_date = datetime.date.today()-datetime.timedelta(1)
    Prev_date = Prev_date.strftime('%d-%m-%Y')

else:
    print "Lets provide our own dates"
    Current_date = raw_input("Enter current date in dd-mm-yyyy format:  ")
    Prev_date = raw_input("Enter previous date in dd-mm-yyyy format:  ")

print "current date"
print Current_date     
print "previous date"
print Prev_date

 
firstline = True
with open('NIFTY_LIST_NEW.csv', 'rb') as f:
    reader = csv.reader(f)
    
	
    for row in reader:
        ticker = row[1]
		
        if  firstline:    #skip first line
            firstline = False
            continue
			
        
        ticker = ticker.replace('&','%26')

        url= "http://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/getHistoricalData.jsp?symbol=" + ticker + "&series=EQ&fromDate=" + Prev_date + "&toDate="+ Current_date +"&datePeriod=unselected&hiddDwnld=true"
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
			   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
			   'Accept-Encoding': 'none',
			   'Accept-Language': 'en-US,en;q=0.8',
			   'Connection': 'keep-alive'}
			   
        req = urllib2.Request(url, headers=hdr)
        print url
        try:
            data = urllib2.urlopen(req).readlines()
        except urllib2.HTTPError, e:
            print e.fp.read()
        
        #truncate and remove files till 'Data' is observed in line
        omit_line_count = 0
        for line in data:
          line = line.replace('\r', '\n')
          line = line.split(',')
          if line[0] == 'Date':
            break
          else:
            data[omit_line_count] = '\b'
          omit_line_count = omit_line_count +1


        print "omit_line_count"
        print omit_line_count
        print "data::"
        print data
        try:
          line = data[omit_line_count + 1]
        except IndexError:
          line = 'null'
          
        if line == 'null':
          print "There seems to be no data today, are you sure the market is open today?"
          sys.exit(0)
        
        
        filename="workfile"+ticker + Current_date+".csv"
        f = open(filename, 'w')

        print "code: "+ ticker
        f.write("code: "+ticker)
        f.write("\nsource_code: TC1")
        print("--")
        f.write("\n")
        f.write("--")
        f.write("\n")
        
        line_count=0
        remove_from = 1
        remove_to = 3
        for line in data:
          if line_count > omit_line_count:
            line = line.replace('\r', '\n')
            line = line.split(',')
            del line[remove_from:remove_to]
            line = ','.join(line)
            print line
            f.write(line)
            if options.var_give_date == False:
              break
          line_count = line_count + 1


	#cmd = "curl -T %s -X PUT -H 'x-amz-acl: bucket-owner-full-control' http://quandl-data-upload.s3.amazonaws.com/qdf/"%filename
	#cmd = "quandl upload "+ filename
	#time.sleep(1)
	#os.system(cmd)
	#print cmd