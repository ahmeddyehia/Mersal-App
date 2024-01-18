from flask import session,request,redirect,render_template,flash,Flask,Response,url_for,jsonify
from flask_session import Session
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from helpers import login_required,apology,decode_img,encrypt_message,decrypt_message
import mimetypes
ALLOWED_EXTENSIONS = { 'jpg', 'jpeg'}
app=Flask(__name__)
app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]="filesystem"
Session(app)
db=SQL("sqlite:///mersal.db")
now=datetime.now()
dt_str=now.strftime("%d %m %Y %H:%M:%S")




@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/",methods=["GET","POST"])
@login_required
def index():
    if request.method == "POST":
        search = request.form.get("search")
        if not search:
            flash("Please provide a search term.")
            return redirect("/")

        users = db.execute(
            "SELECT * FROM users JOIN imgs ON users.id=imgs.user_id WHERE username LIKE ? AND NOT id=?",
            ("%" + search + "%",),session["user_id"]
        )

        users_summary = []
        if not users:
            flash("User not found.")
        else:
            for row in users:
                id = row["id"]
                name = row["name"]
                username = row["username"]
                bio = row["bio"]
                if row["img"]:
                    img = decode_img(row["img"])
                    mimetype = row["mimetype"]
                else:
                    img = None
                    mimetype = None

                users_summary.append({
                    "id": id,
                    "name": name,
                    "username": username,
                    "img": img,
                    "mimetype": mimetype,
                    "bio": bio
                })

        return render_template("index.html", users=users_summary)

    return render_template("index.html")

