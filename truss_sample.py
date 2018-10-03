#!/usr/bin/python

import sys
import datetime
from dateutil.parser import *
import csv
import pytz
import dateutil.parser

def convertFBDuration(duration):
    split_time = duration.split(':')
    changeHoursToSeconds = float(split_time[0]) * 60 * 60
    changeMinutesToSeconds = float(split_time[1]) * 60
    totaltime = changeHoursToSeconds + changeMinutesToSeconds + float(split_time[2])
    return (totaltime)

def totalDuration(duration1, duration2):
    return(duration1 + duration2)

def zipcodeUpdate(zipcode):
    while(len(zipcode) < 5):
        zipcode= '0' + zipcode
    return (zipcode)

def changeToUpperCase(line):
    return(line.upper())

def getHeader(file):
    file = csv.reader(file)
    header = next(file)
    return(header)

def convertToISOEST(line):
    now = parse(line)
    time_in_iso = now.isoformat()
    x = dateutil.parser.parse(time_in_iso)
    tz = pytz.timezone('America/New_York')
    time_in_est = tz.localize(x)
    time_in_iso_est = time_in_est.isoformat()
    return (time_in_iso_est)


#the user input the csv file
new_file = []
all_data = []
inFile = sys.argv[1]
with open(inFile) as csv_file:
    f = csv.reader(csv_file, delimiter=',')
    header = getHeader(csv_file)
    for each_line in f:
        all_data.append(each_line)


#going through each line and replacing any invalid utf-8 character
for each_line in all_data:
    a= str(each_line[1])
    each_line[1] = a.decode("utf-8","replace").encode("utf-8")
    b = str(each_line[7])
    each_line[7]= b.decode("utf-8","replace").encode("utf-8")
    c = str(each_line[0])
    timestamp = convertToISOEST(c)
    timestamp = timestamp.decode("utf-8","replace").encode("utf-8")
    d= str(each_line[2])
    zipcode = zipcodeUpdate(d)
    zipcode = zipcode.decode("utf-8","replace").encode("utf-8")
    e = str(each_line[3])
    full_name = changeToUpperCase(e)
    full_name = full_name.decode("utf-8","replace").encode("utf-8")
    fb_dur = convertFBDuration(each_line[4])
    bd_dur = convertFBDuration(each_line[5])
    total_dur = totalDuration(fb_dur,bd_dur)
    # the '=' sign before zipcode is to make sure that the zeros before the number do not get truncated if opened up on csv
    row = str(timestamp) + "," + "\"" + each_line[1] + "\"" + "," + "=\"" + zipcode + "\"" +"," + str(full_name) + "," + str(fb_dur) + "," + str(bd_dur) + "," + str(total_dur) + "," + "\"" + each_line[7] + "\"" + "\n"
    #print row
    new_file.append(row)
        
#Writing the data to the normalized file
with open('normalized.csv', 'w') as fout:
    header = ','.join(header)
    header = header + "\n"
    fout.write(header)
    for row in new_file:
        fout.write(row)
        
