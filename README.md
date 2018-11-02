# Emitter Python SDK

[![PyPI](https://img.shields.io/pypi/v/emitter-io.svg)](https://github.com/emitter-io/python) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/emitter-io.svg?logo=python)](https://github.com/emitter-io/python)

This repository contains a Python client for [Emitter](https://emitter.io) (see also [Emitter GitHub](https://github.com/emitter-io/emitter)). Emitter is an **open-source** real-time communication service for connecting online devices. At its core, emitter.io is a distributed, scalable and fault-tolerant publish-subscribe messaging platform based on MQTT protocol and featuring message storage.

This library provides a nicer high-level MQTT interface fine-tuned and extended with specific features provided by [Emitter](https://emitter.io). The code uses the [Eclipse Paho MQTT Python Client](https://github.com/eclipse/paho.mqtt.python) for handling all the network communication and MQTT protocol, and is released under the same license (EPL v1). 

* [Examples](#examples)
* [API](#api)

<a name="examples"></a>
## Examples

See [*sample-python2.py*](emitter/sample-python2.py) and [*sample-python3.py*](emitter/sample-python3.py).

<a name="api"></a>
## API

  * [```connect()```](#connect)
  * [```Emitter()```](#emitter)
  	* [```.publish()```](#connect)
  	* [```.subscribe()```](#subscribe)
  	* [```.unsubscribe()```](#unsubscribe)
  	* [```.disconnect()```](#disconnect)
  	* [```.on()```](#on)
  	* [```.presence()```](#presence)
    * [```.keygen()```](#keygen)
  * [```EmitterMessage()```](#message)
  	* [```.asString()```](#asString)
  	* [```.asBinary()```](#asBinary)
  	* [```.asObject()```](#asObject)

-------------------------------------------------------
<a name="connect"></a>
### connect(options={})

```
import emitter

instance = emitter.connect({
    "host": "api.emitter.io",
    "port": 443,
    "keepalive": 30,
    "secure": True
})
```
Connects to an Emitter server and returns an [Emitter](#emitter) instance.
* `host` is the address of the Emitter broker. (Optional | `Str` | Default: `"api.emitter.io"`)
* `port` is the port of the emitter broker. (Optional | `Int` | Default when secure: `443`, otherwise: `8080`)
* `keepalive` is the time the connection is keeped alive (Optional | `Int` | Default: `30`)
* `secure` is if there should be a secure connection. It's recommend to use `True`. (Optional | `Bool` | Default: `True`)

-------------------------------------------------------
<a name="emitter"></a>
### Emitter()

The `Emitter` class represents the client connection to an Emitter server.

See [`Emitter#on()`](#on) for the possibilities of event handling.

#### Event `'connect'`

Emitted on successful (re)connection. No arguments provided.

#### Event `'disconnect'`

Emitted after a disconnection. No arguments provided.

#### Event `'message'`

Emitted when the client receives a message packet. A message object ([EmitterMessage](#message) class) is provided.

<a name="emitter-presence"></a>
#### Event `'presence'`

Emitted when a presence call was made. Example arguments below.
```
{"time": 1577833210, "event": "status", "channel": "<channel name>", "who": [{"id": "ABCDE12345FGHIJ678910KLMNO", "username": "User1"}, {"id": "PQRST12345UVWXY678910ZABCD"}]}
{"time": 1577833220, "event": "subscribe", "channel": "<channel name>", "who": {"id": "ABCDE12345FGHIJ678910KLMNO", "username": "User1"}}
{"time": 1577833230, "event": "unsubscribe", "channel": "<channel name>", "who": {"id": "ABCDE12345FGHIJ678910KLMNO", "username": "User1"}}
````
* `time` is the time of the event as *Unix time*.
* `event` is the event type: `subscribe` when an remote instance subscribed to the channel, `unsubscribe` wehn an remote instance unsubscribed from the channel and `status` for the first time after the [```.presence()```](#presence) call.
* `channel` is the channel name.
* `who` in case of the `event` is `(un)subscribe` one dict with the user id, when the `event` is `status`, it is a list with the users. When more than 1000 users at the moment subscribed to the channel, 1000 randomly selected are displayed.
  * `id` is an internal generated id of the remote instance.
  * `username` is a custom chosen name by the remote instance. Please note that it is **optional** and check always if this parameter exists. 

#### Event `'keygen'`

**ToDo: Description!**

-------------------------------------------------------
<a name="publish"></a>
### Emitter#publish(key, channel, message, ttl=None)

```
instance.publish("key": "<channel key>",
                 "channel": "<channel name>",
                 "message": "Hello Emitter!",
                 "ttl": None)
```
Publishes a message to a channel.
* `key` is the security key to use for the operation. (Required | `Str`)
* `channel` is the channel string to publish to. (Required | `Str`)
* `message` is the message to publish (Required | `String` | Default: `30`)
* `ttl` is the time to live of the message in seconds. When None or 0 the message will only be send to all connected instances. (Optional | `Int` | Default: `None`)

-------------------------------------------------------
<a name="subscribe"></a>
### Emitter#subscribe(key, channel, last=None)

```
instance.subscribe("key": "<channel key>",
                   "channel": "<channel name>",
                   "last": None)
```
Subscribes to a particual channel.
* `key` is the security key to use for the operation. (Required | `Str`)
* `channel` is the channel string to subscribe to. (Required | `Str`)
* `last` is the number of most recent stored messages to retrieve. (Optional | `Int` | Default: `None`)

-------------------------------------------------------
<a name="unsubscribe"></a>
### Emitter#unsubscribe(key, channel)

```
instance.unsubscribe("key": "<channel key>",
                     "channel": "<channel name>")
```
Unsubscribes from a particual channel.
* `key` is the security key to use for the operation. (Required | `Str`)
* `channel` is the channel string to subscribe to. (Required | `Str`)

-------------------------------------------------------
<a name="disconnect"></a>
### Emitter#disconnect()

```
instance.disconnect()
```
Disconnects from the connected Emitter server.

-------------------------------------------------------
<a name="on"></a>
### Emitter#on(event, callback)

Registers a callback for different events. See [`Emitter`](#emitter) for a description of the events.

```
def connectCallback()
    print("Yeah, we connected to Emitter!")

def disconnectCallback()
    print("Oh no, we disconnected from Emitter!")

instance.on("connect", connectCallback)
instance.on("disconnect", disconnectCallback)

def messageHandler(message)
    print("We just recieved a message!")
    print("See it asString: {}".format(message.asString()))
    print("See it asBinary: {}".format(message.asBinary()))
    print("See it asObject: {}".format(message.asObject()))

instance.on("message", messageHandler)

def presenceHandler(status)
    if status["event"] == "subscribe":
        print("An remote instance subscribed the channel! Details: {}".format(status))
    elif status["event"] == "unsubscribe":
        print("An remote instance unsubscribed the channel! Details: {}".format(status))
    elif status["event"] == "status":
        print("Presence information: {}".format(status))

instance.on("presence", presenceHandler)
```

**ToDo: Keygen example!**

-------------------------------------------------------
<a name="presence"></a>
### Emitter#presence(key, channel)

```
instance.presence("key": "<channel key>",
                  "channel": "<channel name>")
```
Sends a presence request to the server. See [`Emitter`](#emitter-presence) for a description of the event and [`Emitter#on()`](#on) for the possibilities of event handling.
* `key` is the security key to use for the operation. (Required | `Str`)
* `channel` is the channel string to subscribe to. (Required | `Str`)

-------------------------------------------------------
<a name="keygen"></a>
### Emitter#keygen(key, channel)

```
instance.keygen("key": "<channel key>",
                "channel": "<channel name>")
```
Sends a key generation request to the server.
* `key` is the security key to use for the operation. (Required | `Str`)
* `channel` is the channel string to subscribe to. (Required | `Str`)

-------------------------------------------------------
<a name="message"></a>
### EmitterMessage()

The `EmitterMessage` class represents a message received from the Emitter server. It contains two properties:
* `channel` is the channel the message was published to. (`Str`)
* `binary` is the buffer associated with the payload. (Binary `Str`)

-------------------------------------------------------
<a name="asString"></a>
### EmitterMessage#asString()

```
message.asString()
```
Returns the payload as a utf-8 `String`.

-------------------------------------------------------
<a name="asBinary"></a>
### EmitterMessage#asBinary()

```
message.asBinary()
```
Returns the payload as a raw binary buffer.

-------------------------------------------------------
<a name="asObject"></a>
### EmitterMessage#asObject()

```
message.asObject()
```
Returns the payload as an JSON-deserialized Python `Object`.
