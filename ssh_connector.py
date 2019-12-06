import sys
from ftntlib import FortiManagerJSON

ip='10.200.x.x'
user='webAPI'
pwd='1234567890'

def _ban(argv):   
	me,objip,push = argv   
	addrgrp = 'Block_SSH'
	package = 'Edge/edge-fw_ITS_Link'
	adom = '54Devices'
	urlpf = 'pm/config/adom/'+adom 
	api = FortiManagerJSON()  
	api.debug('on')  
	api.login(ip,user,pwd)  
	
	objname = 'h_'+objip  
	obj = {		  
	    'name' : objname,		  
	    'type' : 'ipmask',		  
	    'color' : 13,		 
	    'subnet' : [objip,'255.255.255.255']		  
	}  
	api.add(urlpf+'/obj/firewall/address',obj)  
	
	code,d = api.get(urlpf+'/obj/firewall/addrgrp/'+addrgrp)  
	    
	if type(d['member']) is list:	 
		member = d['member']	 
	if objname not in member:	   
		member.append(objname)  
	else:	 
		member = [d['member'], objname]  
	data = {'member':member}  
	api.update(urlpf+'/obj/firewall/addrgrp/'+addrgrp,data)  
	
	if push == "push": 
		scope = [ {'name' : 'All_FortiGate'} ]  
		flags = ['install_chg','generate_rev'] 
		ret_code, response = api.install_package(adom,package,scope,flags)  
	api.logout()  
	api.debug('off')  
	return 

def _unban(argv):   
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

