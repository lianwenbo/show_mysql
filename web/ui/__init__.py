from flask import Flask, render_template as tmpl, request
from flaskext.mysql import MySQL

mysql = MySQL()
cursor = None
app = Flask(
    __name__,
    static_folder='static',
    template_folder='templates'
)
app.config['MYSQL_DATABASE_USER'] = 'XXX'
app.config['MYSQL_DATABASE_PASSWORD'] = 'XXXX'
app.config['MYSQL_DATABASE_DB'] = 'XXXX'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.jinja_env.globals.update(len=len)
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()

field_names = ['id', 'workcode', 'metastatus']
all_fields = map(lambda x:x.strip(),
                 open('field.conf',
                      'r').readline().strip().split(',')
                 )


@app.route('/')
@app.route('/index')
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
    cursor.execute(select_records)
    return tmpl('index.html', cursor=cursor,
                field_names=all_fields)


@app.route('/show_entries', methods=['POST'])
def show_entries():
    field_tuple_str =  ','.join(all_fields)
    select_cmd = 'select %s from data limit 100' % field_tuple_str
    cursor.execute(select_cmd)
    return tmpl('index.html', cursor=cursor, field_names=all_fields)
