# Mersal-App
#### Video Demo:  <https://www.youtube.com/watch?v=di9H85SkHEA>
#### Description:
"Mersal is a chat app created using Flask, SQLite, HTML, CSS, and JavaScript. Initially, you should register as a new user. Multiple users can have the same name, but the username must be unique. User data is stored in mersal.db , and passwords are hashed before storage.mersal.db comes with 3 tabels (users,imgs,messages) Afterward, you can log in to your account. Upon logging in, you will be redirected to the home page, featuring various pictures. In the 'Chats' section, you'll find conversations with people where messages are exchanged. The 'Profile' section includes details and settings, allowing you to change your profile picture, bio, password, or delete your account. You'll also find a logout option. Then search section, If a username is not found during a search, the app will display a flash message say "user not found". Once found, you can send  messages which will encrypted and stored in our database. Short polling is employed to check for new messages. This is my CS50 project, and I hope it turns out well."

# Running
To Install requirements for theis app :
```
$ pip install -r requirements.txt
```
Start Flask’s built-in web server :
```
$ python app.py
```
Visit the URL outputted by flask to see the distribution code in action.

run sqlite3 mersal.db to open finance.db with sqlite3. If you run .schema in the SQLite prompt, notice how mersal.db comes with a 3 tables called users,imgs and messages. Take a look at its structure (i.e., schema).

# app.py
Open up app.py. Atop the file are a bunch of imports, among them CS50’s SQL module and a few helper functions.

Thereafter are a whole bunch of routes. It uses db.execute (from CS50’s library) to query mersal.db. And uses check_password_hash to compare hashes of users’ passwords. signin “remembers” that a user is logged in by storing his or her user_id, an INTEGER, in session. That way, any of this file’s routes can check which user, if any, is logged in. Finally, Once the user has successfully logged in, login will redirect to "/", taking the user to their home page. Meanwhile, notice how logout simply clears session, effectively logging a user out.

Most routes are “decorated” with @login_required (a function defined in helpers.py too). That decorator ensures that, if a user tries to visit any of those routes, he or she will first be redirected to login so as to log in.
Most routes support GET and POST. 
# helper.py
By taking a look at helpers.py. Ah, there’s the implementation of login_required,decode_imgs,encrypt_messages and decrypte_messages
# requirements.txt
By taking a quick look at requirements.txt. That file simply prescribes the packages on which this app will depend.
# static/
Glance too at static/, inside of which is styles.css and some pics that the app will use. 
# templates
By looking in templates/.We will find just an HTML pages, stylized with Bootstrap. 
One of them layout.html. It comes with a fancy, mobile-friendly “navbar” (navigation bar), also based on Bootstrap. Notice how it defines a block, main. It also includes support for Flask’s message flashing so that you can relay messages from one route to another for the user to see.

