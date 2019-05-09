# Freenet FUNK API

## Introduction

Freenet FUNK is cellphone tariff that offers **unlimited** (or 1 GB of) 4G data. The tariff is can be started, stopped and paused **daily**.

To make the most out of this flexibility, I reverse engineered the **API**   to give anyone the ability to develop amazing apps on their own!

## Prerequisites

- Python >=3.2
- pip

## Installation

```sh
git clone https://github.com/lagmoellertim/freenet-funk-api.git

cd freenet-funk-api

python3 setup.py install
```

## Build

```sh
git clone https://github.com/lagmoellertim/freenet-funk-api.git

cd freenet-funk-api

python3 setup.py sdist bdist_wheel
```

## Usage

### Initialize the API

```python3
from funkapi import FunkAPI
api = FunkAPI("*username*", "*password*")
```

### Get a Token (not really necessary to do that manually but I left the option)

```python3
token = api.getToken()
```

### Initialize the API with a predefined Token

```python3
from funkapi import FunkAPI
api = FunkAPI("", "", token="*token*")
```

### Check the validity of a Token (also not really necessary to do manually)

```python3
isValid = api.testToken("*token*")
```

### Get Dashboard Data (includes every piece of data FUNK stores of you)

```python3
data = api.getData()
```

### Get Personal Information (email, name, birthday, …)

```python3
personalInfo = api.getPersonalInfo()
```

### Get a List of your ordered Products

```python3
products = api.getOrderedProducts()
```

### Get the currently active Tariff

```python3
currentTariff = api.getCurrentTariff()
```

### Order the 1GB Tariff

```python3
status = api.order1GBTariff()
```

### Order the unlimited Tariff

```python3
status = api.orderUnlimitedTariff()
```

### Start a Break

```python3
status = api.startPause()
```

### Stop the latest Product (includes stopping a break)

```python3
status = api.stopLatestTariff()
```

## Contributing

If you are missing a feature or have new idea, go for it! That is what open-source is for!

## Author

**Tim-Luca Lagmöller** ([@lagmoellertim](https://github.com/lagmoellertim))

## Donate

You can also contribute by [buying me a coffee](http://donate.lagmoellertim.de).

## License

[MIT License](https://github.com/lagmoellertim/cryption/blob/master/LICENSE)

Copyright © 2019-present, [Tim-Luca Lagmöller](https://en.lagmoellertim.de)

## Have fun :tada:
