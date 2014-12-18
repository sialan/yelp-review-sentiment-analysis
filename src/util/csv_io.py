import csv


def csv_to_array(filename, header=False):
	"""Return a header and data array of a csv file.

	Args:
		filename (string): Complete file path including name of file
		header (boolean): Indicates the presence of data column labels
	Returns:
		header (array): Labels to the output data columns
		data (array): Delimited list of data
	"""
	data = []
	f = open(filename, 'rb')
	csv_reader_object = csv.reader(f)
	if header:
		header = csv_reader_object.next()
	else:
		header = []
	for row in csv_reader_object:
		data.append(row)
	f.close()
	return header, data

def array_to_csv(filename, output, header=None):
	"""Save a header and output array as a csv file.

	Args:
		filename (string): Complete file path including name of file
		output (array): Delimited list of data
		header (array): Labels to the output data columns
	"""
	f = open(filename, 'wb')
	csv_writer_object = csv.writer(f)
	if header:
		csv_writer_object.writerow(header)
	for row in output:
		# csv_writer_object.writerow([x.encode('utf-8') for x in row])
		csv_writer_object.writerow(row)
	f.close()