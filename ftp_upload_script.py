import ftplib
import glob
import os
import time
import requests
from ftplib import FTP_TLS

host = "quandl.brickftp.com"
ftps = FTP_TLS(host)
ftps.prot_p() 
print (ftps.getwelcome())

try:
    print ("Logging in...")
    ftps.login("tricolor", "9v0$NkRUaM")
    file_header = "=\nnotify: arif.fatehi@yahoo.com\ntoken: 9kzPsYLWsnmrZ1xTENrX\n=\n"

    headers = {"x-amz-acl": "bucket-owner-full-control"}

    for input_file in glob.iglob("*.csv"):
        with file(input_file, 'r') as original:
            data = original.read()
        if file_header not in data:
            with file(input_file, 'w') as modified:
                modified.write(file_header + data)
    
        file_name = input_file
        print "Opening file:" + file_name
        fp = open (file_name,'rb')
        ftps.storbinary('STOR ' + file_name, fp)
        fp.close()
    ftps.close()
except Exception, e:  #you can specify type of Exception also
   print str(e)