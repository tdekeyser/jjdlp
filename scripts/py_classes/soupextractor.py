'''
SoupExtractor() takes as input the entire XML and returns a list of pages containing dictionaries with notes.

An example output looks like this:
	[
		{
			'notebpage': 'B.10.001',
			'page_list': [
							{
								'notejj0': '(a) 282 l 7 ff I dare him / and I doubledare him'
								'annotation': 'Note: Page and line references are to the first edition of (...)'
								'ctransfer': 'Transferred to: VI.C.5.092(a)'
								'msinfo': ''
								'source': 'Ulysses 1922, 282 [12.100-1]: I dare him, says he, and I doubledare him. (...)'
							},
							{
								'notejj0': '(b) 284 l 8 freely qfreckled'
								...
							},
							...
						]
		},
		{
			'notebpage': 'B.10.002',
			'page_list': [
							{...},
							{...},
							...
						]
		},
		...
	]

!!! SoupExtractor() relies on the tag definitions of the notebook XMLs. Other XMLs with other tags WILL NOT WORK !!!
'''

import re, sys
from bs4 import BeautifulSoup

def yes_no_question(question):
	valid = {'yes': True, 'y': True, 'no': False, 'n': False}

	while True:
		sys.stdout.write(question + '[y/n]')
		choice = raw_input().lower()
		if choice in valid:
			return valid[choice]
		else:
			sys.stdout.write("Please respond with 'yes' or 'no'.\n")

class SoupExtractor(object):
	page_tag = 'div'
	target_tag = 'div0'

	def __init__(self):
		self.xml_file = raw_input('Enter directory and name of the xml file:\n')
		if len(self.xml_file)< 1: self.xml_file = './jj_xml/testpage_B.10.xml'

		self.extract_all()

	def extract_all(self):
		'''Opens XML and iterates over all pages and returns a list of extracted pages'''

		xml_f = open(self.xml_file).read()
		souped_xml = BeautifulSoup(xml_f, "lxml")
		
		extr_n = []
		i = 0

		if yes_no_question('You wish to extract all files from ' + self.xml_file + '?'):
			print 'Extracting ', self.xml_file

			while i < (len(soup.find_all(self.page_tag))):
				extr_n.append(dict(self.npage_extractor(souped_xml, i)))
				i += 1

			print ' *** Notebook extraction finished. *** '
			return extr_n

		else:
			print ' *** Extraction stopped. *** '

	def extract(self, parsed_tag, target_tag, attr_name, attr_value):
		'''Extracts text from chosen tag with single attribute'''

		def regexsub_tag(string):
			'''Converts <hi rend="sup"> to <sup>'''
			x = re.compile(r'<(?!hi\srend=\"sup\").+?>')
			y = x.sub('', string)
			return re.sub(r'<.*?>([a-z])', r'<sup>\1</sup>', y)

		target_value = parsed_tag.find(target_tag, {attr_name: attr_value})

		if target_value:
			if re.search('rend="sup"', str(target_value)):
				return regexsub_tag(str(target_value).replace('\n', ' '))
			else:
				return target_value.text.replace('\n', ' ')
		else:
			return ''

	def npage_extractor(self, soup, p):
		'''Extracts info from all target tags and wraps them in a dictionary'''

		page_list = []
		note_dict = {}

		for div0 in soup.find_all(self.page_tag)[p].find_all(self.target_tag):
			# End of <div0> MUST immediately start with another opening <div>, or it will add an empty div0, leading to empty note lists.
			
			note_dict['notejj0'] = self.extract(div0, 'p', 'ana', 'NoteJJ0')
			note_dict['annotation'] = self.extract(div0, 'p', 'ana', 'Annotation')
			note_dict['ctransfer'] = self.extract(div0, 'p', 'ana', 'CTransfer')
			note_dict['msinfo'] = self.extract(div0, 'p', 'ana', 'MSinfo')
			note_dict['source'] = ' '.join(source_info.text.replace('\n', ' ') for source_info in div0.find_all('p', {'ana': 'Source1'} or {'ana': 'SourceVerse'}))

			page_list.append(dict(note_dict))

			if len(page_list) == (len(soup.find_all(self.page_tag)[p])-1):
				notebpage = re.findall(r'([A-Z][.]\d{1,2}[.]\d{3})', soup.find_all(self.page_tag)[p].contents[0])[0]
				print 'Extracted page %s' % (notebpage)

				return {
					'notebpage' : notebpage,
					'page_list' : page_list,
				}
