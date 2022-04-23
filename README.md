# Tide Crawler

Tide crawler is used to get tide data.

## Prerequisites

### LeanCloud

Please create classes and a User. The user must have read, write, update, delete privileges.

Create classes with columns as blow or import from [./storages/leancloud/schemas](./storages/leancloud/schemas/).

**NOTE**
Please set all permissions and default ALC to all users. We'll fix this in next version.

* Area

    name|type|required|associated
    -|-|-|-
    raw|any
    name|String|√
    rid|String|√

* Province

    name|type|required|associated
    -|-|-|-
    raw|any
    name|String|√
    rid|String|√
    area|Pointer|√|Area

* Port

    name|type|required|associated
    -|-|-|-
    raw|any
    name|String|√
    rid|String|√
    province|Pointer|√|Province
    zone|String|√
    geopoint|GeoPoint|√

* Tide
    name|type|required|associated
    -|-|-|-
    raw|any
    port|Pointer|√|Port
    limit|Array|√
    day|Array|√
    date|Date|√
    datum|Number|√

## Config

All configs set in [config.py](./config.py)

You can change this file to get variables from environment or other places.
Such as `LCSetting.APP_ID`

## Install dependencies

```sh
pip install -r requirements.txt
```

Or set pip mirror to improve download speed with parameter `-i`.

```sh
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

## Docker

```bash
docker build .
```
