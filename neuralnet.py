import sys
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing   import StandardScaler
from sklearn.neural_network  import MLPClassifier
from sklearn.metrics         import classification_report,confusion_matrix

def loaddata():
	global rows, cols, nholds
	global low_grade, high_grade

	# Load data
	loaddata   = np.loadtxt("/home/michael/Documents/Code/Python/moonboard/climbs.txt")
	grades     = np.loadtxt("/home/michael/Documents/Code/Python/moonboard/grades.txt")
	nproblems  = np.shape(grades)[0]

	# Checks to ensure there are as many problems as grades
	if np.shape(loaddata)[0]/rows != nproblems:
		print >> sys.stderr, 'Mismatch with number of problems and number of grades!'
		sys.exit()

	# Reshapes data into (nproblems) vectors of length (1, nholds)
	data = []
	for i in xrange(nproblems):
		problemi = loaddata[i*rows:(i+1)*rows][:].reshape(1,nholds)[0].tolist()
		if grades[i] >=low_grade and grades[i]<=high_grade: # Only look at problems in some range
			data.append(problemi)

	# Remove the grades outside of the range of interest, but preserve the order!!!
	grades = filter(lambda x: low_grade<=x<=high_grade, grades.tolist())

	return data, grades

def main():
	global rows, cols, nholds
	global low_grade, high_grade

	# Moonboard parameters
	rows   = 18
	cols   = 11
	nholds = rows*cols

	# Grade range of interest
	low_grade  = 4
	high_grade = 13

	# Load data
	X, Y = loaddata()

	# Train the data
	X_train, X_test, Y_train, Y_test = train_test_split(X, Y)

	# Normalize data
	scaler  = StandardScaler()
	scaler.fit(X_train)
	X_train = scaler.transform(X_train)
	X_test  = scaler.transform(X_test )

	# Initializes the Multi-Layer Perceptron
	mlp = MLPClassifier(hidden_layer_sizes=(nholds,)*3)

	# Fits training data to the model
	mlp.fit(X_train, Y_train)

	# Makes predictions
	predictions = mlp.predict(X_test)

	# Performance checks
	print confusion_matrix(Y_test, predictions)
	print classification_report(Y_test, predictions)

if __name__=="__main__":
	main()
