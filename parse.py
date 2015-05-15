from urllib.parse import urlparse
from multiprocessing.dummy import Pool as ThreadPool
import configparser

from lxml import etree
import requests
from lxml import html
import lxml

import ping


class Parser:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.test = []
        for i in config['testing']['test'].split('\n'):
            self.test.append([l.strip() for l in i.split(': ')])

        self.build = []
        for i in config['testing']['build'].split('\n'):
            self.build.append([l.strip() for l in i.split(': ')])

        self.doc = []
        for i in config['testing']['doc'].split('\n'):
            self.doc.append([l.strip() for l in i.split(': ')])

        self.merge = []
        for i in config['testing']['merge'].split('\n'):
            self.merge.append([l.strip() for l in i.split(': ')])

        self.cam = []
        for i in config['cameras']['cam'].split('\n'):
            self.cam.append(i.strip())

        self.res = []
        for i in config['resources']['res'].split('\n'):
            self.res.append([l.strip() for l in i.split(': ')])

        self.buttons = []
        for i in config['buttons']['merge'].split('\n'):
            self.buttons.append([l.strip() for l in i.split(': ')])

    def pinger(self, ip):
        status = ping.ping(ip)
        if status is None:
            return False
        else:
            return True

    def pinger_cam(self, ip):
        if len(ip) == 2:
            ip_adress = ip[1]
            name = ip[0]
            status = ping.ping(ip_adress)
            if status is None:
                return [name, ip_adress, False]
            else:
                return [name, ip_adress, True]
        else:
            status = ping.ping(ip)
            if status is None:
                return [ip, False]
            else:
                return [ip, True]

    def revparser(self, url):
        """
        url = ['SmartStation_x86 Windows', 'http://192.168.6.104:8081/tvz-win-trunk']

        return:
        url_name = Имя адресной строки с конфига config.ini -> SmartStation_x86 Windows
        ip = получаем ip с переменной ip_port -> 192.168.6.104
        port = получаем port с переменной ip_port -> 8081
        name = получаем url вебсервера - > /tvz-win-trunk
        rev = Ревизия
        server_status = Пингуем сервер по ip и получаем ответ True или False
        """
        url_name = url[0]
        ip_port = urlparse(url[1]).netloc
        ip = ip_port.split(':')[0]
        port = ip_port.split(':')[1]
        name = urlparse(url[1]).path[1:]
        server_status = self.pinger(ip)
        try:
            page = requests.get(url[1], timeout=2)
            tree = html.fromstring(page.text)
            rev = max(tree.xpath('//td[@class="context-menu-revision"]/@rev'))
        except (requests.ConnectionError, lxml.etree.XMLSyntaxError):
            rev = 'Uknown'
        except ValueError:
            rev = 'Uknown'
            ip = 'Uknown'
            port = 'Uknown'
        return [url_name, ip, port, name, rev, server_status]

    def testingTest(self):
        pool = ThreadPool(3)
        results = pool.map(self.revparser, self.test)
        pool.close()
        pool.join()
        return results

    def testingBuild(self):
        pool = ThreadPool(3)
        results = pool.map(self.revparser, self.build)
        pool.close()
        pool.join()
        return results

    def testingDoc(self):
        pool = ThreadPool(3)
        results = pool.map(self.revparser, self.doc)
        pool.close()
        pool.join()
        return results

    def testingMerge(self):
        pool = ThreadPool(3)
        results = pool.map(self.revparser, self.merge)
        pool.close()
        pool.join()
        return results

    def camerasCam(self):
        pool = ThreadPool(3)
        results = pool.map(self.pinger_cam, self.cam)
        pool.close()
        pool.join()
        return results

    def resourcesRes(self):
        pool = ThreadPool(3)
        results = pool.map(self.pinger_cam, self.res)
        pool.close()
        pool.join()
        return results

if __name__ == '__main__':
    p = Parser()
    print(p.testingTest())
    print(p.testingBuild())
    print(p.testingDoc())
    print(p.testingMerge())
    print(p.camerasCam())
    print(p.resourcesRes())