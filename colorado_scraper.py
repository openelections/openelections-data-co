from bs4 import BeautifulSoup
import urllib2
import re
import csv
import unicodedata

# pass this function the year you want to scrape, a dummy to indicate general election (1) 
# or primary (0), and a list of offices as they are displayed on the page (capitalization
# doesn't have to be right but everything else does). For example:
# scrape_election(2014,1,['united states senator','representatives to the 114th united
# states congress','governor/lieutenant governor','secretary of state','state treasurer',
# 'attorney general','state senate','state representative'])

# it's a little trickier with primaries because instead of being organized by
# race they are organized by party. Moreover, tables are structured a bit differently,
# with a county column, candidate columns, then total column.
def scrape_election(year,general,list_of_offices,outfile):
	list_of_offices=[item.lower() for item in list_of_offices]
	master_data=[['county','office','district','party','candidate','votes']]

	if general==1:
		etype='general'
	else:
		etype='primary'

	url='http://www.sos.state.co.us/pubs/elections/Results/Abstract/%s/%s/index.html' % (str(year),etype)
	temp=urllib2.urlopen(url).read()
	soup=BeautifulSoup(temp,'html.parser')

	elec_links=soup.find_all('a')

	for link in elec_links:

		if general==0:
			if 'party ballot' in link.text.lower():
				url='http://www.sos.state.co.us/pubs/elections/Results/Abstract/%s/%s/%s' % (str(year),etype,link.attrs['href'])
				print url
				source=urllib2.urlopen(url).read()
				party_soup=BeautifulSoup(source,'html.parser')
				select=party_soup.find_all('select')
				options=select[0].find_all('option')

				for option in options:
					if option.text.lower() in list_of_offices:
						url='http://www.sos.state.co.us%s' % (option['value'])
						office_temp=urllib2.urlopen(url).read()
						office_soup=BeautifulSoup(office_temp,'html.parser')
						tables=office_soup.find_all('table')

						district_finder=re.compile('(District [0-9]{1,2})')
						districts=district_finder.findall(office_temp)
						print districts

						for i,table in enumerate(tables[:-1]):
							tdata=parse_table(i,table)

							# district is the number of the table you are looking at, unless there is only one table, in which case omit district
							try:
								district=districts[i-1]
							except:
								district=''

							# tdata is one table with columns:
							# county, registered voters, ballots cast, candidate1, candidate2, ... , total, turnout%
							# needs to be converted to:
							# county, office, district, party, candidate, votes
							office=option.text
							for row in tdata[1:-1]:
								print row
								county=row[0]
								for i, column in enumerate(row[1:]):
									print tdata[0],i
									party_finder=re.compile('\((...)\)')
									try:
										party=party_finder.findall(tdata[0][i+1])[0]
									except:
										party=''
									candidate_finder=re.compile('(.*?) \(')
									try:
										candidate=candidate_finder.findall(tdata[0][i+1])[0]
									except:
										candidate=tdata[0][i+1]
									candidate=unicodedata.normalize('NFKD',candidate).encode('ascii','replace').replace('?','')
									if candidate=='Total':
										candidate=''
									votes=int(row[i+1].replace(',',''))
									master_data.append([county,office,district,party,candidate,votes])					

		elif general==1:
			if link.text.lower() in list_of_offices:
				url='http://www.sos.state.co.us/pubs/elections/Results/Abstract/%s/%s/%s' % (str(year),etype,link.attrs['href'])
				print url
				office_temp=urllib2.urlopen(url).read()
				office_soup=BeautifulSoup(office_temp,'html.parser')
				tables=office_soup.find_all('table')

				district_finder=re.compile('(District [0-9]{1,2})')
				districts=district_finder.findall(office_temp)
				print districts

				for i,table in enumerate(tables[1:]):
					tdata=parse_table(i,table)

					# district is the number of the table you are looking at, unless there is only one table, in which case omit district
					try:
						district=districts[i]
					except:
						district=''

					# tdata is one table with columns:
					# county, registered voters, ballots cast, candidate1, candidate2, ... , total, turnout%
					# needs to be converted to:
					# county, office, district, party, candidate, votes
					office=link.text
					for row in tdata[1:-1]:
						print row
						county=row[0]
						for i, column in enumerate(row[3:-1]):
							print tdata[0],i
							party_finder=re.compile('\((...)\)')
							try:
								party=party_finder.findall(tdata[0][i+3])[0]
							except:
								party=''
							candidate_finder=re.compile('(.*?) \(')
							try:
								candidate=candidate_finder.findall(tdata[0][i+3])[0]
							except:
								candidate=tdata[0][i+3]
							candidate=unicodedata.normalize('NFKD',candidate).encode('ascii','replace').replace('?','')
							if candidate=='Total':
								candidate=''
							votes=int(row[i+3].replace(',',''))
							master_data.append([county,office,district,party,candidate,votes])

	with open(outfile,'wb') as csvfile:
		writer=csv.writer(csvfile)
		for row in master_data:
			print row
			writer.writerow(row)

def parse_table(i,table):
	# thanks http://stackoverflow.com/a/23377804/3001940 for this table parsing code for bs4
	tdata=[]
	tbody=table.find('tbody')
	rows=tbody.find_all('tr')

	headers=rows[0].find_all('th')
	headers=[ele.text.strip().replace('\n','') for ele in headers]
	tdata.append([ele for ele in headers if ele])

	for row in rows[1:]:
		cols=row.find_all('td')
		cols=[ele.text.strip() for ele in cols]
		tdata.append([ele for ele in cols if ele])

	return tdata

