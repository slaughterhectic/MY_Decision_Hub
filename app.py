from flask import Flask, render_template, request, redirect, url_for
import openai

app = Flask(__name__)

# In-memory storage (replace this with a database in a real app)
users = {'admin': 'adminpass', 'user1': 'userpass', 'user2': 'userpass'}
user_queries = {}

openai.api_key = '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'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username in users and users[username] == password:
        if username == 'admin':
            return redirect(url_for('admin_dashboard', username=username))
        else:
            return redirect(url_for('user_dashboard', username=username))
    else:
        return redirect(url_for('index'))

@app.route('/user_dashboard/', methods=['GET', 'POST'])
def user_dashboard():
    username = request.args.get('username')
    if username != 'admin':
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
                    engine="text-davinci-003",
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

            return redirect(url_for('user_dashboard', username=username))

        return render_template('user_dashboard.html', username=username, data=user_queries[username])
    else:
        return "Permission denied"

@app.route('/admin_dashboard/', methods=['GET', 'POST'])
def admin_dashboard():
    username = request.args.get('username')
    if username == 'admin':
        if request.method == 'POST':
            message = request.form.get('message')
            recipient = request.form.get('recipient')

            if recipient == 'all':
                # Admin sends a message to all users
                for user in user_queries:
                    user_queries[user]['responses'].append(f"\nAdmin: {message}")
            else:
                # Admin sends a message to a specific user
                user_queries[recipient]['responses'].append(f"\nAdmin: {message}")

            return redirect(url_for('admin_dashboard', username=username))

        return render_template('admin_dashboard.html', username=username, data=user_queries)
    else:
        return "Permission denied"

if __name__ == '__main__':
    app.run(debug=True)
