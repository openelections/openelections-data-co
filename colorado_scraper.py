import bs4
import urllib2

# pass this function the year you want to scrape, a dummy to indicate general election (1) 
# or primary (0), and a list of offices as they are displayed on the page (capitalization
# doesn't have to be right but everything else does). For example:
# scrape_election(2014,1,['united states senator','representatives to the 114th united
# states congress','governor/lieutenant governor','secretary of state','state treasurer',
# 'attorney general','state senate','state representative'])
def scrape_election(year,general_flag,list_of_offices):
	if general==1:
		etype='general'
	else:
		etype='primary'

	url='http://www.sos.state.co.us/pubs/elections/Results/Abstract/%s/%s/index.html' % (str(year),etype)
