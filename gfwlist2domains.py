#!/usr/bin/env python  
#coding=utf-8
 
import urllib.request
import re
import base64
import os

# file settings
tmpfile = 'gfwlist.tmp'
outfile = 'gfwlist_domains.txt'
# the url of gfwlist
baseurl = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'
# match comments/title/whitelist/ip address
comment_pattern = '^\!|\[|^@@|^\d+\.\d+\.\d+\.\d+'
domain_pattern = '([\w\-\_]+\.[\w\.\-\_]+)[\/\*]*' 

print('fetching list...')
content = base64.b64decode(urllib.request.urlopen(baseurl, timeout=15).read()).decode()

# write the decoded content to file then read line by line
tfs = open(tmpfile, 'w')
tfs.write(content)
tfs.close()
tfs = open(tmpfile, 'r')

print('page content fetched, analysis...')

# remember all blocked domains, in case of duplicate records
domainlist = []
fs =  open(outfile, 'w')

for line in tfs.readlines():	
	if not re.findall(comment_pattern, line):
		domain = re.findall(domain_pattern, line)
		if domain:
			try:
				found = domainlist.index(domain[0])
			except ValueError:
				print('saving %s' % domain[0])
				domainlist.append(domain[0])
				fs.write('%s\n' % domain[0])
					
tfs.close()	
fs.close();
os.remove(tmpfile)
 
print('Done!')