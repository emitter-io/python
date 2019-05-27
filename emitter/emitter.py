#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is the Python client for Emitter (emitter.io).
GitHub: github.com/emitter-io/python
License: Eclipse Public License 1.0 (EPL-1.0)
"""
import json
import re
import logging
import ssl
import paho.mqtt.client as mqtt
from .subtrie import SubTrie


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

		elif message.channel.startswith("emitter/presence"):
			# This is a presence message.
			self._invoke_trie_handlers(self._handler_trie_presence, self._handler_presence, message)

		elif self._handler_error and message.channel.startswith("emitter/error"):
			# This is an error message.
			self._handler_error(message.as_object())

		elif self._handler_me and message.channel.startswith("emitter/me"):
			# This is a "me" message, giving information about the connection.
			self._handler_me(message.as_object())
	
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

	def publish(self, key, channel, message, options={}):
		"""
		* Publishes a message to a channel.
		"""
		topic = self._format_channel(key, channel, options)
		qos, retain = Client._get_header(options)

		self._mqtt.publish(topic, message, qos=qos, retain=retain)

	def subscribe(self, key, channel, optional_handler=None, options={}):
		"""
		* Subscribes to a particual share group.
		"""
		if optional_handler is not None:
			self._handler_trie_message.insert(channel, optional_handler)

		topic = Client._format_channel(key, channel, options)
		self._mqtt.subscribe(topic)

	def subscribe_with_group(self, key, channel, share_group, optional_handler=None, options={}):
		"""
		* Subscribes to a particual share group.
		"""
		if optional_handler is not None:
			self._handler_trie_message.insert(channel, optional_handler)

		topic = Client._format_channel_share(key, channel, share_group, options)
		self._mqtt.subscribe(topic)

	def unsubscribe(self, key, channel):
		"""
		* Unsubscribes from a particular channel.
		"""
		self._handler_trie_message.delete(channel)
		topic = self._format_channel(key, channel)
		self._mqtt.unsubscribe(topic)

	def disconnect(self):
		"""
		* Disconnects from the connected Emitter server.
		"""
		self._mqtt.disconnect()

	def presence(self, key, channel, status=False, changes=False, optional_handler=None):
		"""
		* Sends a presence request to the server.
		"""
		if optional_handler is not None:
			self._handler_trie_presence.insert(channel, optional_handler)

		request = {"key": key, "channel": channel, "status": status, "changes": changes}
		# Publish the request.
		self._mqtt.publish("emitter/presence/", json.dumps(request))

	def keygen(self, key, channel, permissions, ttl=0):
		"""
		* Sends a key generation request to the server.
		"""
		request = {"key": key, "channel": channel, "type": permissions, "ttl": ttl}
		# Publish the request.
		self._mqtt.publish("emitter/keygen/", json.dumps(request))

	def link(self, key, channel, name, private, subscribe, options={}):
		"""
		* Sends a link creation request to the server.
		"""
		formattedChannel = Client._format_channel_link(channel, options=options)
		request = {"key": key, "channel": formattedChannel, "name": name, "private": private, "subscribe": subscribe}

		# Publish the request.
		self._mqtt.publish("emitter/link/", json.dumps(request))

	def publish_with_link(self, link, message):
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

	@staticmethod
	def _get_header(options):
		retain = False
		qos = 0
		for o in options:
			if o == Client.RETAIN:
				retain = True
			elif o == Client.QOS1:
				qos = 1
		
		return qos, retain

	@staticmethod
	def _format_options(options):
		formatted = ""

		if options != None and len(options) > 0:
			formatted = "?"
			
			for i, o in enumerate(options):
			
				if o.startswith("+"):
					continue
			
				formatted += o

				if i < len(options) - 1:
					formatted += "&"

		return formatted


	@staticmethod
	def _format_channel(key, channel, options={}):
		k = key.strip("/")
		c = channel.strip("/")
		o = Client._format_options(options)

		formatted = "{key}/{channel}/{options}".format(key=k, channel=c, options=o)
		return formatted

	@staticmethod
	def _format_channel_link(channel, options={}):
		c = channel.strip("/")
		o = Client._format_options(options)

		formatted = "{channel}/{options}".format(channel=c, options=o)
		return formatted

	@staticmethod
	def _format_channel_share(key, channel, share_group, options={}):
		k = key.strip("/")
		c = channel.strip("/")
		s = share_group.strip("/")
		o = Client._format_options(options)

		formatted = "{key}/$share/{share}/{channel}/{options}".format(key=k, share=s, channel=c, options=o)
		return formatted

	RETAIN = "+r"
	QOS0 = "+0"
	QOS1 = "+1"

	@staticmethod
	def with_ttl(ttl):
		return "ttl=" + str(ttl)

	@staticmethod
	def without_echo():
		return "me=0"

	@staticmethod
	def with_last(last):
		return "last=" + str(last)

	@staticmethod
	def with_retain():
		return Client.RETAIN
	
	@staticmethod
	def with_at_most_once():
		return Client.QOS0
	
	@staticmethod
	def with_at_least_once():
		return Client.QOS1

	

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
