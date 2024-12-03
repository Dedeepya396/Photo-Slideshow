from flask import Flask, render_template,flash, redirect, url_for, request, session
import bcrypt
import mysql.connector
import jwt   # Import the PyJWT library
import time


app = Flask(__name__)
app.secret_key = "!@#$%^adsfmnv"
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="abc",
    database="ISIS_DB"
)

cursor = db.cursor()

salt_hash = bcrypt.gensalt()

# Update the generate_jwt_token function
def generate_jwt_token(username):
    payload = {'username': username}
    secret_key = '@#23$%^'
    expiration_time = 36000  # Set your desired expiration time in seconds
    token = jwt.encode({'exp': time.time() + expiration_time, **payload}, secret_key, algorithm='HS256')

    # Store token and user details in the session
    session['jwt_token'] = token
    session['user_details'] = {'username': username}

    return {'username': username, 'token': token}

def verify_jwt_token(token):
    secret_key = '@#23$%^'  # Replace with the same key used for encoding
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
    
# Add a protected route that requires a valid JWT token
def find_user_details(user_id):
    cursor.execute("SELECT * FROM accounts WHERE username = %s", (user_id,))
    user_data = cursor.fetchone()
    if user_data:
        return {'username': user_data[1], 'email': user_data[2], 'password': user_data[3]}
    return None

@app.route('/', methods=['GET', 'POST'])
@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    token = session.get('jwt_token')
    if not token:
        return redirect(url_for('login'))
    user_data = None
    if token:
        payload = verify_jwt_token(token)
        if payload:
            # Token is valid, get user details from payload
            username = payload['username']
            user_data = find_user_details(username)
        else :
            return render_template('login.html')
    else :
        return render_template('login.html')
    return render_template('confirmation.html', data=user_data, token=token)


@app.route('/home', methods=['GET', 'POST'])
def home():
    token = session.get('jwt_token')
    if not token:
        return redirect(url_for('login'))
    return render_template('home.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    token = session.get('jwt_token')
    if not token:
        return redirect(url_for('login'))

    username = session['user_details']['username']
    if username != 'admin':
        return redirect(url_for('home'))

    cursor.execute("SELECT * FROM accounts")
    data = cursor.fetchall()
    print(data)
    return render_template('admin.html', accounts=data)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    token = session.get('jwt_token')
    if not token:
        return redirect(url_for('login'))
    if request.method == 'POST':
        username = session['user_details']['username']
        files = request.files.getlist('files[]')
        for file in files:
            cursor = db.cursor()
            img = file.read()
            query = "INSERT INTO images (username, image) VALUES (%s, %s)"
            cursor.execute(query, (username, img))
            db.commit()
        return render_template('preview.html')
    return render_template('home.html')

@app.route('/preview', methods=['GET', 'POST'])
def preview():
    token = session.get('jwt_token')
    if not token:
        return redirect(url_for('login'))
    return render_template('preview.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    token = session.get('jwt_token')
    if token:
        return redirect(url_for('/welcome'))
    if(request.method == 'POST'):
        username = request.form.get("name")
        password = request.form.get("password")
        cursor = db.cursor()
        query = f'SELECT * FROM accounts WHERE Username="{username}"'
        cursor.execute(query)
        data = cursor.fetchone()
        if data and bcrypt.checkpw(password.encode(), data[2].encode()):
            token = generate_jwt_token(username)
            session['user_details'] = {'username': username}
            return redirect(url_for('welcome'))
        else:
           return render_template('login.html', err = "Invalid username or password")
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    token = session.get('jwt_token')
    if token:
        return redirect(url_for('/welcome'))
    msg = ''
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        # Check if the username already exists
        cursor.execute("SELECT * FROM accounts WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            msg += "Username already exists. Please choose a different username."
            return render_template('Signup.html', msg = msg)
        
        hash_password = bcrypt.hashpw(password.encode(), salt_hash)
        # Insert the new user if the username is unique
        cursor.execute("INSERT INTO accounts (username, email, password) VALUES (%s, %s, %s)",
                       (username, email, hash_password))
        db.commit()
        # Fetch the user details after insertion
        cursor.execute("SELECT * FROM accounts WHERE username = %s", (username,))
        data1 = cursor.fetchone()
        user_data = {'username': data1[1], 'email': data1[3], 'password': data1[2]}

        # Generate JWT token for the user information
        token = generate_jwt_token(username)
        return render_template('confirmation.html', data=user_data)  # Pass the parsed data to the template
    session.pop('_flashes', None)
    return render_template('Signup.html')

# @app.route('/', methods=['GET', 'POST'])


# @app.route('/', methods=['GET', 'POST'])


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('jwt_token', None)
    session.pop('user_details', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
