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
from subtrie import SubTrie

try:
	from urllib.parse import urlencode
except ImportError:
	from urllib import urlencode


class Client(object):
	"""
	* Represents the client connection to an Emitter server.
	"""

	def __init__(self):
		"""
		* Register the variables for later use.
		"""
		self._mqtt = None
		self._handler_trie = SubTrie()
		self._handler_connect = None
		self._handler_disconnect = None
		self._handler_error = None
		self._handler_presence = None
		self._handler_me = None
		self._handler_keygen = None


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

	def loop_forever(self):
		"""
		* This is a blocking form of the network loop and will not return until the
		* client calls disconnect(). It automatically handles reconnecting.
		"""
		self._mqtt.loop_forever()

	def loop_start(self):
		"""
		* These functions implement a threaded interface to the network loop.
		* Calling loop_start() once, before or after connect*(), runs a thread in
		* the background to call loop() automatically. This frees up the main
		* thread for other work that may be blocking. This call also handles
		* reconnecting to the broker.
		"""
		self._mqtt.loop_start()

	def loop_stop(self):
		"""
		* Stops the loop started in loopStart().
		* See loopStart() for more information.
		"""
		self._mqtt.loop_stop()


	def _on_connect(self, client, userdata, flags, rc):
		"""
		* Occurs when connection is established.
		"""
		#self._tryInvoke("connect")
		if self._handler_connect:
			self._handler_connect()
		

	def _on_disconnect(self, client, userdata, rc):
		"""
		* Occurs when the connection was lost.
		"""
		#self._tryInvoke("disconnect")
		if self._handler_disconnect:
			self._handler_disconnect()

	def _on_message(self, client, userdata, msg):
		message = EmitterMessage(msg)
		
		# Non-emitter messages are far more frequent, so if it is one, return earlier.
		if (not message.channel.startswith("emitter")):
			handlers = self._handler_trie.lookup(message.channel)
			if len(handlers) == 0 and self.on_message:
				self.on_message(message)

			for h in handlers:
				h(message)
			return

		if self._handler_keygen and message.channel.startswith("emitter/keygen"):
			# This is a keygen message.
			self._handler_keygen(message.as_object())

		elif self._handler_presence and message.channel.startswith("emitter/presence"):
			# This is a presence message.
			self._handler_presence(message.as_object())

		elif self._handler_error and message.channel.startswith("emitter/error"):
			# This is an error message.
			self._handler_error(message.as_object())

		elif self._handler_me and message.channel.startswith("emitter/me"):
			# This is a "me" message, giving information about the connection.
			self._handler_me(message.as_object())
	
	@property
	def on_connect(self):
		return self._handler_connect
	@on_connect.setter
	def on_connect(self, func):
		self._handler_connect = func

	@property
	def on_disconnect(self):
		return self._handler_disconnect
	@on_disconnect.setter
	def on_disconnect(self, func):
		self._handler_disconnect = func

	@property
	def on_error(self):
		return self._handler_error
	@on_error.setter
	def on_error(self, func):
		self._handler_error = func

	@property
	def on_presence(self):
		return self._handler_presence
	@on_presence.setter
	def on_presence(self, func):
		self._handler_presence = func

	@property
	def on_me(self):
		return self._handler_me
	@on_me.setter
	def on_me(self, func):
		self._handler_me = func

	@property
	def on_keygen(self):
		return self._handler_keygen
	@on_keygen.setter
	def on_keygen(self, func):
		self._handler_keygen = func

	@property
	def on_message(self):
		return self._handler_message
	@on_message.setter
	def on_message(self, func):
		self._handler_message = func

	@staticmethod
	def _format_channel(key, channel, options=None):
		"""
		* Formats a channel for emitter.io protocol.
		"""
		# Prefix with the key.
		formatted = channel
		if key and len(key):
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

		self._mqtt.on_connect = self._on_connect
		self._mqtt.on_disconnect = self._on_disconnect
		self._mqtt.on_message = self._on_message

		self._mqtt.connect(options["host"], port=options["port"], keepalive=options["keepalive"])

	def publish(self, key, channel, message, ttl=None, me=True):
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

		# The default server's behavior when 'me' is absent, is to send the publisher its own messages.
		# To avoid any ambiguity, this parameter is always set here.
		if me:
			options["me"] = 1
		else:
			options["me"] = 0

		topic = self._format_channel(key, channel, options)
		self._mqtt.publish(topic, message)

	def subscribe(self, key, channel, optional_handler=None, options={}):
		"""
		* Subscribes to a particual channel.
		"""
		if not isinstance(key, str):
			logging.error("emitter.publish: request object does not contain a 'key' string.")
		if not isinstance(channel, str):
			logging.error("emitter.publish: request object does not contain a 'channel' string.")

		#if last is not None:
		#	options["last"] = str(last)

		if optional_handler is not None:
			self._handler_trie.insert(channel, optional_handler)

		topic = self._format_channel(key, channel, options)
		self._mqtt.subscribe(topic)

	def unsubscribe(self, key, channel):
		"""
		* Unsubscribes from a particular channel.
		"""
		if not isinstance(key, str):
			logging.error("emitter.publish: request object does not contain a 'key' string.")
		if not isinstance(channel, str):
			logging.error("emitter.publish: request object does not contain a 'channel' string.")

		self._handler_trie.delete(channel)
		topic = self._format_channel(key, channel)
		self._mqtt.unsubscribe(topic)

	def disconnect(self):
		"""
		* Disconnects from the connected Emitter server.
		"""
		self._mqtt.disconnect()


	'''
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
	'''

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

	def link(self, key, channel, name, private, subscribe, ttl=None, me=True):
		"""
		* Sends a link creation request to the server.
		"""
		options = {}
		if ttl is not None:
			options["ttl"] = str(ttl)

		# The default server's behavior when 'me' is absent, is to send the publisher its own messages.
		# To avoid any ambiguity, this parameter is always set here.
		if me:
			options["me"] = 1
		else:
			options["me"] = 0

		formattedChannel = self._format_channel(None, channel, options)
		request = {"key": key, "channel": formattedChannel, "name": name, "private": private, "subscribe": subscribe}

		# Publish the request.
		self._mqtt.publish("emitter/link/", json.dumps(request))

	def publishWithLink(self, link, message):
		"""
		* Sends a message through the link.
		"""
		# Publish the request.
		self._mqtt.publish(link, message)

	def me(self):
		"""
		* Requests information about the connection.
		"""
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

	def as_string(self):
		"""
		* Returns the payload as a utf-8 string.
		"""
		return str(self.binary)

	def as_object(self):
		"""
		* Returns the payload as an JSON-deserialized Python object.
		"""
		msg = None
		try:
			msg = json.loads(self.binary)
		except json.JSONDecodeError as exception:
			logging.exception(exception)

		return msg

	def as_binary(self):
		"""
		* Returns the payload as a raw binary buffer.
		"""
		return self.binary
