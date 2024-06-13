# NXO-CPE guesser

NXO-CPE guesser is a command-line and web service to guess the CPE name based on keyword(s), and asset type or version.  The result can be used against [NVD cpe-search](https://nvd.nist.gov/products/cpe/search) to retrieve vulnerabilities related to the search result.

This work is a fork of [Alexandre Dulaunoy and Esa Jokinen tool](https://github.com/cve-search/cpe-guesser).

## Requirements

- Redis 5.0.4
- Redis-cli 7.0.15
- Python 3.12.3
- Dynaconf 3.2.5
- Falcon==3.1.3
- [CPE 2.3 Dictionary XML] (https://nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.3.xml.gz)
- crontab

## Installation

First if it's not already done, you need to install python 3.12.3:  

```bash
    $ sudo apt-get update  
    $ sudo apt-get install python3.12.3
```

Make sure you have the right version of python and pip

```bash
    $ python --version  
    $ pip --version
```

Install [**virtualenv**](https://pypi.org/project/virtualenv/)


```bash
    $ pip install virtualenv  
    $ virtualenv --version
```

Create an isolated python environments and activate it

```bash
    $ virtualenv venv  
    $ source venv/bin/activate
```

Install the project dependency with the following command

```bash
    $ pip install -r requirements.txt  
```

Initialise the Redis database with the following command

```bash
    python ./bin/import.py -d
```

You can now launch the search directly in the command line interface or through a web server. For the CLI, you can search the matching entry for **microsoft sql server** with the following command:  

```bash
    python3 ./bin/lookup.py microsoft server | jq . 
```

To launch the webserver, execute the following command:  

```bash
    python3 ./bin/server.py
```

You can then try the same request with throught a CLI or Postman with the following curl query:  

```curl
    curl -s -X POST http://localhost:8000/search -d "{\"query\": [\"microsoft\",\"server\"]}" | jq .
```

## Configuration

All the configuration can be found in `config -> settings.yaml`.  

```python
    server:
        port: 8080 # The port on which the server will listen for incomming request 
    redis:
        host: 127.0.0.1 # Host of your redis service 
        port: 6379 # Port of your redis service 
    cpe:
        path: '/absolute_path_to_the_dictionnary/official-cpe-dictionary_v2.3.xml' # Absolute path to access a local copy of the CPE dictionnary
        source: 'https://nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.3.xml.gz' # Online adress of the CPE dictionnary. You must frequently check on the NVD website to be sure that the ressource stays available
```

### Docker

#### Single image with existing Redis

```bash
docker build . -t cpe-guesser:l.0
# Edit settings.yaml content and/or path
docker run cpe-guesser:l.0 -v $(pwd)/config/settings.yaml:/app/config/settings.yaml
# Please wait for full import
```

#### Docker-compose

```bash
cd docker
# Edit docker/settings.yaml as you want
docker-compose up --build -d
# Please wait for full import
```

#### Specific usage

If you do not want to use the Web server, `lookup.py` can still be used. Example: `docker exec -it cpe-guesser python3 /app/bin/lookup.py tomcat`

## Public online version

[cpe-guesser.cve-search.org](https://cpe-guesser.cve-search.org) is public online version of CPE guesser which can be used via
a simple API. The endpoint is `/search` and the JSON is composed of a query list with the list of keyword(s) to search for.

```bash
curl --location 'http://localhost:8080/search' --header 'Content-Type: application/json' --data '{"query": ["microsoft","sql", "server"], "version":"(10)","type":"a","limit":10}'
```

```json
[
    "cpe:2.3:a:microsoft:sql_server:6.0", 
    "cpe:2.3:a:microsoft:sql_server:7.0", 
    "cpe:2.3:a:microsoft:sql_server:-", 
    "cpe:2.3:a:microsoft:sql_server:2000", 
    "cpe:2.3:a:microsoft:sql_server:2005", 
    "cpe:2.3:a:microsoft:sql_server:2008", 
    "cpe:2.3:a:microsoft:sql_server:2012", 
    "cpe:2.3:a:microsoft:sql_server:2014", 
    "cpe:2.3:a:microsoft:sql_server:2016", 
    "cpe:2.3:a:microsoft:sql_server:2017"
]
```

### Command line - `lookup.py`

```text
usage: lookup.py [-h] [--type TYPE] [--limit LIMIT]
                 [--version VERSION]
                 WORD [WORD ...]

Find potential CPE names from a list of keyword(s) and return a
JSON of the results

positional arguments:
  WORD                  One or more keyword(s) to lookup

options:
  -h, --help            show this help message and exit
  --type TYPE, -t TYPE  Specify the type of assets(o for
                        Operating system, a for application, h
                        for hardware).
  --limit LIMIT, -l LIMIT
                        Specify the number of result to return.
  --version VERSION, -v VERSION
                        Give a string to match with
                        corresponding asset version.
```

```bash
python3 ./bin/lookup.py cisco ios -v "15.2(2)" -t "a" -l 10 | jq .
```

```json
[
  "cpe:2.3:a:cisco:ios:15.2\\(2\\)ea",
  "cpe:2.3:a:cisco:ios:15.2\\(2\\)eb",
  "cpe:2.3:a:cisco:ios:15.2\\(2\\)ea1",
  "cpe:2.3:a:cisco:ios:15.2\\(2\\)eb1",
  "cpe:2.3:a:cisco:ios:15.8\\(3\\)m3",
  "cpe:2.3:a:cisco:ios:16.11.2",
  "cpe:2.3:a:cisco:ios_xe:15.2\\(07\\)e02",
  "cpe:2.3:a:cisco:ios_xe:15.2\\(07\\)e03",
  "cpe:2.3:a:cisco:ios:17.3.1",
  "cpe:2.3:a:cisco:ios_xe:15.8\\(3\\)m3"
]
```

## How does this work?

A CPE entry is composed of a human readable name with some references and the structured CPE name.

```xml
  <cpe-item name="cpe:/a:10web:form_maker:1.7.17::~~~wordpress~~">
    <title xml:lang="en-US">10web Form Maker 1.7.17 for WordPress</title>
    <references>
      <reference href="https://wordpress.org/plugins/form-maker/#developers">Change Log</reference>
    </references>
    <cpe-23:cpe23-item name="cpe:2.3:a:10web:form_maker:1.7.17:*:*:*:*:wordpress:*:*"/>
  </cpe-item>
```

The CPE name is structured with a vendor name, a product name and some additional information.
CPE name can be easily changed due to vendor name or product name changes, some vendor/product are sharing common names or name is composed of multiple words.

### Data

Split vendor name and product name (such as `_`) into single word(s) and then canonize the word. Building an inverse index using the cpe vendor:product format as value and the canonized word as key.  Then cpe guesser creates a ranked set with the most common cpe (vendor:product)  per version to give a probability of the CPE appearance.

### Redis structure

- `w:<word>` set
- `s:<word>` sorted set with a score depending of the number of appearance
- `w_{type}_v:{word}` set of entry with CPE type
- `s_{type}_v:{word}` sorted set with a score depending of the number of appearance

## License

Software is open source and released under a 2-Clause BSD License

Copyright (C) 2021-2024 Alexandre Dulaunoy  
Copyright (C) 2021-2024 Esa Jokinen  
