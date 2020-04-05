####### EXECUTION ##########
#takes only two arguments, ipfrom ipto 
#python management.py 192.168.104.100 192.168.104.150
############################

#modules for import
import socket
import subprocess
from pexpect import pxssh
import getpass
import colorama
from colorama import Fore, Style
import datetime
import sys
import os
import pandas as pd
import ipproc 

#ssh variables
user = "username"
prts = ["port1","port2"]
pswds = ["pswd1", "pswd2"]

#create dataframe for results
df=pd.DataFrame(columns=['IP','Hostname','Port','Pswd','Version','Mac','#Updates','#Security Updates'])

#check arguments
if len(sys.argv)!=3:
	print("Bad arguments: Give 2 ips: ipfrom ipto")
	exit(1)

#get ips from arguments
ipfrom=ipproc.IpAddress(sys.argv[1])
ipto=ipproc.IpAddress(sys.argv[2])

def getHost(address, pswd, prt):
#creates ssh connection with remote server
#returns hostname, available updates, ubuntu version, mac address
	s=pxssh.pxssh(timeout=5)
	try:
		s.login(server=address, username=user, password=pswd, port=prt, sync_multiplier=2, auto_prompt_reset=True,login_timeout=1)

		#get number of available updates
		s.sendline('/usr/lib/update-notifier/apt-check --human-readable')
		s.prompt()			# match the prompt
		a = s.before			# get everything before the prompt(in bytes)
		ups = a[51:].decode('utf-8')	# decode bytes to string
		nups=[int(s) for s in ups.split() if s.isdigit()]
		print("UPDATES:",nups[0]," SEC:",nups[1])
		
		#get hostname
		s.sendline('hostname')
		s.prompt()
		b = s.before
		name = b.decode('utf-8')

		#get ubuntu version
		s.sendline('lsb_release -sr')
		s.prompt()
		v=s.before
		ver=v[-7:].decode('utf-8')

		#get mac address
		if ver.strip()=="18.04":
			s.sendline('ifconfig | grep ether')
			s.prompt()
			m=s.before
			macaddr=m[53:71].decode('utf-8')
		else:
			s.sendline('ifconfig | grep HWaddr')
			s.prompt()
			m=s.before
			macaddr=m[-21:-4].decode('utf-8')

		#close connection
		s.logout()

		return name, ups, ver, macaddr, nups

	except pxssh.ExceptionPxssh as e:
		print(error)
		return e

#counter for connections
id=0

#scan network hosts from 1 to 255
while True:
	address=ipfrom.toStr()
	flag=False

	#ping address
	res = subprocess.call(['ping', '-c', '3', address])

	#if ping was successful
	if res == 0:
		print(Fore.GREEN+"ping to", address, "OK")
		print(Style.RESET_ALL)

		#try ssh with given passwords and given ports
		for n, pswd in enumerate(pswds):
			for prt in prts:
				try:
					#get details of address
					hostname, nups, ver, mac, dups=getHost(address, pswd, prt)
					flag=True
					hostn=hostname[10:].rstrip()
					sret = address+' '+hostn+' '+prt+' '+str(n) + ' ' +ver+ ' '+ mac + ' ' +nups + '\n'
					print(Fore.GREEN+hostn)
					print(Style.RESET_ALL)
				except:
					print("Could not ssh")
					continue

				if (flag==True):
					#write dataframe
					df.loc[id]=[address]+[hostn]+[prt]+[str(n)]+[ver]+[mac]+[dups[0]]+[dups[1]]
			
			
	#check ip from 
	if ipproc.IpAddress.Eq(ipfrom, ipto):
		break;

	#increment ip by 1
	ipfrom.Inc()

	#increment counter by 1
	id=id+1

#write dataframe to html
html=df.to_html()
textf=open("assets.html","w")
textf.write(html)
textf.close()
