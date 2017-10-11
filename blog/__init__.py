import os
import sqlite3

import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html
from flask import render_template, request, redirect, url_for, send_from_directory, session, flash, jsonify, Blueprint, current_app
from werkzeug.utils import secure_filename
from config import Blog


class HighlightRenderer(mistune.Renderer):
    def block_code(self, code, lang=None):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                   mistune.escape(code)
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = html.HtmlFormatter()
        return highlight(code, lexer, formatter)


blog = Blueprint('blog', __name__, static_folder='static', template_folder='templates', subdomain='blog')
renderer = HighlightRenderer()
markdown = mistune.Markdown(renderer=renderer)


# ============route start============
@blog.route('/')
def index():
    posts = get_posts_by_index(0)
    return render_template("index.html", posts=posts, cur_page=0, pages=(int(get_posts_num() / 10) + 1))


# page_index start with 1
@blog.route('/<int:page_index>')
def page(page_index):
    posts = get_posts_by_index(page_index)
    num = get_posts_num()
    return render_template("index.html", posts=posts, cur_page=page_index, pages=(int(num / 10) + 1))


@blog.route('/download/<string:src>')
def download(src):
    return send_from_directory(Blog.UPLOAD_FOLDER, src)


@blog.route('/upload', methods=['POST'])
def upload():
    if 'logged_in' in session and session['logged_in']:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(Blog.UPLOAD_FOLDER, filename))
            return redirect(url_for('.files'))
        return redirect(url_for('.error'))
    else:
        return redirect(url_for('.login'))


@blog.route('/error')
def error():
    return render_template("error.html")


@blog.route('/files')
def files():
    dir_files = []
    for i in os.listdir(Blog.UPLOAD_FOLDER):
        dir_files.append(i)
    return render_template("fileManager.html", files=dir_files)


@blog.route('/post/<int:post_id>')
def post(post_id):
    poster = get_post(post_id)
    poster['content'] = markdown(poster['content'])
    return render_template("post.html", post=poster)


@blog.route('/add', methods=['POST'])
def add():
    add_post(request.form['title'], request.form['subtitle'], request.form['content'], request.form['tags'],
             sqlite3.Date.today())
    return redirect(url_for('.index'))


@blog.route('/edit/new')
def edit_add():
    return render_template("edit.html")


@blog.route('/edit/<int:post_id>')
def edit_modify(post_id):
    poster = get_post(post_id)
    return render_template('edit.html', post=poster)


@blog.route('/modify', methods=['POST'])
def modify():
    if 'logged_in' in session and session['logged_in']:
        update_post(request.form['post_id'], request.form['title'], request.form['subtitle'], request.form['content'],
                    request.form['tags'], request.form['post_date'])
        return redirect(url_for('.post', post_id=request.form['post_id']))
    else:
        return redirect(url_for('.login'))


@blog.route('/delete', methods=['POST'])
def delete():
    response = {'isLogin': False, 'deleted': False}
    if 'logged_in' in session and session['logged_in']:
        delete_post(request.form['post_id'])
        response['isLogin'] = True
        response['deleted'] = True
    else:
        response['isLogin'] = False
        response['deleted'] = False
    return jsonify(response)


@blog.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@blog.route('/login_submit', methods=['POST'])
def login_submit():
    if login_session(request.form['username'], request.form['passwd']):
        return redirect(url_for('.index'))
    else:
        flash('login failed!')
        return redirect(url_for('.login'))


@blog.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('logged_in', False)
    return redirect(url_for('.index'))
# ============route end============


# ============Login start============
def login_session(username, passwd):
    if username == Blog.USER_NAME and passwd == Blog.USER_PASSWD:
        session['username'] = request.form['username']
        session['logged_in'] = True
        return True
    return False

# ============Login start============


# ============Post function start============
# noinspection SqlNoDataSourceInspection,SqlResolve
def add_post(title, subtitle, content, tags, post_date):
    db = get_db()
    db.execute("INSERT INTO posts (title,subtitle,content,tags,post_date) VALUES(?,?,?,?,?)",
               [title, subtitle, content, tags, post_date])
    db.commit()


# noinspection SqlNoDataSourceInspection,SqlResolve
def delete_post(post_id):
    db = get_db()
    db.execute("DELETE FROM posts WHERE post_id = ?", (post_id,))
    db.commit()


# noinspection SqlNoDataSourceInspection,SqlResolve
def update_post(post_id, title, subtitle, content, tags, post_date):
    db = get_db()
    db.execute("UPDATE posts SET title=?,subtitle=?,content=?,tags=?,post_date=? WHERE post_id=?",
               (title, subtitle, content, tags, post_date, post_id))
    db.commit()


# noinspection SqlNoDataSourceInspection,SqlResolve
def get_post(pots_id):
    cursor = get_cursor().execute(
        "SELECT post_id, title, subtitle, content, tags, post_date FROM posts WHERE post_id=?", (pots_id,))
    poster = cursor.fetchone()
    return dict(post_id=poster[0], title=poster[1], subtitle=poster[2], content=poster[3], tags=poster[4],
                date=poster[5])


# noinspection SqlNoDataSourceInspection,SqlResolve
def get_all_posts():
    cursor = get_cursor().execute(
        "SELECT post_id, title, subtitle, tags, post_date FROM posts ORDER BY post_id DESC ")
    return [dict(post_id=row[0], title=row[1], subtitle=row[2], tags=row[3], date=row[4]) for row in cursor.fetchall()]


# noinspection SqlNoDataSourceInspection,SqlResolve
def get_posts_by_index(page_index):
    cursor = get_cursor().execute(
        "SELECT post_id, title, subtitle, tags, post_date, content FROM posts ORDER BY post_id DESC LIMIT 10 OFFSET ?",
        ((page_index-1)*10,))
    return [dict(post_id=row[0], title=row[1], subtitle=row[2], tags=row[3], date=row[4],
                 content=row[5]) for row in cursor.fetchall()]


# noinspection SqlNoDataSourceInspection,SqlResolve
def get_posts_num():
    cursor = get_cursor().execute("SELECT COUNT(*) FROM posts")
    return cursor.fetchone()[0]
# ============Post function end============


# ============DB function start============
def init_db():
    db_file = open(Blog.DB_PATH, 'w')
    db_file.close()
    db = sqlite3.connect(Blog.DB_PATH)
    cursor = db.cursor()
    sql = current_app.open_resource(Blog.SQL_PATH).read()
    cursor.executescript(sql.decode("utf-8"))
    db.commit()


def get_db():
    db_dir = Blog.DB_PATH
    isfile = os.path.isfile(db_dir)
    if not isfile:
        init_db()
    connect = sqlite3.connect(Blog.DB_PATH)
    connect.row_factory = sqlite3.Row
    return connect


def get_cursor():
    return get_db().cursor()


# ============DB function end============

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in Blog.ALLOWED_EXTENSIONS
