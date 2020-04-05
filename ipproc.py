#module for handling ip addresses
#ip address is of the for X.Y.Z.W

import sys

class IpAddress:	
	#class for representing an ip address
	
	#constructor ip = X.Y.Z.W
	def __init__(self, ip):
		l=[self.X, self.Y, self.Z, self.W] = ip.split('.')
		for i in l:
			IpAddress.Check_Trip(i) 

	#function that checks if a trilet is in range 1-255
	def Check_Trip(t):
		if not 0<int(t)<=255:
			raise Exception('triplet should be in range 1-255') 
	
	#function that increments ip by 1
	def Inc(self):	
		if int(self.W)<255:
			temp=int(self.W)
			temp=temp+1
			self.W=str(temp)
		else:
			temp=int(self.Z)
			temp=temp+1
			self.Z=str(temp)

			self.W=str(1)

	#function that returns ip in form of string
	def toStr(self):
		return self.X+'.'+self.Y+'.'+self.Z+'.'+self.W

	#function that prints the ip
	def Print(self):
		print(self.X, self.Y, self.Z, self.W)

	#function to check equality between two ip addresses
	def Eq(ip1, ip2):
		if ip1.X==ip2.X and  ip1.Y==ip2.Y and  ip1.Z==ip2.Z and  ip1.W==ip2.W:
			return True
 
#test code
#ipfrom=IpAddress(sys.argv[1])
#ipfrom.Print()
#ipto = IpAddress(sys.argv[2])

#while True:
#	ipfrom.Inc()
#	ipfrom.Print()
#	if IpAddress.Eq(ipfrom, ipto): 
#		break
