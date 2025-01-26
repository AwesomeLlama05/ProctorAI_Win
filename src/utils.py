from PIL import ImageGrab
import os

def take_screenshot(filename='screenshot.png'):
    # Take a screenshot
    screenshot = ImageGrab.grab()
    # Save the screenshot to the same directory
    current_directory = os.getcwd()
    screenshot.save(os.path.join(current_directory, filename))