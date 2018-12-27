import csv

def get_pass(func_inputfile,func_outputfile):

	open(func_outputfile, 'w').close()
	def find_between(s, start, end):
	  return (s.split(start))[1].split(end)[0]	  

	def find(substr, password, username,infile, outfile):
		with open(infile,'r') as a, open(outfile, 'w') as b:
			for line in a:
				if substr in line:
					b.write(str((find_between(line, 'ONTPOTS-', ':')+',')).replace('-','/'))
				if username in line:
					b.write(find_between(line, 'USERAOR=\\"', '\\",')+(','))
				if password in line:
					b.write(find_between(line, 'PASSWORD=\\"', '\\",')+'\n')		
	####Apply the function to get the output file    
	find('   "ONTPOTS-', 'PASSWORD=\\"', 'USERAOR=\\"',func_inputfile, func_outputfile)
	#####Create an output csv file with only the Numbers and passwords.
	with open(func_outputfile,'r') as f, open (func_outputfile+'.csv','w',newline='') as w:
		csv_f = csv.reader(f)
		csv_w = csv.writer(w)

		for row in csv_f:
			if (row[1])=='':
				pass
			elif (row[1])=='\n':
				pass
			else:
				csv_w.writerow(row)

#get_pass('TL1Commands_SIP_Pass.txt','sip_passwords')