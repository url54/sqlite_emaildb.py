# This program was created as part of an assignment.  The assignment was to search through
# a text file for all the different domains used in all the emails in this text file. Then create
# a database to house all the different domains and add counts to the number of times they show
# up in the file. Below is actual instructions for this assignment and attached to this repository
# is the mbox.txt file.

# This application will read the mailbox data (mbox.txt) and count the number of email messages per organization (i.e. domain name of the email address)
# using a database with the following schema to maintain the counts. CREATE TABLE Counts (org TEXT, count INTEGER)
# When you have run the program on mbox.txt upload the resulting database file above for grading.
# The data file for this application is the same as in previous assignments: http://www.py4e.com/code3/mbox.txt.
# Because the sample code is using an UPDATE statement and committing the results to the database as each record is
#  read in the loop, it might take as long as a few minutes to process all the data. The commit insists on completely
# writing all the data to disk every time it is called. 

import sqlite3

conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')

cur.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''')

fname = input('Enter file name: ')
if (len(fname) < 1): fname = 'mbox.txt'
fh = open(fname)
for line in fh:
    if not line.startswith('From: '): continue
    pieces = line.split()
    orgs = pieces[1]
    dmns = orgs.split('@')
    org = dmns[1]
    cur.execute('SELECT count FROM Counts WHERE org = ? ', (org,))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Counts (org, count)
                VALUES (?, 1)''', (org,))
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?',
                    (org,))
    conn.commit()

# https://www.sqlite.org/lang_select.html
sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

cur.close()
