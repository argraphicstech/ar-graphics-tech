from flask import Flask, render_template, request
import os

app = Flask(__name__)

# =========================
# HOME PAGE
# =========================
@app.route('/')
def home():
    return render_template('index.html')


# =========================
# SUBMIT FORM (SAVE DATA)
# =========================
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    mobile = request.form.get('mobile')
    date = request.form.get('date')
    message = request.form.get('message')

    # Validate all fields
    if not name or not mobile or not date or not message:
        return "❌ Please fill all fields!"

    # Save data
    with open("data.txt", "a") as f:
        f.write(f"{name},{mobile},{date},{message}\n")

    return """
    <h2 style='text-align:center;'>✅ Submitted Successfully!</h2>
    <div style='text-align:center; margin-top:20px;'>
        <a href='/' style='padding:10px 20px; background:#00e5ff; color:black; text-decoration:none; border-radius:10px;'>Go Back</a>
    </div>
    """


# =========================
# SHOW DATA ON WEBSITE
# =========================
@app.route('/data')
def data():
    customers = []

    try:
        with open("data.txt", "r") as f:
            for line in f:
                name, mobile, date, message = line.strip().split(",")
                customers.append((name, mobile, date, message))
    except Exception as e:
        print("Error:", e)

    return render_template("data.html", customers=customers)


# =========================
# PASSWORD PROTECTED DELETE
# =========================
@app.route('/clear')
def clear():
    return '''
    <h2 style="text-align:center;">🔐 Enter Password to Delete Data</h2>
    <form action="/delete_data" method="POST" style="text-align:center;">
        <input type="password" name="password" placeholder="Enter Password" required>
        <br><br>
        <button type="submit">Delete Data</button>
    </form>
    '''


@app.route('/delete_data', methods=['POST'])
def delete_data():
    password = request.form.get('password')

    if password == "admin123":  # 🔐 Change your password here
        open("data.txt", "w").close()
        return '''
        <h2 style="text-align:center;">✅ Data Deleted Successfully!</h2>
        <div style="text-align:center;">
            <a href="/">Go Back</a>
        </div>
        '''
    else:
        return '''
        <h2 style="text-align:center; color:red;">❌ Wrong Password!</h2>
        <div style="text-align:center;">
            <a href="/clear">Try Again</a>
        </div>
        '''


# =========================
# RUN SERVER (PRODUCTION READY)
# =========================
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)