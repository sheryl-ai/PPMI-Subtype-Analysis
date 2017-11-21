#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def convert_month(date):
    time = list()
    for t in date:
        month, year = t.split('/')
        month = int(month)
        year = int(year[-2::])
        time.append(year*12 + month)
    return time
    
def convert_int(date):
    
    if '/' in date:
        month, year = date.split('/')
        month = int(month)
        year = int(year[-2::])
        new_date = year*12 + month
    elif '-' in date:
        if date.count('-') == 2:
            year, month, day = date.split('-')
            year = int(year[-2::])
            month = int(month)  
            new_date = year*12 + month          
    else:
        if date == 'static' or date == '':
            date = -1
        new_date = int(date)
    return new_date
       
def convert_time(date):
    new_date = date
    t_map = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06',
                'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}

    if len(date) == 10:
        year, month, day = date.split('-')
        new_date = month + '/' + year 
    else:
        if '-' in date:
            month, year = date.split('-')
            new_month = t_map[month]
            new_date = new_month + '/' + '20' + year
    return new_date

    
if __name__=='__main__':
    pass