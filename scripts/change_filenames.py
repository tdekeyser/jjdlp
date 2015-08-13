import os

directory = raw_input('Directory? \n')
replaceable_element = raw_input('Element to be replaced? \n')
new_element = raw_input('New element? \n')

for filename in os.listdir(directory):
	if str(replaceable_element) in filename:
		os.rename(filename, filename.replace(str(replaceable_element), str(new_element)))
		print 'Changed name of ', filename
