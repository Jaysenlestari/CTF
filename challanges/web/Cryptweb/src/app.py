import os
import sqlite3
import secrets
import uuid
from pathlib import Path

from flask import Flask, request, redirect, render_template, url_for, jsonify, make_response

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import HMAC, SHA256

app = Flask(__name__)

FLAG = os.environ.get("FLAG", "NETSOS{FAKEFLAG}")
DATABASE = os.environ.get("DATABASE_PATH", "/data/football.db")
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "botadmin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "botadminpass")

AES_KEY = os.urandom(16)
SIGN_KEY = os.urandom(16)

AUTH_COOKIE = "auth"
IV_COOKIE = "iv"

db_dir = os.path.dirname(DATABASE)
if db_dir:
    Path(db_dir).mkdir(parents=True, exist_ok=True)


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    db = get_db()

    db.execute(
        """
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            body TEXT NOT NULL
        )
        """
    )

    db.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER NOT NULL DEFAULT 0
        )
        """
    )

    user_cols = {row["name"] for row in db.execute("PRAGMA table_info(users)").fetchall()}
    if "is_admin" not in user_cols:
        db.execute("ALTER TABLE users ADD COLUMN is_admin INTEGER NOT NULL DEFAULT 0")
        db.commit()

    db.execute(
        """
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            message TEXT NOT NULL
        );
        """
    )

    cols = {row["name"] for row in db.execute("PRAGMA table_info(reviews)").fetchall()}
    if "uuid" not in cols:
        db.execute("ALTER TABLE reviews ADD COLUMN uuid TEXT UNIQUE")
        existing = db.execute("SELECT id FROM reviews").fetchall()
        for row in existing:
            db.execute(
                "UPDATE reviews SET uuid=? WHERE id=?",
                (uuid.uuid4().hex, row["id"]),
            )
        db.commit()

    admin_exists = db.execute(
        "SELECT 1 FROM users WHERE username=?", (ADMIN_USERNAME,)
    ).fetchone()
    if not admin_exists:
        db.execute(
            "INSERT INTO users(username, password, is_admin) VALUES (?,?,1)",
            (ADMIN_USERNAME, ADMIN_PASSWORD),
        )
        db.commit()

    count = db.execute("SELECT COUNT(*) AS c FROM articles").fetchone()["c"]
    if count == 0:
        db.executemany(
            "INSERT INTO articles(title, body) VALUES (?, ?)",
            [
                (
                    "Messi Cetak Hattrick di Final UCL",
                    "Lionel Messi kembali menunjukkan kelasnya dengan mencetak hattrick "
                    "di final melawan Manchester City. Lini belakang lawan dibuat kerepotan "
                    "sepanjang pertandingan.",
                ),
                (
                    "Real Madrid Juara La Liga",
                    "Real Madrid memastikan gelar juara La Liga setelah menang 3-1 atas "
                    "Barcelona di El Clásico. Gol penutup datang dari tendangan jarak jauh "
                    "di menit akhir.",
                ),
                (
                    "Erling Haaland Bikin Rekor Baru",
                    "Erling Haaland mencatatkan diri sebagai pemain pertama yang menembus "
                    "40 gol dalam satu musim Premier League. Rekor lama akhirnya patah.",
                ),
            ],
        )
        db.commit()

    db.close()


init_db()


def build_session(username: str, is_admin: bool = False):
    admin_flag = "1" if is_admin else "0"
    pt = f"is_admin={admin_flag};".encode()

    iv = os.urandom(16)
    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
    ct = cipher.encrypt(pad(pt, 16))

    mac = HMAC.new(SIGN_KEY, iv + ct, SHA256).digest()
    return iv.hex(), (ct + mac).hex()


def get_session_plaintext():
    auth_hex = request.cookies.get(AUTH_COOKIE)
    iv_hex = request.cookies.get(IV_COOKIE)

    if not auth_hex or not iv_hex:
        return None, render_template(
            "error.html", code=403, message="Missing session cookies"
        )

    try:
        raw = bytes.fromhex(auth_hex)
        iv = bytes.fromhex(iv_hex)
    except Exception:
        return None, render_template(
            "error.html", code=400, message="Malformed cookie (hex error)"
        )

    if len(raw) <= 32:
        return None, render_template(
            "error.html", code=400, message="Cookie too short for HMAC"
        )

    ct, mac = raw[:-32], raw[-32:]

    try:
        HMAC.new(SIGN_KEY, iv + ct, SHA256).verify(mac)
    except Exception:
        return None, render_template(
            "error.html", code=403, message="Invalid cookie signature"
        )

    try:
        pt = unpad(AES.new(AES_KEY, AES.MODE_CBC, iv).decrypt(ct), 16)
    except Exception as e:
        return None, render_template(
            "error.html", code=400, message=f"Decrypt error: {e}"
        )

    return pt, None


@app.route("/")
def index():
    db = get_db()
    arts = db.execute("SELECT id, title FROM articles").fetchall()
    db.close()
    return render_template("index.html", articles=arts)


@app.route("/article/<int:article_id>")
def article(article_id):
    db = get_db()
    art = db.execute("SELECT * FROM articles WHERE id = ?", (article_id,)).fetchone()
    db.close()
    if not art:
        return render_template("error.html", code=404, message="Article not found"), 404
    return render_template("article.html", art=art)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = request.form.get("username", "").strip()
        pw = request.form.get("password", "")

        if len(user) < 3 or len(pw) < 4:
            return render_template(
                "error.html", code=400, message="Invalid username/password"
            )

        db = get_db()
        try:
            db.execute(
                "INSERT INTO users(username, password, is_admin) VALUES (?, ?, 0)",
                (user, pw),
            )
            db.commit()
        except Exception:
            db.close()
            return render_template(
                "error.html", code=400, message="Username already taken"
            )

        db.close()
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("username", "").strip()
        pw = request.form.get("password", "")

        db = get_db()
        row = db.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?", (user, pw)
        ).fetchone()
        db.close()

        if not row:
            return render_template(
                "error.html", code=403, message="Wrong username/password"
            )

        iv_hex, cookie_hex = build_session(user, bool(row["is_admin"]))

        resp = make_response(render_template("login_success.html", username=user))
        resp.set_cookie(AUTH_COOKIE, cookie_hex, httponly=True, samesite="Lax")
        resp.set_cookie(IV_COOKIE, iv_hex, httponly=True, samesite="Lax")
        return resp

    return render_template("login.html")

@app.route("/review", methods=["GET", "POST"])
def review():
    db = get_db()

    if request.method == "POST":
        name = request.form.get("name", "Anonymous")
        msg = request.form.get("message", "")

        review_uuid = secrets.token_hex(16)
        db.execute(
            "INSERT INTO reviews(uuid, name, message) VALUES (?,?,?)",
            (review_uuid, name, msg),
        )
        db.commit()

        review_url = url_for("review", uuid=review_uuid, _external=True)
        db.close()
        return render_template("review_submitted.html", review_url=review_url)

    uuid_param = request.args.get("uuid")
    review_data = None

    if uuid_param:
        session_pt, error_response = get_session_plaintext()
        if error_response:
            db.close()
            return error_response

        if b"is_admin=1;" not in session_pt:
            db.close()
            return render_template("error.html", code=403, message="Admins only")

        review_data = db.execute(
            "SELECT name, message FROM reviews WHERE uuid=?", (uuid_param,)
        ).fetchone()

        if not review_data:
            db.close()
            return render_template("error.html", code=404, message="Review not found")

    response = render_template("review.html", review=review_data)
    db.close()
    return response


@app.route("/admin/reviews")
def admin_reviews():
    db = get_db()
    rows = db.execute("SELECT id, uuid, name FROM reviews ORDER BY id DESC").fetchall()
    db.close()
    return render_template("admin_reviews.html", reviews=rows)

@app.route("/internal/config")
def internal_config():
    session_pt, error_response = get_session_plaintext()
    if error_response:
        return error_response

    if b"is_admin=1;" not in session_pt:
        return render_template("error.html", code=403, message="Admins only")

    return jsonify(
        {
            "sign_key": SIGN_KEY.hex(),
            "note": "Internal HMAC key for session cookies.",
        }
    )

@app.route("/admin/dashboard")
def admin_dashboard():
    session_pt, error_response = get_session_plaintext()
    if error_response:
        return error_response

    if b"is_admin=1;" in session_pt:
        return render_template("admin_dashboard.html", flag=FLAG)

    return render_template("error.html", code=403, message="Admins only")


@app.errorhandler(404)
def notfound(_e):
    return render_template("error.html", code=404, message="Not Found"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
