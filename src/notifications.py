import subprocess

# Notification про тривогу libnotify
def send_notification(title: str, message: str):
    subprocess.run([
        "notify-send",
        title,
        message
    ])
def missile_near_notification(title: str, message: str, picture: str, app: str):
    subprocess.run([
        "notify-send",
        title,
        message,
        picture,
        app
    ])
def alert_notification(title: str, message: str, picture: str, app: str):
    subprocess.run([
        "notify-send",
        title,
        message,
        picture,
        app
    ])