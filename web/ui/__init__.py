from flask import Flask, render_template as tmpl, request
from flaskext.mysql import MySQL

mysql = MySQL()
cursor = None
app = Flask(
    __name__,
    static_folder='static',
    template_folder='templates'
)
app.config['MYSQL_DATABASE_USER'] = 'lianwenbo'
app.config['MYSQL_DATABASE_PASSWORD'] = '123456'
app.config['MYSQL_DATABASE_DB'] = 'transport'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()

entries = []


@app.route('/')
@app.route('/index')
def index():
    return tmpl('index.html')


@app.route('/add_entry', methods=['POST'])
def add_entry():
    name_list = []
    value_list = []
    name_fmt = []
    if request.form['name']:
        name_list.append('name')
        value_list.append('\'' + request.form['name'] + '\'')
        name_fmt.append('%s')
    if request.form['sex']:
        name_list.append('sex')
        value_list.append('\'' + request.form['sex'] + '\'')
        name_fmt.append('%s')
    if request.form['age']:
        name_list.append('age')
        value_list.append(str(int(request.form['age'])))
        name_fmt.append('%s')
    if request.form['tel']:
        name_list.append('tel')
        value_list.append(str(int(request.form['tel'])))
        name_fmt.append('%s')
    name_fmt = '(' + ','.join(name_fmt) + ')'
    names = tuple(name_list)
    values = tuple(value_list)
    insert_record = 'insert into students ' +\
                    (name_fmt % names) + 'values ' + (name_fmt % values)
    cursor.execute(insert_record)
    return tmpl('index.html', insert_record=(insert_record + ' OK'))


@app.route('/show_entries', methods=['POST'])
def show_entries():
    cursor.execute('select * from students')
    return tmpl('index.html', cursor=cursor)
