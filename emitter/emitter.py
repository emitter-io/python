import paho.mqtt.client as mqtt
import ssl
import json
import logging
import re

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


"""
 * Represents the client connection to an Emitter server.
"""
class Emitter(object):

    def __init__(self):
        pass

    """
     * Call regularly to process network events. This call waits in select()
     * until the network socket is available for reading or writing, if
     * appropriate, then handles the incoming/outgoing data. This function
     * blocks for up to timeout seconds.
     * timeout must not exceed the keepalive value for the client or your
     * client will be regularly disconnected by the broker.
    """
    def loop(self, timeout):
        self._mqtt.loop(timeout=timeout)

    """
     * This is a blocking form of the network loop and will not return until the
     * client calls disconnect(). It automatically handles reconnecting.
    """
    def loopForever(self):
        self._mqtt.loop_forever()

    """
     * These functions implement a threaded interface to the network loop.
     * Calling loop_start() once, before or after connect*(), runs a thread in
     * the background to call loop() automatically. This frees up the main
     * thread for other work that may be blocking. This call also handles
     * reconnecting to the broker. 
    """
    def loopStart(self):
        self._mqtt.loop_start()

    def loopStop(self):
        self._mqtt.loop_stop()

    """
     * Occurs when connection is established.
    """
    def _onConnect(self, client, userdata, flags, rc):
        self._tryInvoke("connect")

    """
     * Occurs when the connection was lost.
    """
    def _onDisconnect(self, client, userdata, rc):
        self._tryInvoke("disconnect")

    """
     * Invokes the callback with a specific
    """    
    def _tryInvoke(self, name, args=None):
        if name in self._callbacks and self._callbacks[name] is not None:
            if args is None:
                self._callbacks[name]()
            else:
                self._callbacks[name](args)
            return

    """
     * Formats a channel for emitter.io protocol.
    """
    def _formatChannel(self, key, channel, options=None):
        # Prefix with the key.
        formatted = key + channel if key.endswith("/") else key + "/" + channel

        # Add trailing slash.
        if not formatted.endswith("/"):
            formatted = formatted + "/"

        # Add options.
        if options:
            formatted = "{formatted}?{querystring}".format(
                formatted=formatted,
                querystring=urlencode(options),
            )
        return formatted

    """
     * Connects to an Emitter server.
    """
    def connect(self, options={}):
        
        if "secure" not in options:
            options["secure"] = True

        # Default options.
        defaultConnectOptions = {
            "host": "api.emitter.io",
            "port": 443 if options["secure"] else 8080,
            "keepalive": 30
        }

        # Apply defaults.
        for k in defaultConnectOptions:
            options[k] = defaultConnectOptions[k] if k not in options else options[k]

        options["host"] = re.sub(r"/.*?:\/\//g", "", options["host"])
        self._callbacks = {}

        self._mqtt = mqtt.Client()

        if options["secure"]:
            ssl_ctx = ssl.create_default_context()
            self._mqtt.tls_set_context(ssl_ctx)
                    
        self._mqtt.on_connect = self._onConnect
        self._mqtt.on_disconnect = self._onDisconnect

        self._mqtt.connect(options["host"], port=options["port"], keepalive=options["keepalive"])

        def processMsg(client, userdata, msg):
            message = EmitterMessage(msg)
            if message.channel.startswith("emitter/keygen"):
                # This is a keygen message.
                self._tryInvoke("keygen", message.asObject())
            elif message.channel.startswith("emitter/presence"):
                # This is a presence message.
                self._tryInvoke("presence", message.asObject())
            else:
                # Do we have a message callback?
                self._tryInvoke("message", message)

        self._mqtt.on_message = processMsg

    """
     * Disconnects from the connected Emitter server.
    """
    def disconnect(self):
        self._mqtt.disconnect()

    """
    * Publishes a message to a channel.
    """
    def publish(self, key, channel, message, ttl=None):
        if type(key) is not str:
            logging.error("emitter.publish: request object does not contain a 'key' string.")
        if type(channel) is not str:
            logging.error("emitter.publish: request object does not contain a 'channel' string.")

        options = {}
        if ttl is not None:
            options["ttl"] = str(ttl)

        topic = self._formatChannel(key, channel, options)
        self._mqtt.publish(topic, message)

    """
    * Subscribes to a particual channel.
    """
    def subscribe(self, key, channel, last=None):
        if type(key) is not str:
            logging.error("emitter.publish: request object does not contain a 'key' string.")
        if type(channel) is not str:
            logging.error("emitter.publish: request object does not contain a 'channel' string.")
            
        options = {}
        if last is not None:
            options["last"] = str(last)

        topic = self._formatChannel(key, channel, options)
        self._mqtt.subscribe(topic)

    """
     * Registers a callback for different events.
    """
    def on(self, event, callback):
        # Validate the type.

        if event not in ["connect", "disconnect", "message", "keygen", "presence"]:
            logging.error("emitter.on: unknown event type, supported values are 'connect', 'disconnect', 'message', 'keygen', and 'presence'.");
        
        # Set the callback.
        self._callbacks[event] = callback

    """
     * Unsubscribes from a particular channel.
    """
    def unsubscribe(self, key, channel):
        if type(key) is not str:
            logging.error("emitter.publish: request object does not contain a 'key' string.")
        if type(channel) is not str:
            logging.error("emitter.publish: request object does not contain a 'channel' string.")
            
        topic = self._formatChannel(key, channel)
        self._mqtt.unsubscribe(topic)

    """
     * Sends a key generation request to the server.
    """
    def keygen(self, key, channel):
        if type(key) is not str:
            logging.error("emitter.publish: request object does not contain a 'key' string.")
        if type(channel) is not str:
            logging.error("emitter.publish: request object does not contain a 'channel' string.")

        request = {"key": key, "channel": channel}    
        # Publish the request.
        self._mqtt.publish("emitter/keygen/", json.dumps(request))

    """
     * Sends a presence request to the server.
    """
    def presence(self, key, channel):
        if type(key) is not str:
            logging.error("emitter.publish: request object does not contain a 'key' string.")
        if type(channel) is not str:
            logging.error("emitter.publish: request object does not contain a 'channel' string.")

        request = {"key": key, "channel": channel}
        # Publish the request.
        self._mqtt.publish("emitter/presence/", json.dumps(request))
        

"""
 * Represents a message received from the Emitter server.
"""
class EmitterMessage(object):

    """
     * Creates an instance of EmitterMessage.
    """
    def __init__(self, m):
        self.channel = m.topic
        self.binary = m.payload

    """
     * Returns the payload as a utf-8 string.
    """
    def asString(self):
        return str(self.binary)

    """
     * Returns the payload as a raw binary buffer.
    """
    def asBinary(self):
        return self.binary

    """
     * Returns the payload as an JSON-deserialized Python object.
    """
    def asObject(self):
        msg = None
        try:
            msg = json.loads(self.binary)
        except Exception as e:
            logging.exception(e)

        return msg
