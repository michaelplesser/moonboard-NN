from lxml import html
import requests
import numpy as np

def main():
	page = requests.get('https://www.moonboard.com/problems/')
	tree = html.fromstring(page.content)
	problemnames = []
	for j in xrange(1,12602):
		path = '//html/body/div/div[3]/div/div[2]/div/div[4]/div[2]/div[2]/div['+str(j)+']/a/text()'
		problemi = tree.xpath(path)
		for i in xrange(len(problemi)): 
			problemi[i] = problemi[i].strip() # [name, set by, grade, '']
		problemnames.append(problemi[0]) 
		print problemi[0]
	names = np.array(problemnames)
	np.save('/home/michael/Documents/moonboard/names', names) # saves an array containing all problem names

if __name__=="__main__":
	main()