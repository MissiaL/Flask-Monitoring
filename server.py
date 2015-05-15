import time
import itertools
import os
import sys

from flask import Flask, render_template, redirect, jsonify, request, Response, url_for, abort

from config_monitoring import host, port, title, database
import db

# from scripts import merger
# from scripts.testbranch import downloadSource

if sys.platform == 'win32':
    os.system(title)

#subprocess.Popen([sys.executable, 'scripts/db.py'])

app = Flask(__name__)
app.config.from_object('config_monitoring')
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

dtb = db.Database(database)
# svn = merger.Merger()


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

    res = dtb.read_res_status()
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
    return render_template('index.html', test=test, build=build, doc=doc, merge=merge, cam=cam, res=res,
                           buttons=buttons)


@app.route("/merge", methods=['GET'])
def index_merge():
    buttons = dtb.read_button()
    return render_template('merge_template.html', buttons=buttons)


@app.route('/buttons', methods=['POST'])
def merge():
    buttons = [i[0] for i in dtb.read_button()]
    input_name = [key for key in dict(request.form).keys()]
    input_name = input_name[0]
    if input_name in buttons:
        # out = svn.mergeGo(input_name)
        out = 'svn'
        return render_template('merge_result.html', out=out)
    else:
        return redirect('/')


@app.route('/js')
def getjs():
    jsResStatus = {}
    for data in dtb.read_res():
        jsResStatus[data[0]] = data[2]
    jsCamStatus = {}
    for data in dtb.read_cam():
        #{primary key=status}
        jsCamStatus[data[2]] = data[1]
    jsMergeStatus = {}
    for data in dtb.read_merge():
        jsMergeStatus[data[6]] = [data[0], data[1], data[2], data[3], data[4], data[5]]
    jsDocStatus = {}
    for data in dtb.read_doc():
        jsDocStatus[data[6]] = [data[0], data[1], data[2], data[3], data[4], data[5]]
    jsBuildStatus = {}
    for data in dtb.read_build():
        jsBuildStatus[data[6]] = [data[0], data[1], data[2], data[3], data[4], data[5]]
    jsTestStatus = {}
    for data in dtb.read_test():
        jsTestStatus[data[6]] = [data[0], data[1], data[2], data[3], data[4], data[5]]
    return jsonify(jsResStatus=jsResStatus,
                   jsCamStatus=jsCamStatus,
                   jsMergeStatus=jsMergeStatus,
                   jsDocStatus=jsDocStatus,
                   jsBuildStatus=jsBuildStatus,
                   jsTestStatus=jsTestStatus)


@app.route('/branch')
def branch():
    return render_template('branch.html')


@app.route('/jsbranch', methods=['POST'])
def jsbranch():
    sourceApp, sourceTesting = request.get_json()
    print([sourceApp, sourceTesting])
    #downloadSource([sourceApp, sourceTesting])
    return redirect('/branch')


@app.route('/mergeout')
def mergeout():
    if request.headers.get('accept') == 'text/event-stream':
        def events():
            for i, c in enumerate(itertools.cycle('\|/-')):
                yield "data: %s %d\n\n" % (c, i)
                time.sleep(.1)  # an artificial delay
        return Response(events(), content_type='text/event-stream')
    return redirect(url_for('static', filename='mergeout.html'))

# @app.route('/login')
# def login():
#     abort(404)
#
# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('branch.html'), 404

if __name__ == '__main__':
    app.run(host=host, port=port)