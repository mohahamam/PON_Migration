import csv
# inputconfig = 'Orig_PON_10.33.72.14_1-1-3-6_2018-11-25-09-19-54.txt'
# pass_list = 'sip_passwords.csv'
# result = 'resultWithPass.txt'
	

def origConfigwithPass (inputfile,sip_pass,outputfile):
		
	def find_between(s, start, end):
		  return (s.split(start))[1].split(end)[0]

	def find(potsportnum, password, infile, outfile):
		with open(infile,'r') as a, open(outfile, 'w') as b:
			for line in a:
				if potsportnum in line:
					with open(sip_pass,'r') as f:
						csv_f = csv.reader(f)
						for row in csv_f:
							if str(row[0])==(find_between(line, 'voice-sip-port ', ' ')):
								b.write(line.replace((find_between(line, 'password plain:', ' ')),str(row[2])))				
				else:
					b.write(line)


	find('voice-sip-port ',  'password plain:',inputfile , outputfile)	

#origConfigwithPass (inputconfig,pass_list,result)