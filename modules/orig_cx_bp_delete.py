import re
### a function to find values between two patterns.
def find_between(s, start, end):
	  return (s.split(start))[1].split(end)[0]

expression = r'configure bridge port [\w/]+ vlan-id \d+'

def delete_corss_connect_bridge_ports(inputfile,outpufile,list1):
	###handling stacked vlans
	stackedvlanpattern=r'stacked:(\d+):(\d+)'
	list2 = re.findall(stackedvlanpattern,str(list1))
	list2 = sorted([list2[x][1] for x,i  in enumerate(list2) ])
#	print(list2)

	with open(inputfile,'r') as a, open (outpufile,'w') as b:
		for line in a:
			if ' pvid ' in line:
				if find_between(line,' pvid ', '\n') in list1:
					b.write(str(line).replace(' pvid ', ' no pvid '.rstrip('\s')+'#IPVPN VLAN '))
				elif find_between(line,' pvid ', '\n') in list2:
					b.write(str(line).replace(' pvid ', ' no pvid '.rstrip('\s')+'#Stacked VLAN '))


	with open(inputfile,'r') as a, open (outpufile,'a') as b:
		for line in a:
			if ' vlan-id ' in line:
				if find_between(line,' vlan-id ', ' ') in list1:
					b.write(str(re.match(expression, line).group(0).replace(' vlan-id ', ' no vlan-id '))+'\n')
				elif find_between(line,' vlan-id ', ' ') in list2:
					b.write(str(re.match(expression, line).group(0).replace(' vlan-id ', ' no vlan-id '))+'\n')


#bridgeports='vlans_lista.txt'
#ouputbrdigeports = 'delete_vlans_lista.txt'
#listofVlans = ['3003', '301', '302', '303', '304', '305', '306', '307', '308', '309', '310', '3101', '3102', '311', '3114', '3115', '3117', '3118', '312', '313', '314', '315', '316', '317', '318', '319', '320', '3205', '3206', '3207', '3208', '3209', '3210', '3211', '3212', '3213', '3214', '3215', '3220', '3222', '3223', '3228', '3229', '3231', '3232', '3235', '3236', '3237', '3238', '3239', '3241', '3242', '3246', '3247', '3300', '3305', '3306', '3307', '3308', '3309', '3310', '3311', '3312', '3313', '3314', '3315', '3322', '3323', '3334', '3339', '3340', '3342', '3343', '3345', '3346', '3347', '4000', '502', '504', '505', '507', '508', '510', '511', '513', '514', '516', '517', '522', '523', '531', '532', '534', '535', '537', '538', '540', '541', '543', '544', '546', '547', '549', '550', 'stacked:2400:250', 'stacked:2400:50', 'stacked:2400:56', 'stacked:2400:679', 'stacked:2400:680', 'stacked:2400:681', 'stacked:2400:682', 'stacked:2400:683', 'stacked:2400:684', 'stacked:2400:685', 'stacked:2400:686', 'stacked:2400:687', 'stacked:2400:688', 'stacked:2400:689', 'stacked:2400:690', 'stacked:2400:691', 'stacked:40:0', 'stacked:501:1101', 'stacked:678:678', 'stacked:678:679']

def Main():
	delete_corss_connect_bridge_ports(bridgeports, ouputbrdigeports, listofVlans)
if __name__=='__main__':
	Main()
	
