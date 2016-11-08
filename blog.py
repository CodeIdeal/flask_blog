import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['DB_PATH'] = "C:/Users/woshi/PycharmProjects/blog/blog.db"
app.config['HAS_INIT_DB'] = True


@app.route('/')
def index():
    posts = get_posts()
    return render_template("index.html", posts=posts)


@app.route('/post/<int:post_id>')
def post(post_id):
    poster = get_post(post_id)
    return render_template("post.html", post=poster)


@app.route('/add')
def add():
    add_post(request.form[0], request.form[1], request.form[2], request.form[3], date())
    posts = get_posts()
    return render_template("index.html", posts=posts)


def add_post(title, subtitle, content, tags, date):
    get_cursor().execute("insert into posts (title,subtitle,content,tags,date) values(?,?,?,?)"
                         , [title, subtitle, content, tags, date])
    get_db().commit()


def get_posts():
    cursor = get_cursor().execute("select post_id, title, subtitle, tags, date from posts ORDER BY post_id DESC ")
    return [dict(post_id=row[0], title=row[1], subtitle=row[2], tags=row[3], date=row[4])for row in cursor.fetchall()]


def get_post(pots_id):
    cursor = get_cursor().execute("select title, subtitle, content, tags, date from posts WHERE post_id=?", (pots_id,))
    poster = cursor.fetchone()
    return dict(title=poster[0], subtitle=poster[1], content=poster[2], tags=poster[3], date=poster[4])


def get_db():
    if not app.config['HAS_INIT_DB']:
        init_db()
        return sqlite3.connect(app.config['DB_PATH'])
    else:
        return sqlite3.connect(app.config['DB_PATH'])


def init_db():
    db = sqlite3.connect(app.config['DB_PATH'])
    cursor = db.cursor()
    # cursor.execute()和cursor.executescript()的区别：
    # 前者只能执行单一一句sql语句，后者可以执行多句sql语句。
    if not app.config['HAS_INIT_DB']:
        sql = app.open_resource("db.sql").read()
        cursor.executescript(sql.decode("utf-8"))
        db.commit()
        app.config['HAS_INIT_DB'] = True


def get_cursor():
    return get_db().cursor()


if __name__ == '__main__':
    app.run(debug=True)
