# Secure-Steg-Messaging

📌 Project Overview

Secure-Steg-Messaging is a secure communication system that hides confidential messages inside images using Steganography and protects the hidden data using AES Encryption.
The project is developed using Python Flask with a modern web interface for secure encoding and decoding of hidden messages.

This project ensures secure communication without revealing sensitive information to third parties.

🚀 Features
🔒 Password Protected Messaging
🖼️ Image Steganography
🔐 AES Encryption Security
📤 Encode Secret Messages into Images
📥 Decode Hidden Messages from Images
🌐 Flask-Based Web Interface
💾 SQLite Database Support
📜 Message History Management
⚡ Fast & Secure Processing
📱 Responsive UI Design
🛠️ Technologies Used
Frontend
HTML5
CSS3
JavaScript
Backend
Python
Flask
Database
SQLite
Security
AES Encryption
Image Steganography
📂 Project Structure
Secure-Steg-Messaging/
│
├── static/                 # CSS, JS, Images
├── templates/              # HTML Templates
├── uploads/                # Uploaded Images
├── output/                 # Encoded Images
├── app.py                  # Main Flask App
├── stego.py                # Steganography Logic
├── aes_utils.py            # AES Encryption Functions
├── db_utils.py             # Database Functions
├── requirements.txt        # Required Libraries
└── README.md
⚙️ Software Requirements

Before running the project, install the following software:

✅ Required Software
Software	Version
Python	3.9 or above
pip	Latest
Git	Optional
📦 Required Python Libraries

Install these libraries using pip:

pip install flask pillow pycryptodome

Or install all dependencies using:

pip install -r requirements.txt
📝 requirements.txt

Create a requirements.txt file and add:

Flask
Pillow
pycryptodome
⚙️ Installation & Setup Guide
1️⃣ Clone the Repository
git clone https://github.com/your-username/Secure-Steg-Messaging.git
2️⃣ Open Project Folder
cd Secure-Steg-Messaging
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Run the Application
python app.py
5️⃣ Open in Browser

After running the server, open:
http://127.0.0.1:5000

▶️ How to Use the Project
🔐 Encode Message
Open the web application
Upload an image
Enter secret message
Enter password
Click Encode
Download encoded image
🔓 Decode Message
Upload encoded image
Enter correct password
Click Decode
Hidden message will appear
🔐 How Security Works
AES Encryption

Before hiding the message:

Text is encrypted using AES encryption
Password is required for decryption
Steganography
Encrypted data is hidden inside image pixels
Image looks normal to others
Only authorized users can decode the hidden data

🎯 Project Objectives
Secure communication using images
Protect confidential information
Prevent unauthorized data access
Combine cryptography with steganography
Create a user-friendly secure platform

🔮 Future Enhancements
User Login & Authentication
Secure Cloud Storage
Video & Audio Steganography
AI-Based Security Monitoring
Mobile Application Version
Real-Time Secure Chat
📸 Screenshots
<img width="1876" height="965" alt="SS1" src="https://github.com/user-attachments/assets/cf7f3177-da48-44ac-8d30-27571895e4ca" />
<img width="1886" height="973" alt="SS2" src="https://github.com/user-attachments/assets/16912be0-ba02-4d0e-b425-ded4aed21913" />
<img width="1902" height="962" alt="SS3" src="https://github.com/user-attachments/assets/c6abd6aa-5b0b-492e-b5a1-23a9883167b3" />
<img width="1892" height="962" alt="SS4" src="https://github.com/user-attachments/assets/1e47f094-2288-4063-951c-f2a6aef185c9" />
<img width="1903" height="972" alt="SS5" src="https://github.com/user-attachments/assets/c12a4e2f-9900-4268-a9f8-dd8c795787b9" />
<img width="1898" height="968" alt="SS6" src="https://github.com/user-attachments/assets/d883b167-45b5-408b-bce8-6dd2a198fa8f" />






👨‍💻 Author
Hemant Chauhan
BCA Final Year Student

📄 License
This project is created for educational and academic purposes.

⭐ Support

If you like this project, give it a ⭐ on GitHub.
