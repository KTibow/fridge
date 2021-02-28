![Leftunder logo](/leftunder-color.svg)
# The Leftunder Project
Hosting, docs, and more for the Leftunder Project.
## Set it up
### Addons
Install Grocy. It's how you manage the food.
If you use Home Assistant, it's easily installable as an addon.  
Next, install the combined server. You can find it in the `leftunder_addon` folder of this repo.
Give it your Grocy endpoint, and a Grocy API key.
Copy it over to the `/addons` folder in Home Assistant, in its own directory.  
### MagTag
First, you'll need a physical item: the [Adafruit MagTag](https://www.adafruit.com/product/4819).
Make sure it's up to date. Install the latest beta of CircuitPython.  
Now, copy over the code. Copy over to the CIRCUITPY drive from this repo:
  - the whole `lib` folder
  - all `.pcf` and `.bmp` files
  - `code.py` and `boot.py`

Also add a `secrets.py` file with this structure.
```python
secrets = {
    "ssid": "MyNet",
    "password": "WiFiPassword",
    "endpoint": "http://combinedServerDomain:port"
}
```
Personally, I have an LED strip connected to A1.
## The cool bits
### OTA
OTA is implemented in `boot.py`.
Long-press any button while pressing reset. Release it once it beeps.
Feel free to look in the source. This is what it looks like:
### Web serial console
You can use serial without downloading anything [here](https://ktibow.github.io/fridge/serial).
### Logo + deep sleep
I made a SVG logo. View it in the repo.  
It also deep sleeps for an hour on success, and for a minute when it can't connect to WiFi.
### Photos
OTA (sorry for low quality): ![20210227_182526](https://user-images.githubusercontent.com/10727862/109405885-7f391700-7929-11eb-8fe9-d216ec0f4845.jpg)
Booting up: ![20210227_183122](https://user-images.githubusercontent.com/10727862/109405971-33d33880-792a-11eb-89e3-1741bafd81ec.jpg)
Once it's on: ![20210227_182959](https://user-images.githubusercontent.com/10727862/109405959-18682d80-792a-11eb-915e-a162c7ceb4fe.jpg)


## Attributions
Every icon in the `.bmp` files comes from icons8.
