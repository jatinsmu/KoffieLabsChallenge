# KOFFIE LABS CHALLENGE

## Objective

Objective
This is a simple implementation of [FastAPI](https://fastapi.tiangolo.com/) backend in Python to decode VINs, powered by the [vPIC API](https://vpic.nhtsa.dot.gov/api/) and backed by a [SQLite](https://www.sqlite.org/index.html) cache.


## Installation
1. Clone this repository
2. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.txt file.

```bash
pip install requirements.txt
```

## Usage

Run the main.py file to create a server using your python environment
```bash
python main.py
```

The server will start running at your local server address http://0.0.0.0:8000 .

There are 3 endpoints to interact with namely "lookup", "remove", "export".

Example request - http://0.0.0.0:8000/lookup?vin=1XPWD40X1ED21530

If you want to change the IP Address, change it in the "main.py" file.
```python
uvicorn.run(app, host="0.0.0.0", port=8000) # Your host address, Port number
```

To see the api docs, go to http://0.0.0.0:8000/docs
