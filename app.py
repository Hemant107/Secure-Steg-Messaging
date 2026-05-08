import os
import uuid
import threading
import webbrowser

from flask import Flask, render_template, request, send_file, redirect, url_for, session, jsonify
from werkzeug.utils import secure_filename

from stego import encode_bytes_into_image, decode_bytes_from_image
import aes_utils
from db_utils import add_history, get_history, init_db

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'outputs')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.secret_key = 'my_super_secure_random_string_12345'

init_db()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'bmp'}


def make_display_name(raw: str) -> str:
    if not raw:
        return "User"
    if '@' in raw:
        return raw.split('@')[0].capitalize()
    return raw.capitalize()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if email and password:
            session['logged_in'] = True
            session['username'] = email
            session['display_name'] = make_display_name(email)
            return redirect(url_for('dashboard'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('dashboard.html')


@app.route('/encrypt', methods=['POST'])
def encrypt():
    if not session.get('logged_in'):
        return jsonify(success=False, error="Unauthorized"), 401

    file = request.files.get('image')
    message = request.form.get('message', '').strip()
    password = request.form.get('password', '').strip()

    if not file or file.filename == '':
        return jsonify(success=False, error="Image is required"), 400

    if not message:
        return jsonify(success=False, error="Message is required"), 400

    if not password:
        return jsonify(success=False, error="Password is required"), 400

    if not allowed_file(file.filename):
        return jsonify(success=False, error="Invalid file type. Use PNG, JPG, JPEG, or BMP"), 400

    try:
        original_name = secure_filename(file.filename)
        file_ext = os.path.splitext(original_name)[1].lower()
        unique_id = uuid.uuid4().hex

        input_name = f"upload_{unique_id}{file_ext}"
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_name)
        file.save(input_path)

        # Always save encoded output as PNG because JPEG is lossy
        output_name = f"encoded_{unique_id}.png"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_name)

        encrypted_payload = aes_utils.encrypt_bytes_with_password(
            message.encode('utf-8'),
            password
        )

        encode_bytes_into_image(input_path, encrypted_payload, output_path)

        add_history(session['username'], 'encrypt', output_name)

        return jsonify(
            success=True,
            download_url=url_for('download_file', filename=output_name)
        ), 200

    except Exception as e:
        print(f"[ENCRYPT ERROR] {e}")
        return jsonify(success=False, error=f"Encryption Error: {str(e)}"), 500


@app.route('/decrypt', methods=['POST'])
def decrypt():
    if not session.get('logged_in'):
        return jsonify(success=False, error="Unauthorized"), 401

    file = request.files.get('image')
    password = request.form.get('password', '').strip()

    if not file or file.filename == '':
        return jsonify(success=False, error="Image is required"), 400

    if not password:
        return jsonify(success=False, error="Password is required"), 400

    if not allowed_file(file.filename):
        return jsonify(success=False, error="Invalid file type. Use PNG, JPG, JPEG, or BMP"), 400

    try:
        original_name = secure_filename(file.filename)
        file_ext = os.path.splitext(original_name)[1].lower()
        unique_id = uuid.uuid4().hex

        input_name = f"decrypt_{unique_id}{file_ext}"
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_name)
        file.save(input_path)

        encrypted_data = decode_bytes_from_image(input_path)
        decrypted_data = aes_utils.decrypt_bytes_with_password(encrypted_data, password)

        if isinstance(decrypted_data, bytes):
            message = decrypted_data.decode('utf-8', errors='replace')
        else:
            message = str(decrypted_data)

        add_history(session['username'], 'decrypt', original_name)

        return jsonify(success=True, message=message), 200

    except Exception as e:
        print(f"[DECRYPT ERROR] {e}")
        return jsonify(success=False, error="Incorrect password or no hidden message found."), 400


@app.route('/download/<filename>')
def download_file(filename):
    path = os.path.join(app.config['OUTPUT_FOLDER'], filename)

    if not os.path.exists(path):
        return jsonify(success=False, error="File not found"), 404

    return send_file(
        path,
        as_attachment=True,
        download_name=filename,
        mimetype='image/png'
    )


@app.route('/history')
def history():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    records = get_history(session['username'])
    return render_template(
        'history.html',
        history=records,
        display_name=session.get('display_name')
    )


def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")


if __name__ == '__main__':
    threading.Timer(1, open_browser).start()
    app.run(debug=True)
