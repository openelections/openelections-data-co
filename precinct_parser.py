import csv

statewide_offices = ['President/Vice President', 'United States Senator', 'Supreme Court', 'Court of Appeals']
district_offices = ['United States Representative', 'State Board of Education', 'Regent of the University of Colorado', 'State Senate', 'State Representative', 'District Attorney', 'Regional Transportation District']

results = []

with open('2016GeneralResultsPrecinctLevel.csv', 'rU') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if any(office in row['Office/Issue/Judgeship'] for office in statewide_offices):
            results.append([row['County'], row['Precinct'], row['Office/Issue/Judgeship'], None, row['Party'], row['Candidate'].replace(' TOTAL', ''), row['Candidate Votes'].replace(',','')])
        elif any(office in row['Office/Issue/Judgeship'] for office in district_offices):
            o, d = row['Office/Issue/Judgeship'].split(' - ')
            d = d.replace('District ', '').strip()
            results.append([row['County'], row['Precinct'], o, d, row['Party'], row['Candidate'].replace(' TOTAL', ''), row['Candidate Votes'].replace(',','')])
        else:
            continue

with open('20161108__co__general__precinct.csv', 'wb') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(["county", "precinct", "office", "district", "party", "candidate", "votes"])
    writer.writerows(results)
