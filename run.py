from flask import Flask

from app import create_app


if __name__ == '__main__':
    app = create_app()
    Flask.run(app, host='127.0.0.2', port=5000, debug=True)





