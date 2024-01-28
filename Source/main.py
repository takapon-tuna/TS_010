import pyrebase
from framework_class import Framework
from name_input_scene import NameInputScene


# Firebaseの設定
config = {
    "apiKey": "AIzaSyBfOq3EV7InsWSZ2QlDA9xjf0q-17c8mWw",
    "authDomain": "game-inport-taka.firebaseapp.com",
    "databaseURL": "https://game-inport-taka-default-rtdb.firebaseio.com",
    "projectId": "game-inport-taka",
    "storageBucket": "game-inport-taka.appspot.com",
    "messagingSenderId": "291166917129",
    "appId": "1:291166917129:web:920a7cd8ea953dbaf49ed8",
    "measurementId": "G-JMD1X9X0SZ"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
# メイン関数


def main():
    if __name__ == "__main__":
        framework = Framework(firebase, auth)  # フレームワークのインスタンスを作成
        framework.run()  # フレームワークのメインループを実行


# このスクリプトが直接実行された場合にmain関数を呼び出す
if __name__ == "__main__":
    main()  # メイン関数を実行
