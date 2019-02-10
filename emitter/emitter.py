#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is the Python client for Emitter (emitter.io).
GitHub: github.com/emitter-io/python
License: Eclipse Public License 1.0 (EPL-1.0)
"""
import json
import logging
import re
import ssl
import paho.mqtt.client as mqtt

try:
	from urllib.parse import urlencode
except ImportError:
	from urllib import urlencode


class Emitter(object):
	"""
	* Represents the client connection to an Emitter server.
	"""

	def __init__(self):
		"""
		* Registrate the variables for later use.
		"""
		self._mqtt = None
		self._callbacks = {}

	def loop(self, timeout):
		"""
		* Call regularly to process network events. This call waits in select()
		* until the network socket is available for reading or writing, if
		* appropriate, then handles the incoming/outgoing data. This function
		* blocks for up to timeout seconds.
		* timeout must not exceed the keepalive value for the client or your
		* client will be regularly disconnected by the broker.
		"""
		self._mqtt.loop(timeout=timeout)

	def loopForever(self):
		"""
		* This is a blocking form of the network loop and will not return until the
		* client calls disconnect(). It automatically handles reconnecting.
		"""
		self._mqtt.loop_forever()

	def loopStart(self):
		"""
		* These functions implement a threaded interface to the network loop.
		* Calling loop_start() once, before or after connect*(), runs a thread in
		* the background to call loop() automatically. This frees up the main
		* thread for other work that may be blocking. This call also handles
		* reconnecting to the broker.
		"""
		self._mqtt.loop_start()

	def loopStop(self):
		"""
		* Stops the loop started in loopStart().
		* See loopStart() for more information.
		"""
		self._mqtt.loop_stop()

	def _onConnect(self, client, userdata, flags, rc):
		"""
		* Occurs when connection is established.
		"""
		self._tryInvoke("connect")

	def _onDisconnect(self, client, userdata, rc):
		"""
		* Occurs when the connection was lost.
		"""
		self._tryInvoke("disconnect")

	def _tryInvoke(self, name, args=None):
		"""
		* Invokes the callback with a specific
		"""
		if name in self._callbacks and self._callbacks[name] is not None:
			if args is None:
				self._callbacks[name]()
			else:
				self._callbacks[name](args)
			return

	@staticmethod
	def _formatChannel(key, channel, options=None):
		"""
		* Formats a channel for emitter.io protocol.
		"""
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

	def connect(self, options={}):
		"""
		* Connects to an Emitter server.
		"""

		def processMsg(client, userdata, msg):
			message = EmitterMessage(msg)
			if message.channel.startswith("emitter/keygen"):
				# This is a keygen message.
				self._tryInvoke("keygen", message.asObject())
			elif message.channel.startswith("emitter/presence"):
				# This is a presence message.
				self._tryInvoke("presence", message.asObject())
			elif message.channel.startswith("emitter/error"):
				# This is an error message.
				self._tryInvoke("error", message.asObject())
			elif message.channel.startswith("emitter/me"):
				# This is a "me" message, giving information about the connection.
				self._tryInvoke("me", message.asObject())
			else:
				# This is a text message.
				self._tryInvoke("message", message)

		# Default options.
		if "secure" not in options:
			options["secure"] = True
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
		self._mqtt.on_message = processMsg

		self._mqtt.connect(options["host"], port=options["port"], keepalive=options["keepalive"])

	def publish(self, key, channel, message, ttl=None, me=None):
		"""
		* Publishes a message to a channel.
		"""
		if not isinstance(key, str):
			logging.error("emitter.publish: request object does not contain a 'key' string.")
		if not isinstance(channel, str):
			logging.error("emitter.publish: request object does not contain a 'channel' string.")

		options = {}
		if ttl is not None:
			options["ttl"] = str(ttl)

		if me is not None:
			if me == True:
				options["me"] = 1
			else:
				options["me"] = 0

		topic = self._formatChannel(key, channel, options)
		self._mqtt.publish(topic, message)

	def subscribe(self, key, channel, last=None):
		"""
		* Subscribes to a particual channel.
		"""
		if not isinstance(key, str):
			logging.error("emitter.publish: request object does not contain a 'key' string.")
		if not isinstance(channel, str):
			logging.error("emitter.publish: request object does not contain a 'channel' string.")

		options = {}
		if last is not None:
			options["last"] = str(last)

		topic = self._formatChannel(key, channel, options)
		self._mqtt.subscribe(topic)

	def unsubscribe(self, key, channel):
		"""
		* Unsubscribes from a particular channel.
		"""
		if not isinstance(key, str):
			logging.error("emitter.publish: request object does not contain a 'key' string.")
		if not isinstance(channel, str):
			logging.error("emitter.publish: request object does not contain a 'channel' string.")

		topic = self._formatChannel(key, channel)
		self._mqtt.unsubscribe(topic)

	def disconnect(self):
		"""
		* Disconnects from the connected Emitter server.
		"""
		self._mqtt.disconnect()

	def on(self, event, callback):
		"""
		* Registers a callback for different events.
		"""
		# Validate the type.
		if event not in ["connect", "disconnect", "message", "keygen", "presence", "me", "error"]:
			logging.error("emitter.on: unknown event type, supported values are 'connect', 'disc" \
						  "onnect', 'message', 'keygen', 'presence', 'me', and 'error'.")

		# Set the callback.
		self._callbacks[event] = callback

	def presence(self, key, channel):
		"""
		* Sends a presence request to the server.
		"""
		if not isinstance(key, str):
			logging.error("emitter.publish: request object does not contain a 'key' string.")
		if not isinstance(channel, str):
			logging.error("emitter.publish: request object does not contain a 'channel' string.")

		request = {"key": key, "channel": channel}
		# Publish the request.
		self._mqtt.publish("emitter/presence/", json.dumps(request))

	def keygen(self, key, channel):
		"""
		* Sends a key generation request to the server.
		"""
		if not isinstance(key, str):
			logging.error("emitter.publish: request object does not contain a 'key' string.")
		if not isinstance(channel, str):
			logging.error("emitter.publish: request object does not contain a 'channel' string.")

		request = {"key": key, "channel": channel}
		# Publish the request.
		self._mqtt.publish("emitter/keygen/", json.dumps(request))
	
	def link(self, key, channel, name, private, subscribe, ttl=None, me=None):
		request = {"key": key, "channel": channel, "name": name, "private": private, "subscribe": subscribe}

		options = {}
		if ttl is not None:
			options["ttl"] = str(ttl)

		if me is not None:
			if me == True:
				options["me"] = 1
			else:
				options["me"] = 0

		# Publish the request.
		self._mqtt.publish("emitter/link/", json.dumps(request))

	def publishWithLink(self, link, message):
		# Publish the request.
		self._mqtt.publish(link, message)

	def me(self):
		self._mqtt.publish("emitter/me/", "")


class EmitterMessage(object):
	"""
	* Represents a message received from the Emitter server.
	"""

	def __init__(self, message):
		"""
		* Creates an instance of EmitterMessage.
		"""
		self.channel = message.topic
		self.binary = message.payload

	def asString(self):
		"""
		* Returns the payload as a utf-8 string.
		"""
		return str(self.binary)

	def asObject(self):
		"""
		* Returns the payload as an JSON-deserialized Python object.
		"""
		msg = None
		try:
			msg = json.loads(self.binary)
		except json.JSONDecodeError as exception:
			logging.exception(exception)

		return msg

	def asBinary(self):
		"""
		* Returns the payload as a raw binary buffer.
		"""
		return self.binary