@app.route("/signin",methods=["GET","POST"])
def signin():

    # Forget any user_id
    session.clear()

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")
    return render_template("signin.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
    """Register user"""
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not name:
                flash("must provide a name")
                return redirect("/signup")            
        if not username:
                flash("must provide username")
                return redirect("/signup")  
        if username.isalnum()==False:
                flash("You can't add special carecters in username")
                return redirect("/signup")
        if db.execute("SELECT * FROM users WHERE username = ?", username):
                flash("Username is alread exsist")
                return redirect("/signup")
        # Ensure password was submitted
        elif not password:
                flash("must provide password")
                return redirect("/signup")
        elif not confirmation:
                flash("must confirm password")
                return redirect("/signup")

        # Query database for username
        if password == confirmation:

            db.execute(
                    "INSERT INTO users (time,name,username,hash) VALUES (?,?,?,?)", dt_str,name,username, generate_password_hash(password)
                )
            user=db.execute("SELECT * FROM users WHERE username=?",username)
            try:
                with open ("./static/no one.jpg","rb") as img:
                        img_data=img.read()
                        img_mimetype, _ = mimetypes.guess_type("./static/no one.jpg")
                        img_name="no one"
                        db.execute("INSERT INTO imgs (user_id,img_name,img,mimetype) VALUES (?,?,?,?)",user[0]["id"],img_name,img_data,img_mimetype)

                flash("USER ADDED")
                return redirect("/")
            except:
                 db.execute("INSERT INTO imgs (user_id) VALUES (?)",user[0]["id"])
                 return redirect ("/")

                 
        else:
            flash("Retype the same password")
            return redirect("/signup")

    else:
        return render_template("signup.html")
@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect("/")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/profile', methods=['GET', 'POST'])
def upload_file():
    img=db.execute("SELECT * FROM imgs WHERE user_id =?",session["user_id"])
    row=db.execute("SELECT * FROM users WHERE id=?",session["user_id"])    
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect("/setting")

        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect("/setting")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filedata=file.read()
            mimetype=file.mimetype  
            img=db.execute("SELECT * FROM imgs WHERE user_id =?",session["user_id"])
            if img:
                db.execute("UPDATE imgs SET img=? ,mimetype=? , img_name=? WHERE user_id=?",filedata,mimetype,filename,session["user_id"])
                flash("img updated")
                return redirect("/setting")
        flash("Unsupported file")       
        return redirect("/setting")
    if img[0]["img"]:
        f_str = decode_img(img[0]["img"])
        return render_template("profile.html", imgdata=f_str, mimetype=img[0]["mimetype"],name=row[0]["name"],username=row[0]["username"], bio=row[0]["bio"])

    return render_template("profile.html",name=row[0]["name"],username=row[0]["username"], bio=row[0]["bio"] )

@app.route("/setting",methods=["GET","POST"])
def setting():
    return render_template("setting.html")

@app.route("/delete_account",methods=["GET","POST"])
@login_required
def delete_account ():
    if request.method=="POST":
        password=request.form.get("password")
        row=db.execute("SELECT * FROM users WHERE id=?",session["user_id"])
        if not password:
            flash("Enter your password")
            return redirect("/delete_account")
        if len(row)==1 and check_password_hash(row[0]["hash"],password):
            db.execute("DELETE FROM imgs WHERE user_id=?",session["user_id"])
            db.execute("DELETE FROM users WHERE id=?",session["user_id"])
            db.execute("DELETE FROM messages WHERE sender_id=? OR receiver_id=?",session["user_id"],session["user_id"])
            session.clear()
            return redirect ("/logout")
        else:
            flash("Invalid password")
            return redirect("/delete_account")
    return render_template("deleteaccount.html")

@app.route("/bio",methods=["POST"])
@login_required
def bio():
    if request.form.get("bio"):
        db.execute("UPDATE users SET bio=? WHERE id=?",request.form.get("bio"),session["user_id"])
        flash("Bio updated")
        return render_template("setting.html")
    return Response(status=204)
    

@app.route("/change_pass",methods=["GET","POST"])
@login_required
def chang_pass ():
    current = request.form.get("current_pass")
    new = request.form.get("new_pass")
    confirm=request.form.get("confirm_new_pass")
    if request.method == "POST":
        if not current or not new or not confirm:
            flash("You should provide current and new password ")
            return redirect("/change_pass")
        row = db.execute("SELECT * FROM users WHERE id=?", session["user_id"])
        if row and check_password_hash(row[0]["hash"], current):
            if current==new:
                flash("U can't use the same privous password")
                return redirect("/change_pass")
            if new==confirm:
                db.execute("UPDATE users SET hash=? WHERE id=?", generate_password_hash(new), session["user_id"])
                flash("Password_Updatated")
                return redirect("/")
            else:
                 flash("Retype the same password")
                 return redirect("/change_pass")
        else:
            flash("Type your correct password")
            return redirect("/change_pass")
    return render_template("changepass.html")



@app.route("/chat", methods=["GET", "POST"])
@login_required
def chat():
    id = request.args.get("id")

    if request.method == "POST":
        id = request.form.get("id")
        message_content = request.form.get("message")
        if message_content and message_content != "":
            # Encrypt the message before storing it in the database
            encrypted_message = encrypt_message(message_content)
            user=db.execute("SELECT * FROM users WHERE id=?",id)
            if user:
                db.execute("INSERT INTO messages (sender_id, receiver_id, content) VALUES (?,?,?)",
                       session["user_id"], id, encrypted_message)
            else:
                flash("User is not found")
                return redirect("/")
        return redirect(url_for('chat', id=id))

    receiver = db.execute("SELECT * FROM users JOIN imgs ON users.id=imgs.user_id WHERE id=?", id)
    if receiver:
        img = decode_img(receiver[0]["img"])
        mimetype = receiver[0]["mimetype"]
        me = db.execute("SELECT * FROM users JOIN imgs ON users.id=imgs.user_id WHERE id=?", session["user_id"])
        me_img = decode_img(me[0]["img"])
        me_mimetype = me[0]["mimetype"]

        sender_id = me[0]["id"]
        receiver_id = receiver[0]["id"]
        if request.args.get("poll"):
            # If "poll" parameter is present, return new messages as JSON
            last_message_id = request.args.get("last_message_id")
            new_messages = db.execute(
                "SELECT * FROM messages WHERE ((sender_id=? AND receiver_id=?) OR (sender_id=? AND receiver_id=?)) AND message_id > ? ORDER BY timestamp",
                sender_id, receiver_id, receiver_id, sender_id, last_message_id
            )
            decrypted_messages = [
                {
                    "message_id": message["message_id"],
                    "sender_id": message["sender_id"],
                    "receiver_id": message["receiver_id"],
                    "content": decrypt_message(message["content"]),
                    "timestamp": message["timestamp"]
                } for message in new_messages
            ]
            return jsonify(messages=decrypted_messages)

        encrypted_messages = db.execute(
            "SELECT * FROM messages WHERE (sender_id=? AND receiver_id=?) OR (sender_id=? AND receiver_id=?) ORDER BY timestamp",
            sender_id, receiver_id, receiver_id, sender_id
        )
        decrypted_messages = [
            {
                "message_id": message["message_id"],
                "sender_id": message["sender_id"],
                "receiver_id": message["receiver_id"],
                "content": decrypt_message(message["content"]),
                "timestamp": message["timestamp"]
            } for message in encrypted_messages
        ]

        # If no messages exist, set last_message_id to 0
        last_message_id = decrypted_messages[-1]["message_id"] if decrypted_messages else 0

        return render_template("chat.html", img=img, user=receiver[0]["name"], mimetype=mimetype,
                               me_img=me_img, me_mimetype=me_mimetype, messages=decrypted_messages,
                               sender_id=sender_id, receiver_id=receiver_id, last_message_id=last_message_id)

    flash("User Not Found")
    return redirect("/")
@app.route("/show_chats")
@login_required
def show_chats():
    chats_send=db.execute("SELECT DISTINCT (receiver_id) FROM messages WHERE sender_id=? ",session["user_id"])
    chats_receive= db.execute("SELECT DISTINCT (sender_id) FROM messages WHERE receiver_id=? ",session["user_id"])

    chats=[]
    for id in chats_send:
        if id["receiver_id"] not in chats_receive:
            chats.append(id["receiver_id"])
    for id in chats_receive:
        if id["sender_id"] not in chats:
            chats.append(id["sender_id"])
    users=db.execute("SELECT * FROM users JOIN imgs ON users.id=imgs.user_id WHERE id IN (?)",(chats))
    users_summary = []
    if not users:
        return render_template("show_chats.html")
    else:
        for row in users:
            id = row["id"]
            name = row["name"]
            username = row["username"]
            bio = row["bio"]
            if row["img"]:
                img = decode_img(row["img"])
                mimetype = row["mimetype"]
            else:
                img = None
                mimetype = None

            users_summary.append({
                "id": id,
                "name": name,
                "username": username,
                "img": img,
                "mimetype": mimetype,
                "bio": bio
            })
    return render_template("show_chats.html",users=users_summary)


if __name__ == '__main__':
    app.run(debug=True)