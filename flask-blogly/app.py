"""Blogly application.""" 

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.errorhandler(404)  
def error_handler(e):
    return render_template('404.html'),404

@app.route('/', methods = ['GET'])
def main():
    return redirect('/users')

@app.route('/users', methods = ['GET'])
def show_users():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users = users)

@app.route('/users/new', methods = ['GET'])
def new_user():
    return render_template ('users/new_user.html')

@app.route('/users/new', methods = ['POST'])
def add_user_info():
    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        image_url = request.form['image_url'] or None
        )
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>', methods = ['GET'] )
def show_user_info(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user = user)

@app.route('/users/<int:user_id>/edit', methods= ['GET'])
def edit_request(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user = user)

@app.route('/users/<int:user_id>/edit', methods = ['POST'])
def user_edit(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods = ['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

'''Part 2 Posts'''

@app.route('/users/<int:user_id>/posts/new', methods = ['GET'])
def show_post_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('/posts/new_post.html', user = user)

@app.route('/users/<int:user_id>/posts/new', methods = ['POST'])
def adding_new_post(user_id):
    user = User.query.get_or_404(user_id)
    new_post = Post(title = request.form['title'],
                    content =request.form['content'],
                    user_id = user_id
                    )
    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/post/<int:post_id>', methods = ['GET'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('/posts/show.html', post = post)

@app.route('/posts/<int:post_id>/edit', methods = ['GET'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('/posts/edit.html', post = post)

@app.route('/post/<int:post_id>/edit', methods = ['POST'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.content = request.form['content']
    post.title = request.form['title']

    db.session.add(post)
    db.session.commit()
    return redirect(f'/users/{post.user_id}')

@app.route('/post/<int:post_id>/delete', methods = ['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{post.user_id}')

'''Part 3 tags'''

@app.route('/tags', methods = ['GET'])
def get_tags():
    tags = Tag.query.all()
    return render_template('tags/get_tag.html', tags = tags)

@app.route('/tags/<int:tag_id>', methods = ['GET'])
def adding_new_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/show.html', tag = tag)

@app.route('/tags/new', methods = ['GET'])
def tag_form():
    posts = Post.query.all()
    return render_template('tags/new_tag.html', posts = posts)

@app.route('/tags/new', methods = ['POST'])
def add_tag():
    post_ids = [int(num) for num in request.form.getlist('POST')]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(tagname = request.form['tagname'], posts = posts)

    db.session.add(new_tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit', methods = ['GET'])
def show_tag_form(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    
    return render_template('tags/edit.html', posts = posts, tag = tag)

@app.route('/tags/<int:tag_id>/edit', methods = ['POST'])
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['tagname']
     #retrieves postIDs with the submitted tag
    post_ids = [int(num) for num in request.form.getlist('posts')]
    ## get post from postIDs earlier
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()
    
    db.session.add(tag)
    db.session.commit()
    return redirect("/tags")

@app.route('/tags/<int:tag_id>/delete', methods = ['POST'])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')
    
