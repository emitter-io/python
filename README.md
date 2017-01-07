# Emitter Python SDK

This repository contains a Python client for [Emitter](https://emitter.io) (see also on [Emitter GitHub](https://github.com/emitter-io/emitter)). Emitter is an **open-source** real-time communication service for connecting online devices. At its core, emitter.io is a distributed, scalable and fault-tolerant publish-subscribe messaging platform based on MQTT protocol and featuring message storage.

This library provides a nicer MQTT interface fine-tuned and extended with specific features provided by [Emitter](https://emitter.io). The code uses the [Eclipse Paho MQTT Python Client](https://github.com/eclipse/paho.mqtt.python) for handling all the network communication and MQTT protocol, and is released under the same license (EPL v1). 

* [Installation](#install)
* [Example](#example)
* [API](#api)

<a name="install"></a>
## Installation

This SDK is available as a pip package :
```
pip install emitter-io
```

<a name="example"></a>
## Example

See sample-python2.py and sample-python3.py.

<a name="api"></a>
## API
  * <a href="#connect"><code><b>connect()</b></code></a>
  * <a href="#client"><code><b>Emitter()</b></code></a>
  * <a href="#publish"><code>Emitter#<b>publish()</b></code></a>
  * <a href="#subscribe"><code>Emitter#<b>subscribe()</b></code></a>
  * <a href="#unsubscribe"><code>Emitter#<b>unsubscribe()</b></code></a>
  * <a href="#disconnect"><code>Emitter#<b>disconnect()</b></code></a>
  * <a href="#on"><code>Emitter#<b>on()</b></code></a>
  * <a href="#message"><code><b>EmitterMessage()</b></code></a>
  * <a href="#asString"><code>EmitterMessage#<b>asString()</b></code></a>
  * <a href="#asBinary"><code>EmitterMessage#<b>asBinary()</b></code></a>
  * <a href="#asObject"><code>EmitterMessage#<b>asObject()</b></code></a>

-------------------------------------------------------
<a name="connect"></a>
### connect(options={})

Connects to the emitter api broker and returns an [Emitter](#emitter) instance.
options is a dictionary potentially containing any of the following keys : "host", "port", "keepalive", "secure".

-------------------------------------------------------
<a name="client"></a>
### Emitter()

The `Emitter` class wraps a client connection to an emitter.io MQTT broker.


#### Event `'connect'`

Emitted on successful (re)connection. 


#### Event `'disconnect'`


Emitted after a disconnection.


### Event `'message'`

Emitted when the client receives a message packet. The message object will be of [EmitterMessage](#message) class, encapsulating the channel and the payload.


-------------------------------------------------------
<a name="publish"></a>
### Emitter#publish(key, channel, message, ttl=None)

Publish a message to a channel
* `key` is security key to use for the operation, `String`
* `channel` is the channel string to publish to, `String`
* `message` is the message to publish
* `ttl` is the time to live of the message (optional)

-------------------------------------------------------
<a name="subscribe"></a>
### Emitter#subscribe(key, channel, last=None)

Subscribes to a channel
* `key` is security key to use for the operation, `String`
* `channel` is the channel string to subscribe to, `String`
* `last` is the number of most recent stored messages to retrieve (optional)

-------------------------------------------------------
<a name="unsubscribe"></a>
### Emitter#unsubscribe(key, channel)

Unsubscribes from a channel
* `key` is security key to use for the operation, `String`
* `channel` is the channel string to unsubscribe from, `String`

-------------------------------------------------------
<a name="disconnect"></a>
### Emitter#disconnect()

Disconnects from the remote broker

-------------------------------------------------------
<a name="on"></a>
### Emitter#on(event, handler)

Registers a handler for one of the following events : "connect", "disconnect", "message", "presence", "keygen".

-------------------------------------------------------
<a name="message"></a>
### EmitterMessage()

The `EmitterMessage` class wraps a message received from the broker. It contains several properties:
* `channel` is channel the message was published to, `String`
* `binary` is the buffer associated with the payload

-------------------------------------------------------
<a name="asString"></a>
### EmitterMessage#asString()

Returns the payload as a utf-8 `String`.

-------------------------------------------------------
<a name="asBinary"></a>
### EmitterMessage#asBinary()

Returns the payload as the `Buffer`.

-------------------------------------------------------
<a name="asObject"></a>
### EmitterMessage#asObject()

Returns the payload as JSON-deserialized `Object`.
