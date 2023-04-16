'''
    Our Model class
    This should control the actual "logic" of your website
    And nicely abstracts away the program logic from your page loading
    It should exist as a separate layer to any database or data structure that you might be using
    Nothing here should be stateful, if it's stateful let the database handle it
'''
import sqlite3
import view
import random
import sql
import base64
from cryptography.fernet import Fernet

# Generate a 32-byte key that is url-safe
key = Fernet.generate_key()
key = base64.urlsafe_b64encode(key[:32])

# Create a Fernet object with the key
fernet = Fernet(key)

# Initialise our views, all arguments are defaults for the template
page_view = view.View()

#-----------------------------------------------------------------------------
# Index
#-----------------------------------------------------------------------------

def friend():
    '''
        Andy
        Returns the view for the Andy page
    '''
    return page_view("Andy")

def friend_admin():
    '''
        Admin
        Returns the view for the Admin page
    '''
    return page_view("Admin")

def index():
    '''
        index
        Returns the view for the index
    '''
    return page_view("index")

#-----------------------------------------------------------------------------
# Login
#-----------------------------------------------------------------------------

def login_form():
    '''
        login_form
        Returns the view for the login_form
    '''
    return page_view("login")

#-----------------------------------------------------------------------------

# Check the login credentials
def login_check(username, password):
    '''
        login_check
        Checks usernames and passwords

        :: username :: The username
        :: password :: The password

        Returns either a view for valid credentials, or a view for invalid credentials
    '''

    # By default assume good creds
    login = True

    if username != "admin" and username != "andy": # Wrong Username
        err_str = "Incorrect Username"
        login = False
    
    if password != "123": # Wrong password
        err_str = "Incorrect Password"
        login = False
        
    if login and username == "admin":
        return page_view("user")
    if login and username == "andy":
        return page_view("user_andy")
    else:
        return page_view("invalid", reason=err_str)

#-----------------------------------------------------------------------------
# About
#-----------------------------------------------------------------------------

def about():
    '''
        about
        Returns the view for the about page
    '''
    return page_view("about", garble=about_garble())

def send_message(receiver, message):
    # Get the user ID of the receiver
    receiver_id = get_user_id(receiver)

    # Insert the message into the database
    sql.insert_message(sql.get_user_id('Andy'), receiver_id, message)

def get_user_id(username):
    # Get the user ID
    user_id = sql.get_user_id(username)
    return user_id

def get_conversation(user1, user2):
    # Get the user IDs of the two users
    user1_id = get_user_id(user1)
    user2_id = get_user_id(user2)

    # Get the conversation between the two users
    conversation = sql.get_conversation(user1_id, user2_id)

    # Decrypt the messages with Fernet
    decrypted_messages = []
    for message in conversation:
        decrypted_message = fernet.decrypt(message.encode()).decode()
        decrypted_messages.append(decrypted_message)

    return decrypted_messages





# Returns a random string each time
def about_garble():
    '''
        about_garble
        Returns one of several strings for the about page
    '''
    garble = ["leverage agile frameworks to provide a robust synopsis for high level overviews.", 
    "iterate approaches to corporate strategy and foster collaborative thinking to further the overall value proposition.",
    "organically grow the holistic world view of disruptive innovation via workplace change management and empowerment.",
    "bring to the table win-win survival strategies to ensure proactive and progressive competitive domination.",
    "ensure the end of the day advancement, a new normal that has evolved from epistemic management approaches and is on the runway towards a streamlined cloud solution.",
    "provide user generated content in real-time will have multiple touchpoints for offshoring."]
    return garble[random.randint(0, len(garble) - 1)]


#-----------------------------------------------------------------------------
# Debug
#-----------------------------------------------------------------------------

def debug(cmd):
    try:
        return str(eval(cmd))
    except:
        pass


#-----------------------------------------------------------------------------
# 404
# Custom 404 error page
#-----------------------------------------------------------------------------

def handle_errors(error):
    error_type = error.status_line
    error_msg = error.body
    return page_view("error", error_type=error_type, error_msg=error_msg)