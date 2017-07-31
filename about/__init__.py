from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session, flash, jsonify, Blueprint

about = Blueprint("about", __name__, static_folder='static', template_folder='templates', subdomain="about")


@about.route("/")
def about_page():
    return render_template("about.html", imgurl="https://bing.ioliu.cn/v1?d=0&w=1920&h=1080")
