from app import create_app, Config

app = create_app(Config)

if __name__ == '__main__':
    app.run()
