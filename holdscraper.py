from lxml import html
import requests
import numpy as np
import unidecode
import scipy.io
import time

def fonttonumber(grade):
	if len(grade)==1:
		grade=grade[0].upper()
	else:
		grade=0
	if   grade == '6A':
		grade = 1
	elif grade == '6A+':
		grade = 2
	elif grade == '6B':
		grade = 3
	elif grade == '6B+':
		grade = 4
	elif grade == '6C':
		grade = 5
	elif grade == '6C+':
		grade = 6
	elif grade == '7A':
		grade = 7
	elif grade == "7A+":
		grade = 8
	elif grade == "7B":
		grade = 9
	elif grade == "7B+":
		grade = 10
	elif grade == "7C":
		grade = 11
	elif grade == "7C+":
		grade = 12
	elif grade == "8A":
		grade = 13
	elif grade == "8A+":
		grade = 14
	elif grade == "8B":
		grade = 15
	elif grade == "8B+":
		grade = 16

	return grade

def holdlisttomatrix(holdlist):
	matrix = np.zeros((18,11)) # Dimensions of a full moonboard
	for hold in holdlist:
		row    = 18-int(hold[0][1:])          
		column = ord(hold[0][0])-65        
		matrix[row][column]=1
	return matrix

def main():
	matrices=np.zeros((18,11))
	grades = []

	names = np.load('/home/michael/Documents/moonboard/names.npy')       # numpy array containing list of problem names

	i=9000
	while i < xrange(len(names)):
		matrixfile = open('/home/michael/Documents/moonboard/matrices.txt', 'ab')
		gradefile  = open('/home/michael/Documents/moonboard/grades.txt',   'ab')

		name=names[i]
		urlname = name.replace(" ","-").replace("#","") 				 # trims non-url friendly characters, ie ' ' and '#'
		urlname = unidecode.unidecode(urlname)           				 # replaces accented characters with non-accented
		urlname =  ''.join([j if ord(j) < 128 else '' for j in urlname]) # removes any non ascii characters, IE emojis... 

		time.sleep(0.5)
		page = requests.get('https://www.moonboard.com/problems/'+urlname)
		
		if page.status_code == requests.codes.ok:
			tree = html.fromstring(page.content)
			
			# Get problem grade
			path   = "//*[@id='font_grade']"
			grade = tree.xpath(path+'/text()')   # font grade
			numgrade = fonttonumber(grade)       # raw number grade, see above fn to convert

			# Get start holds
			startholds = []
			for sholds in xrange(1,3):
				path   = "//*[@id='SH"+str(sholds)+"']"
				shold = tree.xpath(path+'/text()')
				if len(shold)!=0:
					startholds.append(shold)

			# Get intermediate holds
			intermediateholds = []
			for iholds in xrange(1,15):
				path   = "//*[@id='IH"+str(iholds)+"']"
				ihold = tree.xpath(path+'/text()')
				if len(ihold)!=0:
					intermediateholds.append(ihold)

			# Get finish holds
			finishholds = []
			for fholds in xrange(1,2):
				path   = "//*[@id='FH"+str(fholds)+"']"
				fhold = tree.xpath(path+'/text()')
				if len(fhold)!=0:
					finishholds.append(fhold)

			# Only save non-empty arrays (empty arrays caused by failed url friendly formatting)
			if len(startholds)!=0 and len(intermediateholds)!=0 and len(finishholds)!=0:
				holds       = startholds+intermediateholds+finishholds
				holdmatrix  = holdlisttomatrix(holds)
				print  name, grade, '\n','		', holds, i
				# grades.append(numgrade)
				# matrices = np.vstack((matrices, holdmatrix))

				np.savetxt(matrixfile, holdmatrix.astype(int), fmt='%i', newline='\n')
				np.savetxt(gradefile, [numgrade], fmt='%i')	
				matrixfile.close()
				gradefile.close()
		i+=1


if __name__=="__main__":
	main()