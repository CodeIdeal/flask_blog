# coding=utf-8

from flask import Flask, redirect, url_for
from blog import blog
from about import about

app = Flask(__name__)
app.secret_key = '81lgSBFtwY^77#IZj8LDv$InOCN4sWp#'
#: 配置项目域名, 作为Flask的ServerName
app.config['SERVER_NAME'] = 'cabana.tech'
# #: 指定该域名中默认的子域名
# app.url_map.default_subdomain = 'www'


#: 注册蓝图(BluePrint)
app.register_blueprint(blog)
app.register_blueprint(about)


@app.route("/")
def main():
    return redirect(url_for('blog.index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
