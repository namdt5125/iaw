from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from database import get_db

app = FastAPI()


@app.get("/ping")
def ping():
    return "pong"


@app.get("/login-form", response_class=HTMLResponse)
def login_form():
    with open("templates/login.html", "r", encoding="utf-8") as f:
        return f.read()


@app.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...)
):
    db = get_db()

    user = db.execute(
        "SELECT id, username FROM users WHERE username = ? AND password = ?",
        (username, password)
    ).fetchone()

    db.close()

    if user:
        response = RedirectResponse(
            url="/index",
            status_code=303
        )

        response.set_cookie(
            key="session",
            value=str(user["id"]),
            httponly=True
        )

        return response

    return HTMLResponse(
        """
        <h2>Login failed</h2>
        <p>Invalid username or password.</p>
        <a href="/login-form">Back to login</a>
        """,
        status_code=401
    )


@app.get("/index", response_class=HTMLResponse)
def index(request: Request):
    session = request.cookies.get("session")

    if not session:
        return RedirectResponse(
            url="/login-form",
            status_code=303
        )

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Index</title>
    </head>
    <body>
        <h1>Login success</h1>
        <p>Welcome to the index page.</p>
        <a href="/logout">Logout</a>
    </body>
    </html>
    """


@app.get("/logout")
def logout():
    response = RedirectResponse(
        url="/login-form",
        status_code=303
    )

    response.delete_cookie("session")

    return response


