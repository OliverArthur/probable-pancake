from app.infrastructure.framework.server import start_server


def server():
    start_server()


def black():
    import subprocess

    subprocess.call(["black", "app"])


def isort():
    import subprocess

    subprocess.call(["isort", "app"])


def flake8():
    import subprocess

    subprocess.call(["flake8", "app"])


def mypy():
    import subprocess

    subprocess.call(["mypy", "app"])