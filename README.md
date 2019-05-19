# Emitter Python SDK

[![PyPI - Emitter version](https://img.shields.io/pypi/v/emitter-io.svg)](https://pypi.org/project/emitter-io) [![PyPI - Python versions](https://img.shields.io/pypi/pyversions/emitter-io.svg?logo=python)](https://github.com/emitter-io/python) [![GitHub - License](https://img.shields.io/github/license/emitter-io/python.svg)](https://github.com/emitter-io/python/blob/master/LICENSE)

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

* [`Client()`](#client)
  * [`.connect()`](#connect)
  * [`.disconnect()`](#disconnect)
  * [`.keygen()`](#keygen)
  * [`.link()`](#link)
  * [`.me()`](#me)
  * [`.on_connect`](#on_connect)
  * [`.on_disconnect`](#on_disconnect)
  * [`.on_error`](#on_error)
  * [`.on_keygen`](#on_keygen)
  * [`.on_me`](#on_me)
  * [`.on_message`](#on_message)
  * [`.on_presence`](#on_presence)
  * [`.presence()`](#presence)
  * [`.publish()`](#publish)
  * [`.publish_with_link()`](#publish_with_link)
  * [`.subscribe()`](#subscribe)
  * [`.subscribe_with_group()`](#subscribe_with_group)
  * [`.unsubscribe()`](#unsubscribe)
* [`EmitterMessage()`](#message)
  * [`.as_string()`](#as_string)
  * [`.as_object()`](#as_object)
  * [`.as_binary()`](#as_binary)

-------------------------------------------------------
<a id="client"></a>
### Client()

The `Client` class represents the client connection to an Emitter server.

-------------------------------------------------------
<a id="connect"></a>
### Emitter#connect(host="api.emitter.io", port=443, secure=True, keepalive=30)

```
emitter = Client()

emitter.connect()
```
Connects to an Emitter server.
* `host` is the address of the Emitter broker. (Optional | `Str` | Default: `"api.emitter.io"`)
* `port` is the port of the emitter broker. (Optional | `Int` | Default: `443`)
* `secure` whether the connection should be secure. (Optional | `Bool` | Default: `True`)
* `keepalive` is the time the connection is kept alive (Optional | `Int` | Default: `30`)

If you don't want a secure connection, set the port to 8080, unless your broker is configured differently.

To handle connection events, see the [`.on_connect`](#on_connect) property.

-------------------------------------------------------
<a id="disconnect"></a>
### Emitter#disconnect()

```
emitter.disconnect()
```
Disconnects from the connected Emitter server.

To handle disconnection events, see the [`.on_disconnect`](#on_disconnect) property.

-------------------------------------------------------
<a id="keygen"></a>
### Emitter#keygen(key, channel, permissions, ttl=0)

```
instance.keygen("Z5auMQhNr0eVnGBAgWThXus1dgtSsvuQ", "channel/", "rwslpex")
```
Sends a key generation request to the server. See also [`Emitter`](#client-keygen) for a description of the event and [`Emitter#on()`](#on) for the possibilities of event handling.
* `key` is your *master key* to use for the operation. (Required | `Str`)
* `channel` is the channel name to generate a key for. (Required | `Str`)
* `permissions` are the permissions associated to the key. (Required | `Str`)
  - `r` for read
  - `w` for write
  - `s` for store
  - `l` for load
  - `p` for presence
  - `e` for extend
  - `x` for execute
* `ttl` is the time to live of the key. `0` means it never expires (Optional | `Int` | Default: `0`)

To handle keygen responses, see the [`.on_keygen`](#on_keygen) property.

-------------------------------------------------------
<a id="link"></a>
### Emitter#link(key, channel, name, private, subscribe, options={})

```
instance.link("5xZjIQp6GA9fpxso1Kslqnv8d4XVWChb",
              "channel",
              "a0",
              False,
              True,
              {Client.with_ttl(604800), Client.without_echo()}) // one week
```
Sends a link creation request to the server. This allows for the creation of a link between a short 2-character name and an actual channel. This function also allows the creation of a private channel. For more information, see 
[Emitter: Simplify Client/Server and IoT Apps with Links and Private Links (on YouTube)](https://youtu.be/_FgKiUlEb_s) and the [Emitter Pull Request (on GitHub)](https://github.com/emitter-io/emitter/pull/183).
* `key` is the key to the channel. (Required | `Str`)
* `channel` is the channel name. (Required | `Str`)
* `name` is the short name for the channel. (Required | `Str`)
* `private` whether the request is for a private channel. (Required | `Bool`)
* `subscribe` whether or not to subscribe to the channel. (Required | `Bool`)
* `options` a set of options. Currently available options are:
  - `with_at_most_once()` to send with QoS0.
  - `with_at_least_once()` to send with QoS1.
  - `with_retain()` to retain this message.
  - `with_ttl(ttl)` to set a time to live for the message.
  - `without_echo()` to tell the broker not to send the message back to this client.

-------------------------------------------------------
<a id="me"></a>
### Emitter#me()

```
instance.me()
```
Requests information about the connection. Information provided in the response contains the id of the connection, as well as the links that were established with [`.link()`](#link) requests.

To handle the responses, see the [`.on_me`](#on_me) property.

-------------------------------------------------------
<a id="on_connect"></a>
### Emitter#on_connect

Property used to get or set the connection handler, that handle events emitted upon successful (re)connection. No arguments provided.

-------------------------------------------------------
<a id="on_disconnect"></a>
### Emitter#on_disconnect

Property used to get or set the disconnection handler, that handle events emitted after a disconnection. No arguments provided.

-------------------------------------------------------
<a id="on_error"></a>
### Emitter#on_error

Property used to get or set the error handler, that handle events emitted when an error occurs following any request. The event comes with a status code and a text message describing the error.

```
{"status": 400,
 "message": "the request was invalid or cannot be otherwise served"}
```

-------------------------------------------------------
<a id="on_keygen"></a>
### Emitter#on_keygen

**ToDo: Description!**
-------------------------------------------------------
<a id="on_me"></a>
### Emitter#on_me

Property used to get or set the handler that handle responses to [`.me()`](#me) requests. Information provided in the response contains the id of the connection, as well as the links that were established with [`.link()`](#link) requests.

```
{"id": "74W77OC5OXDBQRUUMSHROHRQPE",
 "links": {"a0": "test/",
           "a1": "test/"}}
```

-------------------------------------------------------
<a id="on_message"></a>
### Emitter#on_message

Emitted when the client receives a message packet. The message object will be of [EmitterMessage](#message) class, encapsulating the channel and the payload.

-------------------------------------------------------
<a id="on_presence"></a>
### Emitter#on_presence

Emitted either when a presence call was made requesting a status, using the [`Emitter#presence()`](#presence) function, or when a user subscribed/unsubscribed to the channel and updates were previously requested using again a call to the [`Emitter#presence()`](#presence) function. Example arguments below.

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

-------------------------------------------------------
<a id="presence"></a>
### Emitter#presence(key, channel, status=False, changes=False, optional_handler=None)

```
instance.presence(""5xZjIQp6GA9fpxso1Kslqnv8d4XVWChb"",
                  "channel",
                  True,
                  True)
```
Sends a presence request to the server.
* `key` is the channel key to use for the operation. (Required | `Str`)
* `channel` is the channel name of which you want to call the presence. (Required | `Str`)
* `status` is whether the broker should send a full status of the channel. (Optional | `Bool` | Default: `False`)
* `changes` is whether to subscribe to presence changes on the channel.  (Optional | `Bool` | Default: `False`)
* `optional_handler` is the handler to insert in the handler trie.  (Optional | `callable` | Default: `None`)

Note: if you do not provide a handler here, make sure you did set the default handler for all presence messages using the [`.on_presence`](#on_presence) property.

-------------------------------------------------------
<a id="publish"></a>
### Emitter#publish(key, channel, message, options={})

```
emitter.publish("5xZjIQp6GA9fpxso1Kslqnv8d4XVWChb",
                 "channel",
                 "Hello Emitter!",
                 {Client.with_ttl(604800), Client.without_echo()}) // one week
```
Publishes a message to a particual channel.
* `key` is the channel key to use for the operation. (Required | `Str`)
* `channel` is the channel name to publish to. (Required | `Str`)
* `message` is the message to publish (Required | `String`)
* `options` a set of options. Currently available options are:
  - `with_at_most_once()` to send with QoS0.
  - `with_at_least_once()` to send with QoS1.
  - `with_retain()` to retain this message.
  - `with_ttl(ttl)` to set a time to live for the message.
  - `without_echo()` to tell the broker not to send the message back to this client.

-------------------------------------------------------
<a id="publish_with_link"></a>
### Emitter#publish_with_link(link, message)

```
instance.publishWithLink("a0",
                         "Hello Emitter!")
```
Sends a message through the link.
* `link` is the 2-character name of the link. (Required | `Str`)
* `message` is the message to send through the link. (Required | `Str`)

-------------------------------------------------------

<a id="subscribe"></a>
### Emitter#subscribe(key, channel, optional_handler=None, options={})

```
instance.subscribe("5xZjIQp6GA9fpxso1Kslqnv8d4XVWChb",
                   "channel",
                   options={Client.with_last(5)})
```
Subscribes to a particular channel.
* `key` is the channel key to use for the operation. (Required | `Str`)
* `channel` is the channel name to subscribe to. (Required | `Str`)
* `optional_handler` is the handler to insert in the handler trie.  (Optional | `callable` | Default: `None`)
* `options` a set of options. Currently available options are:
  - `with_last(x)` to receive the last `x` messages stored on the channel.

TODO
  - `with_from`
  - `with_until`

Note: if you do not provide a handler here, make sure you did set the default handler for all messages using the [`.on_message`](#on_message) property.

-------------------------------------------------------

<a id="subscribe_with_group"></a>
### Emitter#subscribe_with_group(key, channel, share_group, optional_handler=None, options={})

```
instance.subscribe("5xZjIQp6GA9fpxso1Kslqnv8d4XVWChb",
                   "channel",
                   "sg")
```
Subscribes to a particular share group for a channel. A message sent to that channel will be forwarded to only one member of the share group, chosen randomly. For more information about share groups, see 
[Emitter: Load-balance Messages using Subscriber Groups (on YouTube)](https://youtu.be/Vl7iGKEQrTg).

* `key` is the channel key to use for the operation. (Required | `Str`)
* `channel` is the channel name to subscribe to. (Required | `Str`)
* `share_group` is the name of the group to join. (Required | `Str`)
* `optional_handler` is the handler to insert in the handler trie.  (Optional | `callable` | Default: `None`)
* `options` a set of options.


Note: if you do not provide a handler here, make sure you did set the default handler for all messages using the [`.on_message`](#on_message) property.

-------------------------------------------------------
<a id="unsubscribe"></a>
### Emitter#unsubscribe(key, channel)

```
instance.unsubscribe("5xZjIQp6GA9fpxso1Kslqnv8d4XVWChb",
                     "channel")
```
Unsubscribes from a particual channel.
* `key` is the channel key to use for the operation. (Required | `Str`)
* `channel` is the channel name to unsubscribe from. (Required | `Str`)

This deletes handlers for that channel from the trie.

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
- Complete the [keygen](#client-keygen) entry in the README (see the **ToDo** markings)
- Describe how to use the trie of handlers for regular messages and presence.
- Add `with_from` and `with_until`.

<a id="license"></a>
## License

Eclipse Public License 1.0 (EPL-1.0)

Copyright (c) 2016-2019 [Misakai Ltd.](http://misakai.com)
