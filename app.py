import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "change-this-to-a-random-secret-key" 

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
MOCK_PROVIDERS_BY_CATEGORY = {
    "electrician": [
        {"name": "Ravi Kumar", "initials": "RK", "location": "subhanagar", "stars": "★★★★★", "reviews": 128},
        {"name": "Suresh Babu", "initials": "SB", "location": "Kadalaiyur", "stars": "★★★★☆", "reviews": 82},
        {"name": "Arun Prakash", "initials": "AP", "location": "Indira Nagar", "stars": "★★★★★", "reviews": 61},
    ],
    "plumber": [
        {"name": "Manoj Vel", "initials": "MV", "location": "Subhanagar", "stars": "★★★★☆", "reviews": 74},
        {"name": "Dinesh Kumar", "initials": "DK", "location": "Aanandha Nagar", "stars": "★★★★★", "reviews": 110},
        {"name": "Vijayan S", "initials": "VS", "location": "Lakshmipuram", "stars": "★★★★☆", "reviews": 45},
    ],
    "carpenter": [
        {"name": "Muthu Raj", "initials": "MR", "location": "Loyal Mill Colony", "stars": "★★★★★", "reviews": 93},
        {"name": "Selvam K", "initials": "SK", "location": "Jothi Nagar", "stars": "★★★★☆", "reviews": 58},
        {"name": "Ganesan P", "initials": "GP", "location": "", "VOC Nagar": "★★★★★", "reviews": 71},
    ],
    "beautician": [
        {"name": "Sundari Priya", "initials": "SP", "location": "Maravar Colony", "stars": "★★★★★", "reviews": 96},
        {"name": "Kavitha Raj", "initials": "KR", "location": "Innam Maniyachi", "stars": "★★★★★", "reviews": 140},
        {"name": "Meena Devi", "initials": "MD", "location": "Athaikondan", "stars": "★★★★☆", "reviews": 67},
    ],
    "tutor": [
        {"name": "Karthik S", "initials": "KS", "location": "Gandhinagar", "stars": "★★★★★", "reviews": 55},
        {"name": "Priya Dharshini", "initials": "PD", "location": "Srinivasa Nagar", "stars": "★★★★☆", "reviews": 38},
        {"name": "Anand Babu", "initials": "AB", "location": "Trichy", "stars": "★★★★★", "reviews": 84},
    ],
    "photographer": [
        {"name": "Vignesh R", "initials": "VR", "location": "Subha Nagar", "stars": "★★★★★", "reviews": 102},
        {"name": "Nithya Sri", "initials": "NS", "location": "Appaneri", "stars": "★★★★☆", "reviews": 49},
        {"name": "Kishore Kumar", "initials": "KK", "location": "Elluppaiyurani", "stars": "★★★★★", "reviews": 76},
    ],
    "technician": [
        {"name": "Bala Murugan", "initials": "BM", "location": "Kamaraj Nagar", "stars": "★★★★☆", "reviews": 63},
        {"name": "Ramesh Chandra", "initials": "RC", "location": "Venkateshwara Garden", "stars": "★★★★★", "reviews": 118},
        {"name": "Senthil Kumar", "initials": "SK", "location": "Alagar Nagar", "stars": "★★★★☆", "reviews": 41},
    ],
}
# ---------------- USER DASHBOARD ----------------
@app.route('/dashboard')
def user_dashboard():
    if 'user_id' not in session:
        flash("Please login to view your dashboard.", "error")
        return redirect(url_for('login_page'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM service_requests
        WHERE user_id = %s
        ORDER BY id DESC
    """, (session['user_id'],))
    requests = cursor.fetchall()

    total = len(requests)
    pending = len([r for r in requests if r['status'] == 'pending'])
    accepted = len([r for r in requests if r['status'] == 'accepted'])
    completed = len([r for r in requests if r['status'] == 'completed'])

    conn.close()

    return render_template(
        'user_dashboard.html',
        requests=requests,
        total=total,
        pending=pending,
        accepted=accepted,
        completed=completed
    )
# ---------------- ADMIN LOGIN ----------------
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:

            session['admin'] = username
            return redirect(url_for('admin_dashboard'))

        flash("Invalid Admin Username or Password", "error")

    return render_template('admin_login.html')

#---------------Admin dashboard----------

@app.route('/admin/dashboard')
def admin_dashboard():

    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) total FROM users")
    total_users = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) total FROM service_providers")
    total_providers = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) total FROM service_providers WHERE status='pending'")
    pending = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) total FROM service_providers WHERE status='approved'")
    approved = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) total FROM service_requests")
    requests = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) total FROM categories")
    categories = cursor.fetchone()['total']

    conn.close()

    return render_template(
        "admin_dashboard.html",
        users=total_users,
        providers=total_providers,
        pending=pending,
        approved=approved,
        requests=requests,
        categories=categories
    )
#----------MANAGE USERS-----------

@app.route('/admin/users')
def manage_users():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    conn.close()

    return render_template("manage_users.html", users=users)

#----------DELETE USERS------

@app.route('/admin/delete_user/<int:id>')
def delete_user(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id=%s",(id,))
    conn.commit()

    conn.close()

    return redirect(url_for('manage_users'))

#---------MANAGE PROVIDERS-------

@app.route('/admin/providers')
def manage_providers():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM service_providers")
    providers = cursor.fetchall()

    conn.close()

    return render_template("manage_providers.html",
                           providers=providers)

#----------APPROVE PROVIDERS---------

@app.route('/admin/approve/<int:id>')
def approve_provider(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE service_providers SET status='approved' WHERE id=%s",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for('manage_providers'))

#-------DELETE PROVIDERS-----------

@app.route('/admin/delete_provider/<int:id>')
def delete_provider(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM service_providers WHERE id=%s",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for('manage_providers'))

#----------MANAGE CATEGORIES---------

@app.route('/admin/categories')
def manage_categories():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM categories")

    categories = cursor.fetchall()

    conn.close()

    return render_template("manage_categories.html",
                           categories=categories)

#------------MANAGE REQUEST----------------
@app.route('/admin/requests')
def manage_requests():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM service_requests")

    requests = cursor.fetchall()

    conn.close()

    return render_template("manage_requests.html",
                           requests=requests)

#_________ADMIN LOGOUT------

@app.route('/admin/logout')
def admin_logout():

    session.pop('admin', None)

    return redirect(url_for('admin_login'))


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
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT sp.*,
               COALESCE(AVG(r.rating), 0) AS avg_rating,
               COUNT(r.id) AS review_count
        FROM service_providers sp
        LEFT JOIN reviews r ON r.provider_id = sp.id
        WHERE sp.status = 'approved'
        GROUP BY sp.id
        ORDER BY avg_rating DESC, review_count DESC
        LIMIT 3
    """)
    featured_providers = cursor.fetchall()

    conn.close()

    return render_template('home.html', featured_providers=featured_providers)

# ---------------- PROVIDER LOGIN PAGE ----------------
@app.route('/provider/login', methods=['GET'])
def provider_login_page():
    return render_template('provider_login.html')

# ---------------- PROVIDER LOGIN PROCESS ----------------
@app.route('/provider/login', methods=['POST'])
def provider_login():
    email = request.form['email']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM service_providers WHERE email = %s AND password = %s",
        (email, password)
    )
    provider = cursor.fetchone()

    if not provider:
        conn.close()
        flash("Invalid provider email or password.", "error")
        return redirect(url_for('provider_login_page'))

    if provider['status'] != 'approved':
        conn.close()
        flash("Your account is pending admin approval.", "error")
        return redirect(url_for('provider_login_page'))

    session['user_id'] = provider['id']
    session['user_name'] = provider['name']
    session['user_email'] = provider['email']
    session['user_phone'] = provider['phone']
    session['role'] = 'provider'

    conn.close()
    return redirect(url_for('provider_dashboard'))

