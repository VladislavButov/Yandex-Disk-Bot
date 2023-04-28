from flask import Flask, redirect, request

app = Flask(__name__)


@app.route('/')
def redirect_to_bot():
    code = request.args.get('code', '')
    return redirect(f'https://t.me/YandexDisk_TGBot?start={code}')


if __name__ == '__main__':
    app.run()