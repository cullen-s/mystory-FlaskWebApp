# mystory-FlaskWebApp
Social media web application built on Flask and html5.up's HTML5 template

Click [here](https://vimeo.com/361941506) for demo

![](https://i.imgur.com/itRaXhu.png?1)

# Using the web app

#### Preparing Environment
    $ vagrant init mystory
    $ vagrant up
    $ pip install -r requirements.txt
    $ cd /mystory/server
    $ python app.py

#### Visiting website
localhost:5000

#### Posting a Story

A user has the option of clicking "Post a new story" on the beginning card to quickly jump to the form which allows for a new post to be made. Instructions on how to get the most out of your story are available by clicking or tapping the (?)

Current features include URL image attachments and Alignment settings, along with name, title, story, email, and the user's current date are also recorded in the database.

Stories are validated using wtforms, then entered in a SQLAlchemy database

#### Deleting a Story

Once a story is posted, an email will be automatically sent to the user's provided email. This email includes a unique ID that will allow for their post to be deleted if so desired

Navigating to localhost:5000/delete will provide a form for deleting a previously created story.

# Resources
Credits, Resources, Everything used:

html5up.net (template)

jQuery

thenounproject (Some icons)

pexels (Some images)

Unsplash (Some images)

npmjs.com

Font Awesome

Normalizewheel

Vagrant

Stack-overflow

https://buildmedia.readthedocs.org/media/pdf/flask/latest/flask.pdf

https://flask-sqlalchemy.palletsprojects.com/en/2.x/
