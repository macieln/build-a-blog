from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:AlphaBravoCharlie@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(400))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/')
def index():

    return redirect('/blog')

@app.route('/blog', methods=['POST', 'GET'])
def blog():

    title_error = ''
    body_error = ''

    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']

        if blog_title == '':

            title_error = 'Invalid Title'

        if blog_body == '':

            body_error = 'Invalid Entry'

        if title_error or body_error:

            return render_template('newpost.html', title='Add Blog Entry', title_error=title_error, body_error=body_error)
        else:
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()

            return render_template('blog.html', title=new_blog.title.title(), blog_body=new_blog.body)

    blog_id = request.args.get('id')
    if blog_id:
        blog = Blog.query.filter_by(id=blog_id).all()
        return render_template('blog.html', title=blog[0].title.title(), blog_body=blog[0].body)

    blogs = Blog.query.all()

    return render_template('main.html', title='Build A Blog', blogs=blogs, title_error='', body_error='')

@app.route('/newpost')
def newpost():

    return render_template('newpost.html', title='Add Blog Entry')

if __name__ == '__main__':
    app.run()
