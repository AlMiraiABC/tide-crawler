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

## Config

All configs set in [config.py](./config.py)

You can change this file to get variables from environment or other places.
Such as `LCSetting.APP_ID`

## Docker

## Develop
