#imports:
import netmiko,os,sys,arrow,argparse,time,re
sys.path.insert(0, 'modules')
from inputfromuser import canweproceed
from CleanNetmico import strip_ansi_escape_codes
from extract_pass import get_pass
from sub_pass import origConfigwithPass

# Handling the inputs to the file:
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='''
	This Script will run commands form commands file "-C commands_file "
	and will run them on the NE you specify in the -H host name
	You need to provide username with option "-U username"
	Yeu need to provide password with option "-P password"
	It is possible to chose if you wish to see the commands running in the shell by chosing -V Yes''' )
	parser.add_argument("-H", help="Mandatory Provide the Host IP address")
	parser.add_argument("-O", help="Mandatory Input the List of ONTs you wish to Shift to a new PON")
	parser.add_argument("-newpon", help="Mandatory Provide the New pon you wish to shift the ONTs to for example 1/1/10/12")
	parser.add_argument("-V", help="Do you want to see the commands being running ? select Yes ?")
	parser.add_argument("-U", help="Mandatory Username of the NE")
	parser.add_argument("-P", help="Mandatory Password of the NE")
	parser.add_argument("-SIP", help="TL1 commands output file with SIP passwords")
	
args = parser.parse_args()
hostname=(args.H)
ONTsfilename=(args.O)
ToPon=(args.newpon)
Verbose=(args.V)
Username=(args.U)
Password=(args.P)
SipPasswordFile = (args.SIP)

os.system('cls' if os.name == 'nt' else 'clear')

###Check the inputs form the user are all correct and prompt him to continue if all OK
mandatories ={'NE IP':hostname,'ONTs file name':ONTsfilename,'Target PON':ToPon,'NE Username':Username,'NE Password':Password,'SIP password File':SipPasswordFile}

print('List of inputs')
print('~'*79)
for key,val in mandatories.items():
	print (key+' = ',val)
	if val is None:
		print('!!!!!!!Erorr\nThe',key,'value should not be empty please re-enter the command with correct inputs for help use -h or --help')
		print('Quitting....')
		time.sleep(1)
		exit()
		
print('~'*79)

##Ask the user to check his inputs and prompt to proceed or not this is a module under modules directory.
if Verbose!="Yes":
	print('You have chosen not to display the commands on this console. \nYou did not give< -V Yes >in your command.\nEvery thing will work find but you wont see the commmands running')

canweproceed()

####Assign an output and log directory

outdir =os.path.join('outputfiles',hostname)
if not os.path.exists(outdir):
	os.makedirs(outdir)

logsdir =os.path.join(outdir,'logs/')
if not os.path.exists(logsdir):
	os.makedirs(logsdir)

def whichPON (ONTslist):
	print('ONTs to be shifted are:\n'+'~'*79)
	#global FromPon
	with open (ONTslist,'r') as f:
		FromPon =set()
		for line in f:
			if line !=('\n'):
				position = (line[0:int([i for i, a in enumerate(line) if a == '/'][3])])
				FromPon.add(position)
		if len(FromPon) >1 :
			print (('~'*79),'\nThe Source PONs you are looking to get the info of ONTs from are:',FromPon)
			print('\nError !!!! Total Number of <',len(FromPon),'> PONs were found in the ONTs list.\nNot All the ONTs are under the same PON.\nPlease check the ONTs list provided\nQuitting!!!!')
			time.sleep(1)
			exit()
		elif len(FromPon) ==1 :
			print (('~'*79),'\nThe Source PON you are looking to get the info of ONTs from is:',FromPon)
			print('\nGood :-) All ONTs are under the same PON.\nCreating a file to get thier Configuration\n'+'~'*79)
			time.sleep(1)
		elif len(FromPon) ==0 :
			print (('~'*79),'\nThe Source PONs you are looking to get the info of ONTs from are:',FromPon)
			print('\nError !!!! Total Number of <',len(FromPon),'> PONs were found in the ONTs list.\nPlease check the ONTs list file provided with the  ( -O )option \nQuitting!!!!')
			time.sleep(1)
			exit()
	return FromPon

