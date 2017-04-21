import csv

statewide_offices = ['President/Vice President', 'United States Senator', 'Supreme Court', 'Court of Appeals']
district_offices = ['United States Representative', 'State Board of Education', 'Regent of the University of Colorado', 'State Senate', 'State Representative', 'District Attorney', 'Regional Transportation District']

results = []

with open('2016GEstatewideAbstractResults.csv', 'rU') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if any(office in row['OFFICE / BALLOT ISSUE'] for office in statewide_offices):
            results.append([row['COUNTY'], row['OFFICE / BALLOT ISSUE'], None, row['PARTY'], row['CANDIDATE / BALLOT ISSUE TITLE'].replace(' TOTAL', ''), row['YES VOTES'].replace(',','')])
        elif any(office in row['OFFICE / BALLOT ISSUE'] for office in district_offices):
            o, d = row['OFFICE / BALLOT ISSUE'].split(' - ')
            d = d.replace('District ', '').strip()
            results.append([row['COUNTY'], o, d, row['PARTY'], row['CANDIDATE / BALLOT ISSUE TITLE'].replace(' TOTAL', ''), row['YES VOTES'].replace(',','')])
        else:
            continue

with open('20161108__co__general.csv', 'wb') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(["county", "office", "district", "party", "candidate", "votes"])
    writer.writerows(results)
