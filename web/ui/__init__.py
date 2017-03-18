from flask import Flask, render_template as tmpl, request
from flaskext.mysql import MySQL
from flask_bootstrap import Bootstrap

mysql = MySQL()
cursor = None
app = Flask(
    __name__,
    static_folder='static',
    template_folder='templates'
)
bootstrap = Bootstrap(app)
#app.config['MYSQL_DATABASE_USER'] = 'lianwenbo'
#app.config['MYSQL_DATABASE_PASSWORD'] = '123456'
#app.config['MYSQL_DATABASE_DB'] = 'transport'
#app.config['MYSQL_DATABASE_HOST'] = 'localhost'
#app.jinja_env.globals.update(len=len)
#mysql.init_app(app)
#conn = mysql.connect()
#cursor = conn.cursor()

field_names = ['id', 'workcode', 'metastatus']
all_fields = map(lambda x:x.strip(),
                 open('field.conf',
                      'r').readline().strip().split(',')
                 )

@app.route('/')
@app.route('/index.html')
def index():
    return tmpl('index.html')


@app.route('/select_entry', methods=['POST'])
def select_entry():
    conds = []
    if request.form['workcode']:
        cond = 'workcode=\'%s\'' % request.form['workcode']
        conds.append(cond)
    if request.form['metastatus']:
        cond = 'metastatus=%s' % request.form['metastatus']
        conds.append(cond)
    select_records = 'select * from data '
    if conds:
        select_records += 'where ' + 'and '.join(conds)
    import sys
    print >>sys.stderr, 'select records:', select_records
    #cursor.execute(select_records)
    return tmpl('index.html')


@app.route('/show_entries', methods=['POST'])
def show_entries():
    field_tuple_str = ','.join(all_fields[1:])
    select_cmd = 'select %s from %s limit 100' % (all_fields[0], field_tuple_str)
    #cursor.execute(select_cmd)
    return tmpl('index.html')


@app.route('/unget_packages.html')
def unget_packages():
    return tmpl('unget_packages.html')


@app.route('/get_packages.html')
def get_packages():
    id = request.args.get('id')
    return tmpl('get_packages.html', id=id)


@app.route('/detail_package.html')
def detail_package():
    id = request.args.get('id')
    return tmpl('detail_package.html', id=id)
