import os

if __name__ == '__main__':
	os.system('python XYZ2LLH.py -i Data/Days/Narrabeen1/150319_030412.txt -o Data/Days/Narrabeen1/XYZ2LLH.csv')
	os.system('python Filter.py -i Data/Days/Narrabeen1/XYZ2LLH.csv -o Data/Days/Narrabeen1/Filtered.csv --minHeight 13.211 --maxHeight 43.211 --polygon Data/Common/polygon.txt ')
	os.system('python Reproject.py -i Data/Days/Narrabeen1/Filtered.csv -o Data/Days/Narrabeen1/UTM.csv --epsgCode epsg:32756')

	os.system('python XYZ2LLH.py -i Data/Days/Narrabeen2/150319_030852.txt -o Data/Days/Narrabeen2/XYZ2LLH.csv')
	os.system('python Filter.py -i Data/Days/Narrabeen2/XYZ2LLH.csv -o Data/Days/Narrabeen2/Filtered.csv --minHeight 13.211 --maxHeight 43.211 --polygon Data/Common/polygon.txt ')
	os.system('python Reproject.py -i Data/Days/Narrabeen2/Filtered.csv -o Data/Days/Narrabeen2/UTM.csv --epsgCode epsg:32756')

	os.system('python XYZ2LLH.py -i Data/Days/Narrabeen3/150319_031335.txt -o Data/Days/Narrabeen3/XYZ2LLH.csv')
	os.system('python Filter.py -i Data/Days/Narrabeen3/XYZ2LLH.csv -o Data/Days/Narrabeen3/Filtered.csv --minHeight 13.211 --maxHeight 43.211 --polygon Data/Common/polygon.txt ')
	os.system('python Reproject.py -i Data/Days/Narrabeen3/Filtered.csv -o Data/Days/Narrabeen3/UTM.csv --epsgCode epsg:32756')