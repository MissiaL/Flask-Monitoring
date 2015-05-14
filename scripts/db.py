import sqlite3
import time
import configparser

from scripts.parse import Parser
from config_monitoring import database

class Database:
    def __init__(self, name):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.tables = config['testing']
        self.db = sqlite3.connect(name, check_same_thread=False, timeout=30)
        for table in self.tables:
            self.db.executescript('''CREATE TABLE IF NOT EXISTS {0}
                                    ( NAME TEXT NOT NULL,
                                      IP TEXT NOT NULL,
                                      PORT TEXT NOT NULL,
                                      doc TEXT NOT NULL,
                                      REV TEXT NOT NULL,
                                      STATUS INT NOT NULL,
                                      ID INT NOT NULL,
                                      PRIMARY KEY (ID) );'''.format(table))
        self.db.executescript('''CREATE TABLE IF NOT EXISTS cam
                                (IP TEXT NOT NULL,
                                 STATUS INT NOT NULL,
                                 ID INT NOT NULL,
                                 PRIMARY KEY (ID) );''')
        self.db.executescript('''CREATE TABLE IF NOT EXISTS res
                                (NAME TEXT NOT NULL,
                                 URL TEXT NOT NULL,
                                 STATUS INT NOT NULL,
                                 ID INT NOT NULL,
                                 PRIMARY KEY (ID) );''')
        self.db.executescript('''CREATE TABLE IF NOT EXISTS button
                                (BRANCH TEXT NOT NULL,
                                 RESULT TEXT NOT NULL,
                                 ID INT NOT NULL,
                                 PRIMARY KEY (ID) );''')
        self.db.executescript('''CREATE TABLE IF NOT EXISTS testbranch
                                (ID INTEGER PRIMARY KEY,
                                 BRANCH TEXT NOT NULL,
                                 DIR TEXT NOT NULL);''')
    def write_test(self, w):
        self.db.execute("DELETE FROM test")
        for key, test in enumerate(w):
            self.db.execute("INSERT OR REPLACE INTO test VALUES(?, ?, ?, ?, ?, ?, ?);",
                            (test[0], test[1], test[2], test[3], test[4], test[5], key))
            self.db.commit()

    def write_build(self, w):
        self.db.execute("DELETE FROM build")
        for key, build in enumerate(w):
            self.db.execute("INSERT OR REPLACE INTO build VALUES(?, ?, ?, ?, ?, ?, ?);",
                            (build[0], build[1], build[2], build[3], build[4], build[5], key))
            self.db.commit()

    def write_doc(self, w):
        self.db.execute("DELETE FROM doc")
        for key, cam in enumerate(w):
            self.db.execute("INSERT OR REPLACE INTO doc VALUES(?, ?, ?, ?, ?, ?, ?);",
                            (cam[0], cam[1], cam[2], cam[3], cam[4], cam[5], key))
            self.db.commit()

    def write_merge(self, w):
        self.db.execute("DELETE FROM merge")
        for key, merge in enumerate(w):
            self.db.execute("INSERT OR REPLACE INTO merge VALUES(?, ?, ?, ?, ?, ?, ?);",
                            (merge[0], merge[1], merge[2], merge[3], merge[4], merge[5], key))
            self.db.commit()

    def write_cam(self, w):
        self.db.execute("DELETE FROM cam")
        for key, cam in enumerate(w):
            self.db.execute("INSERT OR REPLACE INTO cam VALUES(?,?,?);",
                            (cam[0], cam[1], key))
            self.db.commit()

    def write_res(self, w):
        self.db.execute("DELETE FROM res")
        for key, res in enumerate(w):
            self.db.execute("INSERT OR REPLACE INTO res VALUES(?,?,?,?);",
                            (res[0], res[1], res[2], key))
            self.db.commit()

    def write_button(self, w):
        self.db.execute("DELETE FROM button")
        for key, res in enumerate(w):
            self.db.execute("INSERT OR REPLACE INTO button VALUES(?,?,?);",
                            (res[0], res[1], key))
            self.db.commit()

    def read_test(self):
        return self.db.execute("select * from test").fetchall()

    def read_build(self):
        return self.db.execute("select * from build").fetchall()

    def read_doc(self):
        return self.db.execute("select * from doc").fetchall()

    def read_merge(self):
        return self.db.execute("select * from merge").fetchall()

    def read_cam(self):
        return self.db.execute("select * from cam").fetchall()

    def read_res(self):
        return self.db.execute("select * from res").fetchall()

    def read_button(self):
        return self.db.execute("select * from button").fetchall()

def loop():
    while True:
        dtb = Database(database)
        p = Parser()
        dtb.write_test(p.testingTest())
        dtb.write_build(p.testingBuild())
        dtb.write_doc(p.testingDoc())
        dtb.write_merge(p.testingMerge())
        dtb.write_cam(p.camerasCam())
        dtb.write_res(p.resourcesRes())
        dtb.write_button(p.buttons)
        # print('\nLOOP: ', dtb.read_button())
        time.sleep(30)


if __name__ == '__main__':
    loop()
