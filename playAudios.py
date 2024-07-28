from playsound import playsound

def play_sound(path):
	'''play sound of different numbers'''
	directory,file=path.split('/')[0],path.split('/')[-1]
	num=file.split('.')[0]
	num=int(num)
	if num < 10:
		
		playsound(directory+'/'+f'{num}.mp3')
	elif num<20 and num>12:
		first=str(num)[0]
		second=str(num)[1]
		
		playsound(directory+'/'+f'{num}.mp3')

	elif (num % 10 == 0 ) and (num != 0) :
		first=str(num)[0]
		second=str(num)[1]
		
		playsound(directory+'/'+f'{num}.mp3')
	else:
		playsound(path)


