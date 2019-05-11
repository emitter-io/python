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
		self._handler_message = None
		self._handler_trie_message = SubTrie()
		self._handler_connect = None
		self._handler_disconnect = None
		self._handler_error = None
		self._handler_presence = None
		self._handler_trie_presence = SubTrie()
		self._handler_me = None
		self._handler_keygen = None

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
		if self._handler_connect:
			self._handler_connect()
		

	def _on_disconnect(self, client, userdata, rc):
		"""
		* Occurs when the connection was lost.
		"""
		if self._handler_disconnect:
			self._handler_disconnect()

	def _invoke_trie_handlers(self, trie, default_handler, message):
		handlers = trie.lookup(message.channel)
		if len(handlers) == 0 and default_handler:
				default_handler(message)

		for h in handlers:
			h(message)
		

	def _on_message(self, client, userdata, msg):
		message = EmitterMessage(msg)
		
		# Non-emitter messages are far more frequent, so if it is one, return earlier.
		if (not message.channel.startswith("emitter")):
			self._invoke_trie_handlers(self._handler_trie_message, self._handler_message, message)

		if self._handler_keygen and message.channel.startswith("emitter/keygen"):
			# This is a keygen message.
			self._handler_keygen(message.as_object())

		elif self._handler_presence and message.channel.startswith("emitter/presence"):
			# This is a presence message.
			self._invoke_trie_handlers(self._handler_trie_presence, self._handler_presence, message)

		elif self._handler_error and message.channel.startswith("emitter/error"):
			# This is an error message.
			self._handler_error(message.as_object())

		elif self._handler_me and message.channel.startswith("emitter/me"):
			# This is a "me" message, giving information about the connection.
			self._handler_me(message.as_object())
	
	@staticmethod
	def _format_channel(channel, key=None, options=None, share_group=None):
		"""
		* Formats a channel for emitter.io protocol.
		"""
		if key and len(key):
			if not share_group or not len(share_group):
				formatted = "{key}/{channel}/".format(
					key=key.strip("/"),
					channel=channel.strip("/"))
			else:
				formatted = "{key}/$share/{share_group}/{channel}/".format(
					key=key.strip("/"),
					share_group=share_group.strip("/"),
					channel=channel.strip("/"))
		else:
			formatted = channel if channel.endswith("/") else channel + "/"

		if options:
			formatted = "{formatted}?{querystring}".format(
					formatted=formatted,
					querystring=urlencode(options),
				)
		return formatted

	def connect(self, host="api.emitter.io", port=443, secure=True, keepalive=30):
		"""
		* Connects to an Emitter server.
		"""
		formatted_host = re.sub(r"/.*?:\/\//g", "", host)
		self._mqtt = mqtt.Client()

		if secure:
			ssl_ctx = ssl.create_default_context()
			self._mqtt.tls_set_context(ssl_ctx)

		self._mqtt.on_connect = self._on_connect
		self._mqtt.on_disconnect = self._on_disconnect
		self._mqtt.on_message = self._on_message

		self._mqtt.connect(host=formatted_host, port=port, keepalive=keepalive)

	def publish(self, key, channel, message, ttl=None, me=True, retain=False):
		"""
		* Publishes a message to a channel.
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

		topic = self._format_channel(channel, key, options)
		self._mqtt.publish(topic, message, retain=retain)

	def subscribe(self, key, channel, optional_handler=None, chan_options={}, share_group=None):
		"""
		* Subscribes to a particual channel.
		"""
		if not isinstance(key, str):
			logging.error("emitter.publish: request object does not contain a 'key' string.")
		if not isinstance(channel, str):
			logging.error("emitter.publish: request object does not contain a 'channel' string.")

		if optional_handler is not None:
			self._handler_trie_message.insert(channel, optional_handler)

		topic = self._format_channel(channel, key, chan_options, share_group)
		self._mqtt.subscribe(topic)

	def unsubscribe(self, key, channel):
		"""
		* Unsubscribes from a particular channel.
		"""
		if not isinstance(key, str):
			logging.error("emitter.publish: request object does not contain a 'key' string.")
		if not isinstance(channel, str):
			logging.error("emitter.publish: request object does not contain a 'channel' string.")

		self._handler_trie_message.delete(channel)
		topic = self._format_channel(channel, key)
		self._mqtt.unsubscribe(topic)

	def disconnect(self):
		"""
		* Disconnects from the connected Emitter server.
		"""
		self._mqtt.disconnect()

	def presence(self, key, channel):
		"""
		* Sends a presence request to the server.
		"""
		request = {"key": key, "channel": channel}
		# Publish the request.
		self._mqtt.publish("emitter/presence/", json.dumps(request))

	def keygen(self, key, channel):
		"""
		* Sends a key generation request to the server.
		"""
		request = {"key": key, "channel": channel}
		# Publish the request.
		self._mqtt.publish("emitter/keygen/", json.dumps(request))

	def link(self, key: str, channel: str, name: str, private: bool, subscribe: bool, ttl: int=None, me: bool=True):
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

		formattedChannel = self._format_channel(channel, options=options)
		request = {"key": key, "channel": formattedChannel, "name": name, "private": private, "subscribe": subscribe}

		# Publish the request.
		self._mqtt.publish("emitter/link/", json.dumps(request))

	def publish_with_link(self, link, message):
		"""
		* Sends a message through the link.
		"""
		if not isinstance(link, str):
			logging.error("emitter.publish_with_link: request object does not contain a 'key' string.")
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
