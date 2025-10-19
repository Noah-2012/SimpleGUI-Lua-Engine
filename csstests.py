from SimpleGUICSSParser import *

with open("style.css", "r", encoding="utf-8") as f:
    css_code = f.read()

parser = CSSParser()
parser.parse(css_code)

button = parser.get("button")

print(button.background_color)
print(hex_to_rgb(button.background_color))

window = parser.get("window")

print(window.border_radius)
print(px_to_int(window.border_radius))