# ---------------- PROVIDER DASHBOARD ----------------
@app.route('/provider/dashboard')
def provider_dashboard():
    if session.get('role') != 'provider':
        flash("Please login as a service provider to continue.", "error")
        return redirect(url_for('provider_login_page'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM service_providers WHERE id = %s
    """, (session['user_id'],))
    provider = cursor.fetchone()
    conn.close()

    return render_template('provider_dashboard.html', provider=provider)

# ---------------- PROVIDER REGISTER PAGE ----------------
@app.route('/provider/register', methods=['GET'])
def provider_register():
    return render_template('provider_register.html', categories=CATEGORIES.values())


# ---------------- SAVE PROVIDER TO DATABASE ----------------
@app.route('/provider/register', methods=['POST'])
def provider_register_post():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    business_name = request.form['business_name']
    password = request.form['password']
    confirm_password = request.form.get('confirm_password')
    category = request.form['category']
    city = request.form['location']
    area = request.form['location']
    experience = request.form.get('experience') or 0

    if password != confirm_password:
        flash("Passwords do not match.", "error")
        return redirect(url_for('provider_register'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Check duplicate email
    cursor.execute(
        "SELECT id FROM service_providers WHERE email = %s",
        (email,)
    )

    if cursor.fetchone():
        conn.close()
        flash("An account with this email already exists.", "error")
        return redirect(url_for('provider_register'))

    cursor.execute("""
        INSERT INTO service_providers
        (name, email, phone, password, category, city, area, experience, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'pending')
    """, (
        name,
        email,
        phone,
        password,
        category,
        city,
        area,
        experience
    ))

    conn.commit()
    conn.close()

    flash("Registration successful! Waiting for admin approval.", "success")
    return redirect(url_for('provider_login_page'))

# ---------------- PROVIDER LOGOUT ----------------
@app.route('/provider/logout')
def provider_logout():
    session.clear()
    return redirect(url_for('provider_login_page'))
@app.route('/provider/request/<int:id>/update/<status>')
def update_request_status(id, status):
    if session.get('role') != 'provider':
        return redirect(url_for('provider_login_page'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE service_requests SET status=%s WHERE id=%s", (status, id))
    conn.commit()
    conn.close()

    return redirect(url_for('provider_dashboard'))


# ---------------- SERVICE CATEGORY MODULE ----------------
@app.route('/categories')
def categories():
    return render_template('categories.html', categories=CATEGORIES.values())


@app.route('/category/<name>')
def category_page(name):
    category = CATEGORIES.get(name)
    if not category:
        return redirect(url_for('categories'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM service_providers
        WHERE category = %s AND status = 'approved'
    """, (name,))
    db_providers = cursor.fetchall()
    conn.close()

    # Turn real DB rows into the same shape the template expects
    real_providers = []
    for p in db_providers:
        initials = "".join([w[0].upper() for w in p['name'].split()][:2])
        real_providers.append({
            "name": p['name'],
            "initials": initials,
            "location": p.get('area') or p.get('city') or "",
            "stars": "★★★★★",
            "reviews": 0
        })

    mock_providers = MOCK_PROVIDERS_BY_CATEGORY.get(name, [])
    providers = real_providers + mock_providers

    return render_template('category_page.html', category=category, providers=providers)

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

#----------MANAGE REVIEWS-----------

@app.route('/admin/reviews')
def manage_reviews():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM reviews")
    reviews = cursor.fetchall()

    conn.close()

    return render_template(
        "manage_reviews.html",
        reviews=reviews
    )


#----------DELETE REVIEW-----------

@app.route('/admin/delete_review/<int:id>')
def delete_review(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM reviews WHERE id=%s",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for('manage_reviews'))

#----------DELETE CATEGORY-----------

@app.route('/admin/delete_category/<int:id>')
def delete_category(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM categories WHERE id=%s",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for('manage_categories'))

#----------ADD CATEGORY-----------

@app.route('/admin/add_category', methods=['POST'])
def add_category():

    category_name = request.form['category_name']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO categories(category_name) VALUES(%s)",
        (category_name,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('manage_categories'))

# ---------------- SUBMIT REVIEW ----------------
@app.route('/provider/<int:provider_id>/review', methods=['GET', 'POST'])
def submit_review(provider_id):

    if 'user_id' not in session:
        flash("Please login before leaving a review.", "error")
        return redirect(url_for('login_page'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM service_providers WHERE id = %s", (provider_id,))
    provider = cursor.fetchone()

    if not provider:
        conn.close()
        flash("Provider not found.", "error")
        return redirect(url_for('categories'))

    if request.method == 'POST':
        rating = request.form.get('rating')
        comment = request.form.get('comment', '').strip()

        if not rating or not comment:
            conn.close()
            flash("Please give a star rating and a comment.", "error")
            return redirect(url_for('submit_review', provider_id=provider_id))

        cursor.execute("""
            INSERT INTO reviews (provider_id, user_id, customer_name, rating, comment)
            VALUES (%s, %s, %s, %s, %s)
        """, (provider_id, session['user_id'], session['user_name'], rating, comment))
        conn.commit()
        conn.close()

        flash("Thank you for your review!", "success")
        return redirect(url_for('submit_review', provider_id=provider_id))

    # Real average rating + review count for this provider (fixes header always
    # showing the hardcoded 4.8 / 128 placeholder)
    cursor.execute("""
        SELECT COALESCE(AVG(rating), 0) AS avg_rating, COUNT(*) AS review_count
        FROM reviews WHERE provider_id = %s
    """, (provider_id,))
    stats = cursor.fetchone()
    provider['avg_rating'] = round(float(stats['avg_rating']), 1)
    provider['review_count'] = stats['review_count']

    # NOTE: aliased as current_user_name (not customer_name) so it does NOT
    # overwrite the customer_name already stored on the review row at
    # submission time -- keeps the reviewer's name as it was when they posted
    cursor.execute("""
        SELECT r.*, u.name AS current_user_name
        FROM reviews r
        LEFT JOIN users u ON r.user_id = u.id
        WHERE r.provider_id = %s
        ORDER BY r.id DESC
    """, (provider_id,))
    reviews = cursor.fetchall()

    conn.close()

    return render_template('review_provider.html', provider=provider, reviews=reviews)
# ---------------- CHECK ROUTES ----------------
print(app.url_map)

# ---------------- RUN APP ----------------
if __name__ == '__main__':
    app.run(debug=True)
