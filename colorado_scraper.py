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
				# district is the number of the table you are looking at, unless there is only one table, in which case omit district
				# could there ever be a special case where a district is missing, screwing up the numbering? I don't see how...
				try:
					district=districts[i]
				except:
					district=''

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

				# tdata is one table with columns:
				# county, registered voters, ballots cast, candidate1, candidate2, ... , total, turnout%
				# needs to be converted to:
				# county, office, district, party, candidate, votes
				office=link.text
				for row in tdata[1:-1]:
					print row
					county=row[0]
					for i, column in enumerate(row[3:-2]):
						party_finder=re.compile('\((...)\)')
						party=party_finder.findall(tdata[0][i+3])[0]
						candidate_finder=re.compile('(.*?) \(')
						candidate=candidate_finder.findall(tdata[0][i+3])[0]
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

