<h1 align="center">Feather Lamp</h1>

## About This Project

<p align="center">
  <img src="lamp-demo.gif" width="200" height="200">
</p>
The intent of this project is to control a custom lamp I made. The lamp contains a 'bulb' with 34 rgb leds that are controlled by an esp8266. In addition to controlling the leds the esp8266 runs a web server that, when accessed, can be used to change the light's settings.

For the time being the web server only allows for changing between a few preset colors and hopefully eventually have time to add some other cool options.

## File Hierarchy
* `boot.py`
* `main.py`
  * `try_connect.py`
  * `light_effects.py`
  * `web_server.py`
    * `index.html`
    * `app.js`
    * `style.css`
    
## Module Breakdown
With micropython `boot.py` and `main.py` will both be run on boot.

* `boot.py` is pretty much the default micropython boot file. It's necessary, but not doing much for this project.

* `try_connect.py` when run, looks for and attempts to connect to a predefined wifi network. This might usually be done in `boot.py` but I wanted to call it repeadtedly in case it couldn't initially connect without affecting other code execution and putting it in it's own module seemed like a good way to do that.

* `main.py` is actually the main file housing the `Main` class and the `main` method which use the other modules in conjunction to make all this lampy goodness happen.

* `light_effects.py` holds all the code responsible for setting led colors and maintaining the strip's state when doing interesting transition effects.

* `web_server.py` runs the web server and uses `index.html`, `app.js`, and `style.css` to display the web page and send appropriate http requests to change light settings.


