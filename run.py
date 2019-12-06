import time, traceback
import sys
from ftntlib import FortiManagerJSON
from db_connector import get_ips

#These should be env vars.
ip='10.200.x.x'
user='webAPI'
pwd='1234567890'

def every(delay, task):
  next_time = time.time() + delay
  while True:
    time.sleep(max(0, next_time - time.time()))
    try:
      task()
    except Exception:
      traceback.print_exc()
      # in production code you might want to have this instead of course:
      # logger.exception("Problem while executing repetitive task.")
    # skip tasks if we are behind schedule:
    next_time += (time.time() - next_time) // delay * delay + delay

def db_to_firewall():
  connect_to_firewall(get_ips("blocked_ips"), "block", "push")
  connect_to_firewall(get_ips("unblock_ips"), "unblock", "push")

def connect_to_firewall(objip,reqtype,push=None):  
  addrgrp = 'Block_SSH'
  package = 'Edge/edge-fw_ITS_Link'
  adom = '54Devices'
  urlpf = 'pm/config/adom/'+adom
  api = FortiManagerJSON()
  api.debug('on')
  api.login(ip,user,pwd)
  objname = 'h_'+objip
  if reqtype == "block":
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
  elif reqtype == "unblock":
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
  else:
    print("log error")
    
every(600, db_to_firewall)
