# snipit
Generate code snippets from files and clipboard.
*This is still in very early development and simply in an Alpha stage.*

### Requirements:

- Python 3.6
- Firefox (Get a newer version for best results, need geckodriver for Selenium)
- Selenium

### Installation:

Grab dependencies:

```
pip install -r requirements.txt
```

Make sure you have Geckodriver installed and available in your path! If you installed the Firefox browser you should be all set.

### Usage:

```
python snipit.py [-h] [-i INPUT] [-o OUTPUT] [-l LANGUAGE] [-wh WINDOW_HEIGHT]
                 [-ww WINDOW_WIDTH] [-cb] [-bc BACKGROUND_COLOR]
                 [-bi BACKGROUND_IMAGE] [-cc CODEBOX_COLOR] [-ss SYNTAX_STYLE]
                 [-sc STYLE_CONFIG] [-z ZOOM]
```

To input a file use:

```
python snipit.py -i /path/to/file -l language
```

To input from clipboard use:

```
python snipit.py -cb -l language
```

To pull from a config use:
```
python snipit.py -sc config.json -cb -l python
```

**Syntax Styles == Highlight.JS CSS Colors. You can find a list of them here: https://github.com/highlightjs/highlight.js/tree/master/src/styles**

### Style Configs:

You can use a JSON file to share style configs for others or to use for yourself to keep track of easy configurations. Any values in these configs will override values you pass as an argument!

Example Style:
```json
{
    "background-color": "292929",
    "codebox-color": "707070",
    "zoom": 1.5,
    "syntax-style": "a11y-light"
}
```

### Options as of now:

```
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Generate Snippet From Input File
  -o OUTPUT, --output OUTPUT
                        Output File To Store Image. No need for file ext.
  -l LANGUAGE, --language LANGUAGE
                        Language for Syntax Highlighting. Supports
                        highlight.js
  -wh WINDOW_HEIGHT, --window-height WINDOW_HEIGHT
                        Browser Height. Default: 1200
  -ww WINDOW_WIDTH, --window-width WINDOW_WIDTH
                        Browser Width. Default: 1600
  -cb, --clip-board     Generate Snippet From Clibboard
  -bc BACKGROUND_COLOR, --background-color BACKGROUND_COLOR
                        Background Color For HTML. Uses Hex Codes.
  -bi BACKGROUND_IMAGE, --background-image BACKGROUND_IMAGE
                        Path to background image for snippet.
  -cc CODEBOX_COLOR, --codebox-color CODEBOX_COLOR
                        Background Color for Codebox. Uses Hex Codes.
  -ss SYNTAX_STYLE, --syntax-style SYNTAX_STYLE
                        Syntax Color Style for Code. Supports highlight.js
                        styles
  -sc STYLE_CONFIG, --style-config STYLE_CONFIG
                        Pass StyleConfig.json File As Snippet Style.
  -z ZOOM, --zoom ZOOM  Amount to Use for Zoom
  ```
  
  
  ## Credits:
  
  [highlight.js](https://highlightjs.org) - Syntax highlighting and CSS
  
  [bulma.io](https://bulma.io) - CSS Components
  
