# Emitter Python SDK

[![PyPI - Emitter version](https://img.shields.io/pypi/v/emitter-io.svg?style=flat-square)](https://pypi.org/project/emitter-io) [![PyPI - Python versions](https://img.shields.io/pypi/pyversions/emitter-io.svg?logo=python&style=flat-square)](https://github.com/emitter-io/python) [![GitHub - License](https://img.shields.io/github/license/emitter-io/python.svg?style=flat-square)](https://github.com/emitter-io/python/blob/master/LICENSE)

This repository contains a Python client for [Emitter](https://emitter.io) (see also [Emitter GitHub](https://github.com/emitter-io/emitter)). Emitter is an **open-source** real-time communication service for connecting online devices. At its core, emitter.io is a distributed, scalable and fault-tolerant publish-subscribe messaging platform based on MQTT protocol and featuring message storage.

This library provides a nicer high-level MQTT interface fine-tuned and extended with specific features provided by [Emitter](https://emitter.io). The code uses the [Eclipse Paho MQTT Python Client](https://github.com/eclipse/paho.mqtt.python) for handling all the network communication and MQTT protocol.


* [Installation](#install)
* [Examples](#examples)
* [API reference](#api)
* [ToDo](#todo)
* [License](#license)


<a id="install"></a>
## Installation

This SDK is available as a pip package. Install with: 
```
pip install emitter-io
```


<a id="examples"></a>
## Examples

These examples show you the whole communication process.
* Python 2: [*sample-python2.py*](emitter/sample-python2.py)
* Python 3: [*sample-python3.py*](emitter/sample-python3.py)


<a id="api"></a>
## API reference

* [`Emitter()`](#client)
  * [`.connect()`](#connect)
  * [`.publish()`](#publish)
  * [`.subscribe()`](#subscribe)
  * [`.unsubscribe()`](#unsubscribe)
  * [`.disconnect()`](#disconnect)
  * [`.on()`](#on)
  * [`.presence()`](#presence)
  * [`.keygen()`](#keygen)
* [`EmitterMessage()`](#message)
  * [`.asString()`](#asString)
  * [`.asObject()`](#asObject)
  * [`.asBinary()`](#asBinary)

-------------------------------------------------------
<a id="client"></a>
### Emitter()

The `Emitter` class represents the client connection to an Emitter server.

See [`Emitter#on()`](#on) for the possibilities of event handling.

#### Events

##### Event `'connect'`

Emitted on successful (re)connection. No arguments provided.

##### Event `'disconnect'`

Emitted after a disconnection. No arguments provided.

##### Event `'message'`

Emitted when the client receives a message packet. The message object will be of [EmitterMessage](#message) class, encapsulating the channel and the payload.

<a id="client-presence"></a>
##### Event `'presence'`

Emitted when a presence call was made using the [`Emitter#presence()`](#presence) function. Example arguments below.
```
{"time": 1577833210,
 "event": "status",
 "channel": "<channel name>",
 "who": [{"id": "ABCDE12345FGHIJ678910KLMNO", "username": "User1"},
         {"id": "PQRST12345UVWXY678910ZABCD"}]}
{"time": 1577833220,
 "event": "subscribe",
 "channel": "<channel name>",
 "who": {"id": "ABCDE12345FGHIJ678910KLMNO", "username": "User1"}}
{"time": 1577833230,
 "event": "unsubscribe",
 "channel": "<channel name>",
 "who": {"id": "ABCDE12345FGHIJ678910KLMNO"}}
````
* `time` is the time of the event as *Unix time*.
* `event` is the event type: `subscribe` when an remote instance subscribed to the channel, `unsubscribe` when an remote instance unsubscribed from the channel and `status` when [`Emitter#presence()`](#presence) is called the first time.
* `channel` is the channel name.
* `who` in case of the `event` is `(un)subscribe` one dict with the user id, when the `event` is `status`, it is a list with the users. When more than 1000 users at the moment subscribed to the channel, 1000 randomly selected are displayed.
  * `id` is an internal generated id of the remote instance.
  * `username` is a custom chosen name by the remote instance. Please note that it is **optional** and check always if this parameter exists. 

<a id="client-keygen"></a>
##### Event `'keygen'`

**ToDo: Description!**

-------------------------------------------------------
<a id="connect"></a>
### Emitter#connect(options={})

```
import emitter

instance = emitter.connect({
    "host": "api.emitter.io",
    "port": 443,
    "keepalive": 30,
    "secure": True
})
```
Connects to an Emitter server and returns an [Emitter](#client) instance.
* `host` is the address of the Emitter broker. (Optional | `Str` | Default: `"api.emitter.io"`)
* `port` is the port of the emitter broker. (Optional | `Int` | Default when secure: `443`, otherwise: `8080`)
* `keepalive` is the time the connection is keeped alive (Optional | `Int` | Default: `30`)
* `secure` is if there should be a secure connection. It's recommend to use `True`. (Optional | `Bool` | Default: `True`)

-------------------------------------------------------
<a id="publish"></a>
### Emitter#publish(key, channel, message, ttl=None)

```
instance.publish("<channel key>",
                 "<channel name>",
                 "Hello Emitter!",
                 ttl=604800) // one week
```
Publishes a message to a particual channel.
* `key` is the channel key to use for the operation. (Required | `Str`)
* `channel` is the channel name to publish to. (Required | `Str`)
* `message` is the message to publish (Required | `String` | Default: `30`)
* `ttl` is the time to live of the message in seconds. When `None` or `0` the message will only be send to all connected instances. (Optional | `Int` | Default: `None`)

-------------------------------------------------------
<a id="subscribe"></a>
### Emitter#subscribe(key, channel, last=None)

```
instance.subscribe("<channel key>",
                   "<channel name>",
                   last=5)
```
Subscribes to a particual channel.
* `key` is the channel key to use for the operation. (Required | `Str`)
* `channel` is the channel name to subscribe to. (Required | `Str`)
* `last` is the number of most recent stored messages to retrieve. (Optional | `Int` | Default: `None`)

-------------------------------------------------------
<a id="unsubscribe"></a>
### Emitter#unsubscribe(key, channel)

```
instance.unsubscribe("<channel key>",
                     "<channel name>")
```
Unsubscribes from a particual channel.
* `key` is the channel key to use for the operation. (Required | `Str`)
* `channel` is the channel name to unsubscribe from. (Required | `Str`)

-------------------------------------------------------
<a id="disconnect"></a>
### Emitter#disconnect()

```
instance.disconnect()
```
Disconnects from the connected Emitter server.

-------------------------------------------------------
<a id="on"></a>
### Emitter#on(event, callback)

Registers a callback for different events. See [`Emitter`](#client) for a description of the events. The callbacks are all overridden when calling [`connect()`](#on).

```
def connectCallback()
    print("Yeah, we connected to Emitter!")

def disconnectCallback()
    print("Oh no, we disconnected from Emitter!")

instance.on("connect", connectCallback)
instance.on("disconnect", disconnectCallback)

def messageHandler(message) # because of the f-Strings only for Python 3.6+
    print("We just recieved a message!")
    print(f"See it asString: {message.asString()}")
    print(f"See it asObject: {message.asObject()}")
    print(f"See it asBinary: {message.asBinary()}")

instance.on("message", messageHandler)

def presenceHandler(status) # because of the f-Strings only for Python 3.6+
    if status["event"] == "subscribe":
        print(f"A remote instance subscribed the channel! Details: {status}")
    elif status["event"] == "unsubscribe":
        print(f"A remote instance unsubscribed the channel! Details: {status}")
    elif status["event"] == "status":
        print(f"Presence information: {status}")

instance.on("presence", presenceHandler)
```

**ToDo: Keygen example!**

-------------------------------------------------------
<a id="presence"></a>
### Emitter#presence(key, channel)

```
instance.presence("<channel key>",
                  "<channel name>")
```
Sends a presence request to the server. See also [`Emitter`](#client-presence) for a description of the event and [`Emitter#on()`](#on) for the possibilities of event handling.
* `key` is the channel key to use for the operation. (Required | `Str`)
* `channel` is the channel name of which you want to call the presence. (Required | `Str`)

-------------------------------------------------------
<a id="keygen"></a>
### Emitter#keygen(key, channel)

```
instance.keygen("<master key>",
                "<channel name>")
```
Sends a key generation request to the server. See also [`Emitter`](#client-keygen) for a description of the event and [`Emitter#on()`](#on) for the possibilities of event handling.
* `key` is your *master key* to use for the operation. (Required | `Str`)
* `channel` is the channel name to generate a key for. (Required | `Str`)

-------------------------------------------------------
<a id="message"></a>
### EmitterMessage()

The `EmitterMessage` class represents a message received from the Emitter server. It contains two properties:
* `channel` is the channel name the message was published to. (`Str`)
* `binary` is the buffer associated with the payload. (Binary `Str`)

-------------------------------------------------------
<a id="asString"></a>
### EmitterMessage#asString()

```
message.asString()
```
Returns the payload as a utf-8 `String`.

-------------------------------------------------------
<a id="asObject"></a>
### EmitterMessage#asObject()

```
message.asObject()
```
Returns the payload as a JSON-deserialized Python `Object`.

-------------------------------------------------------
<a id="asBinary"></a>
### EmitterMessage#asBinary()

```
message.asBinary()
```
Returns the payload as a raw binary buffer.


<a id="todo"></a>
## ToDo

There are some points where the Python libary can be improved:
- Complete the [presence](#client-presence) and [keygen](#client-keygen) entries in the README (see the **ToDo** markings)
- Add more features to reach the same feature set as the JavaScript libary (`username` in presence; Emitter#me() function)


<a id="license"></a>
## License

Eclipse Public License 1.0 (EPL-1.0)

Copyright (c) 2016-2019 [Misakai Ltd.](http://misakai.com)
