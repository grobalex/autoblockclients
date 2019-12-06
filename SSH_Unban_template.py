#!/usr/bin/python3

ip='10.200.x.x'
user='webAPI'
pwd='1234567890'

import sys

if len(sys.argv) < 2: 
	print('Usage: '+sys.argv[0]+' <blocked IP>')  
	print('Used to remove given IP from SSH Block list on edge firewall')
	exit()

from ftntlib import FortiManagerJSON

def main(argv):   
	me,objip = argv   
	addrgrp = 'Block_SSH'
	package = 'Edge/edge-fw_ITS_Link'
	adom = '54Devices'
	urlpf = 'pm/config/adom/'+adom 
	api = FortiManagerJSON()  
	api.debug('on')  
	api.login(ip,user,pwd)  
	
	objname = 'h_'+objip  
	
	code,d = api.get(urlpf+'/obj/firewall/addrgrp/'+addrgrp)  
	    
	if type(d['member']) is list:
		member = d['member']	 
	if objname not in member:   
		print('Host is not in block group!')
		return
	else:	 
		member.remove(objname)
	data = {'member':member}  
	api.update(urlpf+'/obj/firewall/addrgrp/'+addrgrp,data)  

	scope = [ {'name' : 'All_FortiGate'} ]  
	flags = ['install_chg','generate_rev'] 
	ret_code, response = api.install_package(adom,package,scope,flags)  
	api.logout()  
	api.debug('off')  
	return 

if __name__ == "__main__":   
	 main(sys.argv) 

