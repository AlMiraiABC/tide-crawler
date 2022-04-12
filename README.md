# Tide Crawler

Tide crawler is used to get tide data.

## Data source

It is designed to support multiple data source: [nmdis](http://mds.nmdis.org.cn/pages/tidalCurrent.html), [cxb](https://www.chaoxibiao.net/), [cnss](https://www.cnss.com.cn/tide/), ...

Set `CRAWLER` to determine which data source should be in use.

## Data storage

It is designed to support multiple data storage: mysql, [leancloud](https://www.leancloud.cn/), redis, ...

Set `STORAGE` to determine which data storage should be in use.

## Prerequisites

### Storage in RDB

Create database and tables. The user must have read, write, update, delete privileges.

### Storage in LeanCloud

Please create classes and a User. The user must have read, write, update, delete privileges.

Create classes with columns as blow.

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

Commingle soon.

## Develop

### Project structure

```sh
|- `.devcontainer`  # configurations to develop in docker container used for vscode.
|- `crawler` # crawlers to get data from third-part
|- `db` # databases management(DAO)
|- `log` # default logs save directory.
|- `service` # unified `crawler` and `db` to provide services for `app`.
|- `utils`
|- `app.py` # start up application
|- `config.py` # configuration
|- `logging.yaml` # logger configuration
```

### Terminology

name|alias|description
-|-|-
id|objectId|Object's id for users stored in project database.
rid||Origin id for crawlers stored in third-part.

### Storage

All storage management(util) should implements `BaseDbUtil`

Using `DbUtil` to provide a unified operations.

### Crawler

### Service

All services should implements `BaseCrawlerService`
