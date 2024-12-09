# Web Console

<img src="https://shields.io/badge/version-0.1.0-blue">

<img src="https://raw.githubusercontent.com/SuperZombi/Web-Console/main/github/images/console.jpg" width="600px">

### Example usage
```python
from web_console import WebConsole

console = WebConsole()
console.log("Hello world")
console.loop()
```

### Constructor
```python
WebConsole(host="127.0.0.1", port=8080, show_url=True, debug=False)
```

### Methods
```python
console.log(msg)
console.warn(msg)
console.error(msg)
```
```python
console.url
```
```python
console.open() # open console_url in browser
```
```python
console.sleep(sec) # use this instead of time.sleep()
```
```python
console.loop() # use this if you dont have your code mainloop
```
