# Mersal-App
#### Video Demo:  <https://www.youtube.com/watch?v=di9H85SkHEA>
#### Description:
"Mersal is a chat app created using Flask, SQLite, HTML, CSS, and JavaScript. Initially, you should register as a new user. Multiple users can have the same name, but the username must be unique. User data is stored in mersal.db , and passwords are hashed before storage.mersal.db comes with 3 tabels (users,imgs,messages) Afterward, you can log in to your account. Upon logging in, you will be redirected to the home page, featuring various pictures. In the 'Chats' section, you'll find conversations with people where messages are exchanged. The 'Profile' section includes details and settings, allowing you to change your profile picture, bio, password, or delete your account. You'll also find a logout option. Then search section, If a username is not found during a search, the app will display a flash message say "user not found". Once found, you can send  messages which will encrypted and stored in our database. Short polling is employed to check for new messages. This is my CS50 project, and I hope it turns out well."
# Running

Install requirements for theis app :
```
$ pip install -r requirements.txt
```
Start Flask’s built-in web server :
```
$ python app.py
```
Visit the URL outputted by flask to see the distribution code in action.

run sqlite3 mersal.db to open finance.db with sqlite3. If you run .schema in the SQLite prompt, notice how mersal.db comes with a 3 tables called users,imgs and messages. Take a look at its structure (i.e., schema).


