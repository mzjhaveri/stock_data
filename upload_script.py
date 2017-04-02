import glob
import os
import time
import requests

file_header = "=\nnotify: arif.fatehi@yahoo.com\ntoken: 9kzPsYLWsnmrZ1xTENrX\n=\n"

headers = {"x-amz-acl": "bucket-owner-full-control"}

for input_file in glob.iglob("*.csv"):
    
    with file(input_file, 'r') as original:
        data = original.read()
        if file_header not in data:
            with file(input_file, 'w') as modified:
                modified.write(file_header + data)
    
        file_name = input_file
        url = "http://quandl-data-upload.s3.amazonaws.com/qdf/%s" %file_name
        with open(file_name) as f:
            mydata = f.read()
            print file_name
#response = requests.put(url, data=mydata, headers=headers, params={"file": file_name})