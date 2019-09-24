from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_mail import Mail, Message
from wtforms import Form, BooleanField, StringField, TextAreaField, FileField, validators
from flask_wtf.file import FileField, FileAllowed
from werkzeug.utils import secure_filename
from threading import Thread

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.sqlite3'
app.config['SECRET_KEY'] = "development"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = #put a username 
app.config['MAIL_DEFAULT_SENDER'] = #put an email 
app.config['MAIL_PASSWORD'] = #put a password

db = SQLAlchemy(app)
mail = Mail(app)

class posts(db.Model):
	id = db.Column('post_id', db.Integer, primary_key = True)
	name = db.Column(db.String(100), nullable=False)
	title = db.Column(db.String(50), nullable=False)
	story = db.Column(db.String(1000), nullable=False)
	email = db.Column(db.String(500), nullable=False)
	imgurl = db.Column(db.String(1000), nullable=True)
	postdate = db.Column(db.DateTime(), default=datetime.datetime.utcnow)

class PostForm(Form):
	name = StringField('Name', [validators.DataRequired(message='Post Failed: You did not enter a name!'), validators.Length(min=3, max=25, message='Post Failed: Name must be between 3 and 25 characters.')])
	title = StringField('Title', [validators.DataRequired(message='Post Failed: You did not enter a title!'), validators.Length(min=5, max=50, message='Post Failed: Title must be between 5 and 50 characters.')])
	story = TextAreaField('Story', [validators.DataRequired(message='Post Failed: You did not enter anything in the story field!'), validators.Length(min=50, max=1000, message='Post Failed: Story must be between 50 and 1000 characters.')])
	email = StringField('Email', [validators.DataRequired(message='Post Failed: You did not enter an email!'), validators.Email(message='Post Failed: You entered an invalid Email address.')])
	imgurl = StringField('Image URL', [validators.URL(require_tld=True, message='Post Failed: Bad URL! See Help Me link for more info.'), validators.Optional()])

def __init__(self, name, title, story, imgurl, postdate):
	self.name = name
	self.title = title
	self.story = story
	self.imgurl = imgurl
	self.postdate = postdate


@app.route('/', methods=['GET', 'POST'])
def addpost():
	form = PostForm(request.form)
	if request.method == 'POST' and form.validate():
			post = posts(name=request.form['name'], title=request.form['title'], story=request.form['story'], imgurl=request.form['imgurl'], email=request.form['email'])

			db.session.add(post)
			db.session.commit()

			getID = db.session.execute('SELECT post_id FROM posts WHERE post_id = (SELECT MAX(post_id) FROM posts)')
			mystoryID = getID.fetchall()

			msg = Message(subject='Thanks for posting to My.Story!', recipients=[form.email.data])
			line_one = 'We think the community is going to love your story, thanks for sharing it!'
			line_two = '\nIf desired, you can delete your post using this unique ID number: {}'.format(mystoryID)
			line_three = '\n Visit localhost:5000/delete for more information. Again, thank you, and we hope you decide to share something new soon!'
			line_four = '\n\n\nThis is an automated message, please do not reply.'
			message_tosend = line_one + line_two + line_three + line_four
			msg.body = message_tosend
			mail.send(msg)

			return render_template("index.html", posts=posts.query.all(), form=form)
			
	return render_template('index.html', posts=posts.query.all(), form=form)


@app.route('/delete', methods=['GET', 'POST'])
def deletepost():
	if request.method == 'POST':
		if not request.form['email'] or not request.form['id']:
			flash('Post Not Deleted! There is an error with the data you provided, please try again.', 'error')
		else:
			deletePost = posts.query.filter_by(id=request.form['id']).delete()
			db.session.commit()

		return redirect(url_for('addpost'))

	return render_template('delete-post.html')



if __name__ == '__main__':
	db.create_all()
	app.run(debug = True)