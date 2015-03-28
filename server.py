from flask import Flask, render_template, redirect, jsonify
import db
import subprocess
import sys
import merger
from os import system


#subprocess.Popen([sys.executable, "db.py"])
system("title " + "testing.nordavind.ru")
app = Flask(__name__, static_folder='', static_url_path='')
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
dtb = db.Database('server')
svn = merger.Merger()


@app.route("/")
def index():
    """
    Парсим результаты с dtb.py
    test = dtb.read_urls_test()
    Получаем список, вида:
    l = [['SmartStation_x86 Windows', '192.168.6.104', '8081', '/tvz-win-trunk', '9581', True, 1],[],...]
    где:
    l[0][0] - Имя страницы из конфига
    l[0][1] - ip  вебсервера, на котором запущено тестирование
    l[0][2] - порт  вебсервера, на котором запущено тестирование
    l[0][3] - путь к вебсерверу
    l[0][4] - последняя ревизия
    l[0][5] - статус сервера 192.168.6.104
    l[0][6] - primary key из БД

    cams = dtb.read_cam_status()
    c = [('192.168.10.10', 0, 0), ('192.168.10.11', 0, 1),...]
    c[0][0] = ip камеры
    c[0][1] = Статус камеры. True или False
    c[0][2] = primary key из БД

    res = dtb.read_cam_status()
    res = [('Redmine', 'redmine.nordavind.ru', True, 0), ...]
    res[0][0] = название ресурса
    res[0][1] = ip или url
    res[0][2] = статус
    res[0][3] = primary key из БД

    """
    test = dtb.read_test()
    build = dtb.read_build()
    doc = dtb.read_doc()
    merge = dtb.read_merge()
    cam = dtb.read_cam()
    res = dtb.read_res()
    buttons = dtb.read_button()
    return render_template('template.html', test=test, build=build, doc=doc, merge=merge, cam=cam, res=res,
                           buttons=buttons)


@app.route("/merge", methods=['GET'])
def index_merge():
    buttons = dtb.read_button()
    return render_template('merge_template.html', buttons=buttons)


@app.route('/<action>', methods=['POST'])
def merge(action):
    buttons = dtb.read_button()
    for data in buttons:
        if action == data[0]:
            out = svn.mergeGo(data[1])
            return render_template('merge_result.html', out=out)
    else:
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)