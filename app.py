from app import create_app
from app.config import DevelopmentConfig, TestingConfig

app = create_app(DevelopmentConfig)
testapp = create_app(TestingConfig)


if __name__ == '__main__':
    app.run(port=8080)