###Run the ONTs check
FromPon=whichPON(ONTsfilename)
###covert the FromPon to a string making sure that it is a unique element in the set ( you could use FromPon = FromPon.pop() OR element = next(iter(myset))  ) but this way actually makes sure you do not have more than one element in your set.
(FromPon,) = FromPon
#Below Regex pattern verifies that the user have given the correct PONs addresses.

PONrule = '1/1/(1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16)/(1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16)$'

if re.search(PONrule,FromPon):
    pass
else:
	print(('\n\n')+('X!'*79),'\nMistake in the Sourcre PON address\nThe ONTs list should have correct ONTs address something like( 1/1/5/6/x )Check your ONTs list is having correct addresses')
	exit()
if re.search(PONrule,ToPon):
	pass
else:
	print(('\n\n')+('X!'*79),'\nMistake in the Target PON address\nYou Should give the correct Target PON address such as: -newpon 1/1/10/12')
	exit()

	
###Create a file that contains the info configure of the list of ONTs.
	
infoconfigONTsfilename = ('info_config_PON_'+hostname+'_'+FromPon.replace('/','-') +'_at_'+ arrow.now().format('YYYY-MM-DD-HH-mm-ss')+'.txt')
ONTToMove = 'ONTtoBeRetrived'
ONTMasterFile = 'modules/ONT_Master_Config.txt'
numberOfLines=0


	
with open (ONTsfilename,'r') as ontslist:
	for ONTAddress in ontslist:
		if ONTAddress == "\n":
			pass
		else:
			numberOfLines+=1
			with open (ONTMasterFile,'r') as inputfile:
				filedata = inputfile.read()
			filedata=filedata.replace(ONTToMove,ONTAddress.rstrip('\n'))
			with open (os.path.join(outdir,infoconfigONTsfilename),'a') as outputfile:
				outputfile.write('\n\n'+'#~'*10+'ONT number: '+ONTAddress.rstrip('\n')+'#~'*10+'\n\n')	
				outputfile.write(filedata)
			print('Creating ONT info configure for ONT: ',ONTAddress.rstrip('\n'))
	


############################### Create a file to delete OLD ONTs
ONT_Delete ='modules/ONT_Master_delete.txt'

deleteOldONTs = ('DeleteOldONTs_'+hostname+'_'+FromPon.replace('/','-') +'_at_'+ arrow.now().format('YYYY-MM-DD-HH-mm-ss')+'.txt')
with open (ONTsfilename,'r') as ontslist:
	for ONTAddress in ontslist:
		if ONTAddress == "\n":
			pass
		else:
			with open (ONT_Delete,'r') as inputfile:
				filedata = inputfile.read()
			filedata=filedata.replace(ONTToMove,ONTAddress.rstrip('\n'))
			with open (os.path.join(outdir,deleteOldONTs),'a') as outputfile:	
				outputfile.write(filedata)
			

			
			
			
print('\n\nA file created with info configure of above ONTs named:',infoconfigONTsfilename,'under the directory '+outdir)
print('\n\n Also A file created with commands to delete the above ONTs named:',deleteOldONTs,'under the directory '+outdir)
time.sleep(1)
print('~'*79)
print('Total Number of ONTs =',numberOfLines)
print('The PON you want to copy from is :', FromPon)
print('The PON you want to shift ONTs to is :', ToPon)
print('~'*79)
##Ask the user to check his inputs and prompt to proceed or not this is a module under modules directory.
if FromPon == ToPon:
	print('The source PON and the Target PON are the same!!\nThat does not make sence. Are you sure ?!!!!')
	for i in range(5):
		print('!')
		time.sleep(0.25)

canweproceed()


##############################Running the commands on the OLT #################################

OuTpUt01 = ('SessionLog_'+hostname+'_'+FromPon.replace('/','-') +'_at_'+ arrow.now().format('YYYY-MM-DD-HH-mm-ss')+'.txt')
os.system('cls' if os.name == 'nt' else 'clear')
netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                      netmiko.ssh_exception.NetMikoAuthenticationException)

