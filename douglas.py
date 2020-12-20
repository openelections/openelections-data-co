import csv

source = '/Users/derekwillis/Downloads/2018 Douglas County, CO precinct-level election results.txt'
offices = ['Representative to the 116th US Congress', 'Governor', 'Secretary of State', 'State Treasurer', 'Attorney General', 'State Representative']

lines = open(source).readlines()
results = []

for line in lines:
    if line == '\n':
        continue
    if "ScanStations" in line:
        continue
    if "Cumulative" in line:
        continue
    if "General 2018" in line:
        continue
    if "Official Results" in line:
        continue
    if line[0:4] == 'Total':
        continue
    if "Vote %" in line:
        continue
    if "VOTES  PERCENT" in line:
        continue
    if any(o in line for o in offices):
        office = line.split('(Vote for 1)', 1)[0]
    if "Precinct" in line:
        precinct = line.strip()
    if "%" in line:
        # this is a result line
        candidate, party = line.split('  ', 3)[2].split(').')[0].split(' (')
        party = None
        candidate = candidate.strip()
        votes = line.split('    ', 3)[3].split('   ')[0].strip()
        results.append(['Beaver', precinct, office, None, party, candidate, votes])

with open('20181106__pa__general__beaver__precinct.csv', 'wt') as csvfile:
    w = csv.writer(csvfile)
    headers = ['county', 'precinct', 'office', 'district', 'party', 'candidate', 'votes']
    w.writerow(headers)
    w.writerows(results)
