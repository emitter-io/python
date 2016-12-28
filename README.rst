Emitter Python SDK
==================

This repository contains a Python client for
`Emitter <https://emitter.io>`__ (see also on `Emitter
GitHub <https://github.com/emitter-io/emitter>`__). Emitter is an
**open-source** real-time communication service for connecting online
devices. At its core, emitter.io is a distributed, scalable and
fault-tolerant publish-subscribe messaging platform based on MQTT
protocol and featuring message storage.

This library provides a nicer MQTT interface fine-tuned and extended
with specific features provided by `Emitter <https://emitter.io>`__. The
code uses the `Eclipse Paho MQTT Python
Client <https://github.com/eclipse/paho.mqtt.python>`__ for handling all
the network communication and MQTT protocol, and is released under the
same license (EPL v1).

 ## Example

See test.py.

 ## API \* connect() \* Emitter() \* Emitter#publish() \*
Emitter#subscribe() \* Emitter#unsubscribe() \* Emitter#disconnect() \*
Emitter#on() \* EmitterMessage() \* EmitterMessage#asString() \*
EmitterMessage#asBinary() \* EmitterMessage#asObject()

+--------------------------------------------------------+
|  ### connect(options={})                               |
+--------------------------------------------------------+
| Connects to the emitter api broker and returns an      |
| `Emitter <#emitter>`__ instance. options is a          |
| dictionary potentially containing any of the following |
| keys : "host", "port", "keepalive", "secure".          |
+--------------------------------------------------------+

 ### Emitter()

The ``Emitter`` class wraps a client connection to an emitter.io MQTT
broker.

Event ``'connect'``
^^^^^^^^^^^^^^^^^^^

Emitted on successful (re)connection.

Event ``'disconnect'``
^^^^^^^^^^^^^^^^^^^^^^

Emitted after a disconnection.

Event ``'message'``
~~~~~~~~~~~~~~~~~~~

Emitted when the client receives a message packet. The message object
will be of `EmitterMessage <#message>`__ class, encapsulating the
channel and the payload.

+--------------------------------------------------------+
|  ### Emitter#publish(key, channel, message, ttl=None)  |
+--------------------------------------------------------+
| Publish a message to a channel \* ``key`` is security  |
| key to use for the operation, ``String`` \*            |
| ``channel`` is the channel string to publish to,       |
| ``String`` \* ``message`` is the message to publish \* |
| ``ttl`` is the time to live of the message (optional)  |
+--------------------------------------------------------+

 ### Emitter#subscribe(key, channel, last=None)

Subscribes to a channel \* ``key`` is security key to use for the
operation, ``String`` \* ``channel`` is the channel string to subscribe
to, ``String`` \* ``last`` is the number of most recent stored messages
to retrieve (optional)

+--------------------------------------------------------+
|  ### Emitter#unsubscribe(key, channel)                 |
+--------------------------------------------------------+
| Unsubscribes from a channel \* ``key`` is security key |
| to use for the operation, ``String`` \* ``channel`` is |
| the channel string to unsubscribe from, ``String``     |
+--------------------------------------------------------+

 ### Emitter#disconnect()

Disconnects from the remote broker

+--------------------------------------------------------+
|  ### Emitter#on(event, handler)                        |
+--------------------------------------------------------+
| Registers a handler for one of the following events :  |
| "connect", "disconnect", "message", "presence",        |
| "keygen".                                              |
+--------------------------------------------------------+

 ### EmitterMessage()

The ``EmitterMessage`` class wraps a message received from the broker.
It contains several properties: \* ``channel`` is channel the message
was published to, ``String`` \* ``binary`` is the buffer associated with
the payload

+--------------------------------------------------------+
|  ### EmitterMessage#asString()                         |
+--------------------------------------------------------+
| Returns the payload as a utf-8 ``String``.             |
+--------------------------------------------------------+

 ### EmitterMessage#asBinary()

Returns the payload as the ``Buffer``.

--------------

 ### EmitterMessage#asObject()

Returns the payload as JSON-deserialized ``Object``.
