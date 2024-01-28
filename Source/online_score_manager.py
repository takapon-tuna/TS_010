import pyrebase
from cryptography.fernet import Fernet

# Firebaseの設定
config = {
    "apiKey": "apiKey",
    "authDomain": "projectId.firebaseapp.com",
    "databaseURL": "https://databaseName.firebaseio.com",
    "storageBucket": "projectId.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()

# プレイヤー名とスコアをFirebaseに送信する関数


def send_score_to_firebase(player_name, score):
    # 匿名認証でUIDを取得
    user = auth.sign_in_anonymous()
    uid = user['localId']

    # スコアとプレイヤーネームをデータベースに送信
    data = {"name": player_name, "score": score, "uid": uid}
    db.child("scores").push(data)

# プレイヤー名を復号化する関数


def decrypt_player_name():
    try:
        with open('data/iziruna.key', 'rb') as keyfile:
            key = keyfile.read()
        cipher_suite = Fernet(key)
        with open('data/player_name.json', 'rb') as file:
            encrypted_name = file.read()
        decrypted_name = cipher_suite.decrypt(encrypted_name).decode('utf-8')
        return decrypted_name
    except (FileNotFoundError, ValueError, json.decoder.JSONDecodeError):
        return "Unknown Player"
