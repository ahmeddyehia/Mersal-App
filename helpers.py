from flask import redirect,session,render_template
from functools import wraps
import base64
from cryptography.fernet import Fernet

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/signin")
        return f(*args, **kwargs)

    return decorated_function


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code

def decode_img(img):
    encode=base64.b64encode(img)
    decode=encode.decode('utf-8')
    return decode




# Generate a key (store this securely and do not expose it)
key = b'wrnpB7JFsn6n19qS5rYAgAjJiKGRYMdHuNWuMYA6NdA='
cipher_suite = Fernet(key)

# Function to encrypt a message
def encrypt_message(message):
    encrypted_message = cipher_suite.encrypt(message.encode())
    return encrypted_message

# Function to decrypt a message
def decrypt_message(encrypted_message):
    decrypted_message = cipher_suite.decrypt(encrypted_message).decode()
    return decrypted_message
