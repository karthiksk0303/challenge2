from flask import Flask, render_template, request, redirect, session, jsonify

app = Flask(__name__)
app.secret_key = "idor-ctf-secret-key"

# Challenge users
USERS = {
    "admin123": {
        "password": "admin123",
        "user_id": 1001
    }
}

# Documents belonging to different users
DOCUMENTS = {
    1001: {
        "owner": "admin123",
        "title": "Admin Private Notes",
        "content": "Welcome, admin. This is your private document."
    },
    1002: {
        "owner": "employee",
        "title": "Employee Confidential File",
        "content": "PSNACET{L0g1n_SuC33ss_An6_D0n3}"
    }
}


@app.route("/")
def index():
    if "username" in session:
        return redirect("/dashboard")
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        user = USERS.get(username)

        if user and user["password"] == password:
            session["username"] = username
            session["user_id"] = user["user_id"]
            return redirect("/dashboard")

        return render_template(
            "login.html",
            error="Invalid username or password"
        )

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        username=session["username"],
        user_id=session["user_id"]
    )


@app.route("/api/document/<int:document_id>")
def get_document(document_id):
    if "username" not in session:
        return jsonify({"error": "Authentication required"}), 401

    document = DOCUMENTS.get(document_id)

    if not document:
        return jsonify({"error": "Document not found"}), 404

    # INTENTIONALLY VULNERABLE:
    # There is NO ownership/authorization check here.
    return jsonify({
        "document_id": document_id,
        "title": document["title"],
        "owner": document["owner"],
        "content": document["content"]
    })


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
