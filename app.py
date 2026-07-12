import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "change-this-to-a-random-secret-key"   # required for session/flash

# ---------------- DATABASE CONNECTION ----------------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="service_hub"
    )

# ---------------- STATIC CATEGORY DATA ----------------
CATEGORIES = {
    "electrician":  {"slug": "electrician",  "name": "Electricians",         "icon": "⚡", "desc": "Wiring, repairs & installations"},
    "plumber":      {"slug": "plumber",      "name": "Plumbers",             "icon": "🔧", "desc": "Leaks, fittings & pipelines"},
    "carpenter":    {"slug": "carpenter",    "name": "Carpenters",           "icon": "🪚", "desc": "Furniture & woodwork"},
    "beautician":   {"slug": "beautician",   "name": "Beauticians",          "icon": "💇", "desc": "Salon & grooming at home"},
    "tutor":        {"slug": "tutor",        "name": "Tutors",               "icon": "📘", "desc": "Academic & skill coaching"},
    "photographer": {"slug": "photographer", "name": "Photographers",        "icon": "📷", "desc": "Events & portraits"},
    "technician":   {"slug": "technician",   "name": "Computer Technicians", "icon": "💻", "desc": "Repairs & setup"},
}

# Placeholder providers until the `service_providers` table is wired up (see schema.sql)
MOCK_PROVIDERS = [
    {"name": "Ravi Kumar", "initials": "RK", "location": "Madurai", "stars": "★★★★★", "reviews": 128},
    {"name": "Sundari Priya", "initials": "SP", "location": "Madurai", "stars": "★★★★★", "reviews": 96},
    {"name": "Manoj Vel", "initials": "MV", "location": "Trichy", "stars": "★★★★☆", "reviews": 74},
]


# ---------------- LOGIN PAGE ----------------
@app.route('/')
def login_page():
    return render_template('login.html')


# ---------------- LOGIN PROCESS ----------------
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        return redirect(url_for('home'))

    flash("Invalid email or password.", "error")
    return redirect(url_for('login_page'))


# ---------------- REGISTER PAGE ----------------
@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')


# ---------------- SAVE USER TO DATABASE ----------------
@app.route('/register', methods=['POST'])
def register_post():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    password = request.form['password']
    confirm_password = request.form.get('confirm_password')

    if password != confirm_password:
        flash("Passwords do not match.", "error")
        return redirect(url_for('register'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Reject duplicate emails
    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    if cursor.fetchone():
        conn.close()
        flash("An account with this email already exists.", "error")
        return redirect(url_for('register'))

    cursor.execute("""
        INSERT INTO users (name, email, phone, password)
        VALUES (%s, %s, %s, %s)
    """, (name, email, phone, password))
    conn.commit()

    new_user_id = cursor.lastrowid
    conn.close()

    # Log the new user in immediately and send them to the home page
    session['user_id'] = new_user_id
    session['user_name'] = name
    return redirect(url_for('home'))


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))


# ---------------- HOME PAGE ----------------
@app.route('/home')
def home():
    return render_template('home.html')


# ---------------- SERVICE CATEGORY MODULE ----------------
@app.route('/categories')
def categories():
    return render_template('categories.html', categories=CATEGORIES.values())


@app.route('/category/<name>')
def category_page(name):
    category = CATEGORIES.get(name)
    if not category:
        return redirect(url_for('categories'))
    return render_template('category_page.html', category=category, providers=MOCK_PROVIDERS)


# ---------------- SERVICE REQUEST MODULE ----------------
@app.route('/request/<name>', methods=['GET', 'POST'])
def request_service(name):
    category = CATEGORIES.get(name)
    if not category:
        return redirect(url_for('categories'))

    if request.method == 'POST':
        if 'user_id' not in session:
            flash("Please login before requesting a service.", "error")
            return redirect(url_for('login_page'))

        provider_name = request.form['provider_name']
        address = request.form['address']
        preferred_date = request.form['preferred_date']
        details = request.form.get('details', '')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO service_requests
                (user_id, category, provider_name, address, preferred_date, details, status)
            VALUES (%s, %s, %s, %s, %s, %s, 'pending')
        """, (session['user_id'], category['name'], provider_name, address, preferred_date, details))
        conn.commit()
        conn.close()

        flash("Your service request has been submitted!", "success")
        return redirect(url_for('category_page', name=name))

    return render_template('service_request.html', category=category)


# ---------------- RUN APP ----------------
if __name__ == '__main__':
    app.run(debug=True)