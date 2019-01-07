# PON_Migration
This script will collect ONTs configuration form a list provided by the user and give the commands needed to shift them to a new PON.
the user needs to provide the following:
1. Host IP address with the option -H
2. List of ONTs with option -O
3. Target PON in the format 1/1/1/1 with the option -NEWPON
4. User name with the option -U
5. Password with the option -P
6. List of TL1 output for passwords of SIP with the option -SIP

## The output.
The script will connect the device, collect all the ONTs listed configuraiton. 
Then it will generate three files:
* Original ONTs Commands of the source PON.
* Target PON ONTs configuraiton commands. ( It will also provide you at the beginning of this file a list of commands which you need to delete cross-connect bridge ports form the OLD ONTs so that you do not get error during the creation of the new ONTs ( cross-connect vlans can't be created under more than one port) 
* Commands to delete the OLD ONTs configuration.