import time
def canweproceed():
	answer = input('Are the above inputs correct? (Yes,No):')

	if answer.lower()=='yes':
		print('Proceeding to Next Steps....')
		time.sleep(0.5)
		pass
	elif answer.lower()=='y':
		print('Proceeding to Next Steps....')
		time.sleep(0.5)
		pass
	else:
		print('You have chosen ',answer)
		print('Quitting...')
		time.sleep(0.25)
		exit()
