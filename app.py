from flask import Flask, render_template, request, redirect, url_for
import openai
from unicodedata import name
from flask import Flask, render_template, request, flash, redirect, url_for, session
from firebase import signup, signin, auth
from flask import Flask, render_template, request, flash, redirect, url_for, session
import os
app = Flask(__name__)

# In-memory storage (replace this with a database in a real app)

user_queries = {}

openai.api_key = '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'

app.secret_key = os.urandom(24)



# ... (previous code remains unchanged)
@app.route("/", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect_dashboard(session["user"])

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email and password:
            message, category = signin(email, password)

            if message is not None and category is not None:
                session["user"] = email
                if category == "success":
                    if message == "email not verified":
                        flash("Check your e-mail to do an email verification")
                        return redirect(url_for("user_dashboard", username=email))

                    return redirect_dashboard(email)
                else:
                    flash(message)
            else:
                flash("An unexpected error occurred during login")
        else:
            flash("Please, enter email and password")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user")
    return redirect(url_for("login"))

@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    if "user" in session:
        return redirect_dashboard(session["user"])

    if request.method == "POST":
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if password1 != password2:
            flash("Both password should be same", category="error")
        else:
            message, category = signup(email, password1)
            if category == "success":
                return render_template("verify_email.html")
            else:
                flash(message)

    return render_template("sign_up.html")

# ... (previous code remains unchanged)

# Helper function to redirect to the appropriate dashboard based on the email
# Helper function to redirect to the appropriate dashboard based on the email
def redirect_dashboard(email):
    if 'admin' in email:

        return redirect(url_for("admin_dashboard", username=email))
    else:
        return redirect(url_for("user_dashboard", username=email))





@app.route('/user_dashboard/', methods=['GET', 'POST'])
def user_dashboard():
    username = session.get('user')

    if username and 'admin' not in username:
        if username not in user_queries:
            user_queries[username] = {}  # Update to store queries and responses separately

        if request.method == 'POST':
            recipient = request.form.get('recipient')
            message = request.form.get('message')

            if recipient == 'admin':
                # Store user query and admin response separately
                if 'queries' not in user_queries[username]:
                    user_queries[username]['queries'] = []
                user_queries[username]['queries'].append(f"{username}: {message}")
                # Add a placeholder for admin response, to be updated later
                if 'responses' not in user_queries[username]:
                    user_queries[username]['responses'] = [f"Admin: Response to '{message}' will appear here."]
            elif recipient == 'openai':
                # Send the query to ChatGPT using the OpenAI API
                openai_response = openai.Completion.create(
                    engine="gpt-3.5-turbo-instruct",
                    prompt=message,
                    max_tokens=100
                )
                # Store user query and ChatGPT response separately
                if 'queries' not in user_queries[username]:
                    user_queries[username]['queries'] = []
                user_queries[username]['queries'].append(f"{username}: {message}")
                if 'responses' not in user_queries[username]:
                    user_queries[username]['responses'] = []
                user_queries[username]['responses'].append(f"OpenAI: {openai_response['choices'][0]['text']}")

            return redirect(url_for('user_dashboard'))

        return render_template('user_dashboard.html', username=username, data=user_queries[username])
    else:
        flash("Permission denied. You must be a regular user to access this page.")
        return redirect(url_for("login"))



@app.route('/admin_dashboard/', methods=['GET', 'POST'])
def admin_dashboard():
    username = session.get('user')

    if username and 'admin' in username:
        if request.method == 'POST':
            message = request.form.get('message')
            recipient = request.form.get('recipient')

            if recipient == 'all':
                # Admin sends a message to all users
                for user in user_queries:
                    if 'responses' not in user_queries[user]:
                        user_queries[user]['responses'] = []
                    user_queries[user]['responses'].append(f"\nAdmin: {message}")
            else:
                # Admin sends a message to a specific user
                if recipient in user_queries and 'responses' not in user_queries[recipient]:
                    user_queries[recipient]['responses'] = []
                user_queries[recipient]['responses'].append(f"\nAdmin: {message}")

            return redirect(url_for('admin_dashboard'))

        return render_template('admin_dashboard.html', username=username, data=user_queries)
    else:
        return redirect(url_for("login"))


if __name__ == "__main__":

    app.run(debug=True)