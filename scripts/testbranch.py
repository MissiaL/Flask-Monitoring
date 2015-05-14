import tempfile
import sqlite3

from scripts.merger import SvnClient


svn = SvnClient()


def downloadSource(svnUrls):
    db = sqlite3.connect('server')
    db.execute('delete from testbranch')
    # svn.checkout(url, tempdir)
    for url in svnUrls:
        tempdir = tempfile.mkdtemp()
        db.executemany('INSERT INTO testbranch (BRANCH, DIR) VALUES (?,?)', [(url, tempdir)])
        db.commit()
    print(db.execute('select * from testbranch').fetchall())
    db.close()

def checkDb():
    db = sqlite3.connect('server')
    if db.execute('select * from testbranch').fetchall():
        return False
    else:
        return True

url = ['1212', '444']
#downloadSource(url)
checkDb()