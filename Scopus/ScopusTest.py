from pybliometrics.scopus import ScopusSearch
    
s = ScopusSearch('ISSN(1532-849X) AND PUBYEAR IS 2010',view="COMPLETE", subscriber=True)
# need authorization

dump = open("RawDataTests/ScopusDump.txt", 'w')
dump.write(str(s.results))
