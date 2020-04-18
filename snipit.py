from flask import Flask, send_file, render_template
from selenium import webdriver
from argparse import ArgumentParser
from uuid import uuid4
import json
import clipboard
import webbrowser
import logging
import os


def parse():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input', help='Generate Snippet From Input File')
    parser.add_argument('-o', '--output', help='Output File To Store Image. No need for file ext.')
    parser.add_argument('-l', '--language', help='Language for Syntax Highlighting. Supports highlight.js')
    parser.add_argument('-wh', '--window-height', help="Browser Height. Default: 1200")
    parser.add_argument('-ww', '--window-width', help="Browser Width. Default: 1600")
    parser.add_argument('-cb', '--clip-board', help='Generate Snippet From Clibboard', action='store_true')
    parser.add_argument('-bc', '--background-color', help='Background Color For HTML. Uses Hex Codes.')
    parser.add_argument('-bi', '--background-image', help='Path to background image for snippet.')
    parser.add_argument('-cc', '--codebox-color', help='Background Color for Codebox. Uses Hex Codes.')
    parser.add_argument('-ss', '--syntax-style', help='Syntax Color Style for Code. Supports highlight.js styles')
    parser.add_argument('-sc', '--style-config', help='Pass StyleConfig.json File As Snippet Style.')
    parser.add_argument('-z', '--zoom', help='Amount to Use for Zoom')
    return parser

parser = parse()
args = parser.parse_args()

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True
app.logger.disabled = True
has_opened = False

@app.route('/')
def render():
    default_color = "background-color: #292929"
    content = ""
    if args.clip_board:
        content = clipboard.paste()
    else:
        if args.input == None:
            print("You need to either pass a file to parse with -i or use the -cb argument to pull form clipboard.")
            content = "You need to either pass a file to parse with -i or use the -cb argument to pull form clipboard."
        else:
            content = open(os.path.realpath(args.input)).read()
    if args.codebox_color != None:
        default_color = "background-color: #" + args.codebox_color
    if args.background_color != None:
        body_style = 'background-color: #' + args.background_color + ''
    elif args.background_image:
        body_style = 'background-image: url(\'/getImagePath/' + args.background_image + '\'); height: 100%; background-position: center; background-repeat: no-repeat;'
    else:
        body_style = ""
    if args.syntax_style:
        if args.syntax_style in os.listdir(os.path.realpath('./styles')):
            default_css = args.syntax_style
    default_css = "a11y-dark"
    language = "plaintext"
    if args.language:
        language = args.language
    if args.style_config:
        if os.path.exists(os.path.realpath(args.style_config)):
            with open(os.path.realpath(args.style_config), 'r+') as jf:
                config = json.load(jf)
        if config.get('background-color'):
            body_style = "background-color: #" + config['background-color']
        if config.get('codebox-color'):
            default_color = "background-color: #" + config['codebox-color']
        if config.get('background-image'):
            body_style = 'background-image: url(\'/getImagePath/' + config['background-image'] + '\'); width: 100%; height: 100%'
        if config.get('syntax-style'):
            for file in os.listdir(os.path.realpath('styles/')):
                match = False
                if config.get('syntax-style') == file:
                    match = True
                if not match:
                    print("Syntax Style:" + config.get('syntax-style'), "unknown. Please check the styles/ folder or highlight.js documentation for more info.")
                else:
                    default_css = config['syntax-style']
    return render_template('test.html', style=default_css, box_color=default_color, body_style=body_style, code_here=content, language=language)

@app.route('/getImagePath/<image_path>')
def gip(image_path):
    return send_file(os.path.realpath(image_path))

@app.route('/generate')
def gen():
    browser=webdriver.Firefox()
    wheight = 1200
    wwidth = 1600
    if args.window_height:
        if not args.window_width:
            print("Please Provide A Window Width As Well!")
        else:
            wheight = args.window_height
    if args.window_width:
        if not args.window_height:
            print("Please Provide A Window Height As Well!")
        else:
            wwidth = args.window_width
    browser.set_window_size(wwidth, wheight)
    url = "http://localhost:5000"
    browser.get(url)
    if not args.output:
        print("No Output Argument Used! Using Random Name.")
        destination = "Snippet_" + str(uuid4()).split('-')[1] + '.png'
    else:
        if args.output.endswith(".png"):
            destination = args.output.replace('.png', '') + ".png"
        else:
            destination = args.output + ".png"
    if args.zoom:
        scale = float(args.zoom)
    else:
        scale = 1.0
    browser.execute_script("document.body.style.transform = 'scale({})'".format(scale))
    if browser.save_screenshot(destination):
        print("Finished Generating Snippet! You can now close out of the program with Ctrl+C.")
    browser.quit()
    return "Complete. You can now use Ctrl+C in your terminal to close the program.", 200

@app.route('/styles/<name>')
def send_style(name):
    return send_file('./styles/' + name)

print("Starting Generation...")
webbrowser.open_new_tab('http://localhost:5000/generate')
    
app.run("0.0.0.0")