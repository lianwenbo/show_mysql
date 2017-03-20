from flask import Flask, render_template as tmpl, request, make_response
from flaskext.mysql import MySQL
from flask_bootstrap import Bootstrap
import argparse

mysql = MySQL()
cursor = None
app = Flask(
    __name__,
    static_folder='static',
    template_folder='templates'
)
bootstrap = Bootstrap(app)
parser = argparse.ArgumentParser()
parser.add_argument('--conf', default='conf/conf.yaml')
args = parser.parse_args()
with open(args.conf) as f:
    import yaml
    config = yaml.load(f)


def set_mysql_config(app, conf=None):
    if not conf:
        return
    app.config['MYSQL_DATABASE_USER'] = conf['user']
    app.config['MYSQL_DATABASE_PASSWORD'] = conf['password']
    app.config['MYSQL_DATABASE_DB'] = conf['database']
    app.config['MYSQL_DATABASE_HOST'] = conf['host']


set_mysql_config(app, config)
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()
app.jinja_env.globals.update(len=len)


@app.route('/')
@app.route('/index.html')
def index():
    return tmpl('index.html')


@app.route('/unget_packages.html')
def unget_packages():
    cursor.execute(config['unget_package_sql'])
    return tmpl('unget_packages.html', cursor=cursor,
                schema=config['unget_schema'],
                cols=config['unget_columns'])


@app.route('/docs/<metatxtid>')
def get_docs(metatxtid=None):
    cursor.execute(config['download_pdf_sql'] % metatxtid)
    pdf_data = cursor.fetchone()
    response = make_response(pdf_data)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] =\
        'inline; filename=%s' % metatxtid
    return response


@app.route('/get_packages.html')
def get_packages():
    cursor.execute(config['get_package_sql'])
    return tmpl('get_packages.html', cursor=cursor,
                schema=config['get_schema'],
                cols=config['get_columns'])


@app.route('/detail_package.html')
def detail_package():
    cmd = config['get_detail_sql'] % (request.args['metatxtid'], request.args['nameid'])
    cursor.execute(cmd)
    not_empty = {}
    by_10_map = {}
    by_100_map = {}
    for record in cursor.fetchall():
        gram = int(record[0] * 1000)
        if gram not in not_empty:
            not_empty[gram] = 1
        else:
            not_empty[gram] += 1
        by_10 = gram / 10
        if by_10 * 10 not in by_10_map:
            by_10_map[by_10 * 10] = 1
        else:
            by_10_map[by_10 * 10] += 1
        by_100 = gram / 100
        if by_100 * 100 not in by_100_map:
            by_100_map[by_100 * 100] = 1
        else:
            by_100_map[by_100 * 100] += 1
    return tmpl('detail_package.html', label_args=request.args,
                not_empty=not_empty, by_10_map=by_10_map,
                by_100_map=by_100_map)