try:
	print('~'*79)
	print('connecting to the device',hostname)
	connection = netmiko.ConnectHandler(ip=hostname,device_type='alcatel_sros',username=Username,password=Password)
	print('connection to ',hostname,'is successful',type(connection))
	with open (os.path.join(logsdir,OuTpUt01), 'w') as commandsin:
		commandsin.writelines('~'*79+('\n'))
		commandsin.writelines('#'*3+'Connecting to the Device IP ='+hostname+'#'*3+('\n'))
		commandsout =connection.send_config_from_file(config_file=os.path.join(outdir,infoconfigONTsfilename))
		if Verbose =='Yes':
			print(strip_ansi_escape_codes(commandsout.rstrip('\n')))
		commandsin.writelines(strip_ansi_escape_codes(commandsout.rstrip('\n')))
	
					
	connection.disconnect()

except netmiko_exceptions as e:
	print('Failed to connect to the hostname', hostname, e)
	print('Quitting...')
	exit()
except OSError as err:
	print('An error in the commands was observed please check your commands ',err)
	print('Quitting...')
	exit()
except Exception as e:
	print('An Unexpected error occured ')
	print (e.message, e.args)
	print('Quitting...')
	exit()


origONTsConfig=('Orig_PON'+'_'+hostname+'_' + FromPon.replace('/','-') +'_'+ arrow.now().format('YYYY-MM-DD-HH-mm-ss')+'.txt')

##### Creat a function to chose only configure lines and ignore other lines, add separator between each ONT configuration and for the voice service, add bridge port without starting with vlan-id to avoid rejections.

def find(substr, omit,separator, infile, outfile):
    with open(infile,'r') as a, open(outfile, 'w') as b:
    	for line in a:
		    if separator in line:
		        b.write('\n'+'#'+line)
		    elif omit in line:
		        continue
		    elif 'configure qos interface ont:' in line:
		        if ' scheduler-node name:' in line:
		            b.write(line.split(' ds-num-queue')[0]+'\n')
		    elif '/vuni vlan-id ' in line:
		    	b.write(line.split(' vlan-id ')[0]+'\n')
		    	b.write(line)	
		    elif line.startswith(substr):
		        b.write(line)
 
####Apply the function to get the output file and save it under the logs directory under the HOST ip directory 

find('configure','>','ONT number: ',os.path.join(logsdir,OuTpUt01),os.path.join(logsdir,origONTsConfig))



#######Extract SIP passwords and generate a file listing all the POTS ports with phone number and password for each POTS port.
get_pass(SipPasswordFile,os.path.join(logsdir,'listofPass'))


#######Substitue the *** stars in the password on the sip ports lines with the corresponding correct password.
origConfigwithPass (os.path.join(logsdir,origONTsConfig),os.path.join(logsdir,'listofPass'),os.path.join(outdir,'WithPass'+origONTsConfig))


print ('~'*79)
print('Sucess!!!!!!! \nThe output file has been created\n' + 'WithPass'+origONTsConfig)
print('You can find it under the directory '+outdir.rstrip('/')+'\n')


####A function to Modify the OLD PON configuraiton to the New PON configuration.

def Shifting(OldPon,NewPon,ONTConfig):
	global outputfilename
	outputfilename = ('Target_PON'+'_'+hostname+'_'+ NewPon.replace('/','-') +'_'+ arrow.now().format('YYYY-MM-DD-HH-mm-ss')+'.txt')

	with open (ONTConfig,'r') as config:
		filedata = config.read()
	filedata = filedata.replace(' '+OldPon,' '+NewPon)
	filedata = filedata.replace(':'+OldPon,':'+NewPon)


	with open (os.path.join(outdir,outputfilename),'a') as outputfile:
		outputfile.write(filedata)


Shifting(FromPon,ToPon,os.path.join(outdir,'WithPass'+origONTsConfig))

print('Sucess!!!!!!! \nThe output file has been created\n' + outputfilename)
print('You can find it under the directory '+outdir.rstrip('/')+'\n')

