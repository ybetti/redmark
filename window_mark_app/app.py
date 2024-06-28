from flask import Flask, render_template, jsonify, request
import pygetwindow as gw
from PIL import ImageGrab
import numpy as np
import cv2

app = Flask(__name__)

def get_window_image(window_title):
    windows = gw.getWindowsWithTitle(window_title)
    if not windows:
        return None
    window = windows[0]
    bbox = (window.left, window.top, window.right, window.bottom)
    screenshot = ImageGrab.grab(bbox)
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

def detect_red(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    return mask

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_windows')
def get_windows():
    windows = gw.getAllTitles()
    return jsonify(windows)

@app.route('/get_window_image', methods=['POST'])
def get_window_image_route():
    window_title = request.json.get('window_title')
    image = get_window_image(window_title)
    if image is None:
        return jsonify({'error': 'Window not found'}), 404

    mask = detect_red(image)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    _, buffer = cv2.imencode('.jpg', image)
    return jsonify({'image': buffer.tobytes().hex()})

if __name__ == '__main__':
    app.run(debug=True)
