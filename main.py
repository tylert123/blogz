from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://build-a-blog:blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO']=True
db = SQLAlchemy(app)
app.secret_key='randomsecretkey4BuildABlog'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self,title,body):
        self.title = title
        self.body = body

@app.route('/blog', methods=['GET','POST'])
def blog_posts():
    return render_template('blog.html', blog_post=Blog.query.all())


# @app.route('/newblog', methods=['GET','POST'])
# def new_post():
#     blog_title = request.form['blog_title']
#     blog_body = request.form['blog_body']

#     if (blog_title.strip()=='') and (blog_body.strip()==''):
#         flash('Please enter a blog title', 'error')
#         flash('Please enter a blog message', 'error')

#         return render_template('newpost.html')

#     if (not blog_title) or (blog_title.strip()==''):
#         flash('Please enter a blog title', 'error')
#         return render_template('newpost.html')

#     if (not blog_body) or (blog_body.strip()==''):
#         flash('Please enter a blog message', 'error')
#         return render_template('newpost.html')

#     return render_template('blog.html')

# def ind_post():
#     post_num = request.args.get('post.id')
#     post_info = Blog.query.filter_by(post_num).all()
#     if post_num in post_info:
#         post_title = post_info.title(post_num)
#         post_body = post_info.body(post_num)

#     return render_template('blog.html?id={0}'.format(post_num), post_num=post_num, post_title=post_title, post_body=post_body)

@app.route('/newpost', methods=['GET','POST'])
def new_post():
    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']

        if (blog_title.strip()=='') and (blog_body.strip()==''):
            flash('Please enter a blog title', 'error')
            flash('Please enter a blog message', 'error')

            return render_template('newpost.html')

        if (not blog_title) or (blog_title.strip()==''):
            flash('Please enter a blog title', 'error')
            return render_template('newpost.html')

        if (not blog_body) or (blog_body.strip()==''):
            flash('Please enter a blog message', 'error')
            return render_template('newpost.html')

        if (blog_title.strip()!='') and (blog_body.strip()!=''):
            new_blog_post = Blog(blog_title,blog_body)
            db.session.add(new_blog_post)
            db.session.commit()
            return redirect('/blog')

    else: 
        return render_template('newpost.html')

    # return render_template('blog.html')

if __name__ == '__main__':
    app.run()