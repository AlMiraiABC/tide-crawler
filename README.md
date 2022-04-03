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

## Docker

## Develop
