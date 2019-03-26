import emitter
import tkinter
import json

emitter = emitter.Client()

def connect():
	#options = {"host": "192.168.0.4", "secure": False}
	options = {"secure": False}
	emitter.connect(options)

	def m(m):
		result_text.insert("0.0", "Message received on " + m.channel + ": " + m.as_string() + "\n\n")

	emitter.on_connect = lambda: result_text.insert("0.0", "Connected\n\n")
	emitter.on_disconnect = lambda: result_text.insert("0.0", "Disconnected\n\n")
	emitter.on_presence = lambda p: result_text.insert("0.0", "Presence message: '" + str(p) + "'\n\n")
	emitter.on_message = m#lambda m: result_text.insert("0.0", "Message received on " + m.channel + ": " + m.asString() + "\n\n")
	emitter.on_error = lambda e: result_text.insert("0.0", "Error received: " + str(e) + "\n\n")
	emitter.on_me = lambda me: result_text.insert("0.0", "Information about Me received: " + str(me) +"\n\n")
	emitter.loop_start()

def disconnect():
	emitter.loop_stop()
	emitter.disconnect()

def subscribe():
	str_key = emitter_key.get()
	str_channel = channel.get()
	emitter.subscribe(str_key, str_channel)
	result_text.insert("0.0", "Subscribtion to '" + str_channel + "' requested.\n\n")

def unsubscribe():
	str_key = emitter_key.get()
	str_channel = channel.get()
	emitter.unsubscribe(str_key, str_channel)
	result_text.insert("0.0", "Unsubscribtion to '" + str_channel + "' requested.\n\n")

def presence():
	str_key = emitter_key.get()
	str_channel = channel.get()
	emitter.presence(str_key, str_channel)
	result_text.insert("0.0", "Presence on '" + str_channel + "' requested.\n\n")

def message():
	str_key = emitter_key.get()
	str_channel = channel.get()
	emitter.publish(str_key, str_channel, json.dumps({"key1": "value1", "key2": 2}))
	result_text.insert("0.0", "Test message send through '" + str_channel + "'.\n\n")

def link():
	str_key = emitter_key.get()
	str_channel = channel.get()
	strLink = shortcut.get()
	emitter.link(str_key, str_channel, strLink, False, True)

def linkPrivate():
	str_key = emitter_key.get()
	str_channel = channel.get()
	strLink = shortcut.get()
	emitter.link(str_key, str_channel, strLink, True, True)

def pubToLink():
	strLink = shortcut.get()
	emitter.publishWithLink(strLink, json.dumps({"key1": "value1", "key2": 2}))

def me():
	emitter.me()

root = tkinter.Tk()
emitter_key = tkinter.StringVar(root, value="5xZjIQp6GA9fpxso1Kslqnv8d4XVWCha")
#emitter_key = tkinter.StringVar(root, value="EckDAy4LHt_T0eTPSBK_0dmOAGhakMgI")#local
channel = tkinter.StringVar(root, value="test/")
shortcut = tkinter.StringVar(root, value="a0")

# Col 1
tkinter.Label(root, text="Emitter key : ").grid(column=1, row=1)
emitter_keyEntry = tkinter.Entry(root, width=40, textvariable=emitter_key)
emitter_keyEntry.grid(column=1, row=2)

tkinter.Label(root, text="Channel : ").grid(column=1, row=3)
channelEntry = tkinter.Entry(root, width=40, textvariable=channel)
channelEntry.grid(column=1, row=4)

tkinter.Label(root, text="Shortcut : ").grid(column=1, row=5)
shortcutEntry = tkinter.Entry(root, width=40, textvariable=shortcut)
shortcutEntry.grid(column=1, row=6)

# Col 2
connectButton = tkinter.Button(root, text="Connect", width=30, command=connect)
connectButton.grid(column=2, row=1)

disconnectButton = tkinter.Button(root, text="Disconnect", width=30, command=disconnect)
disconnectButton.grid(column=2, row=2)

subscribeButton = tkinter.Button(root, text="Subscribe", width=30, command=subscribe)
subscribeButton.grid(column=2, row=4)

unsubscribeButton = tkinter.Button(root, text="Unsubscribe", width=30, command=unsubscribe)
unsubscribeButton.grid(column=2, row=5)

# Col 3
linkButton = tkinter.Button(root, text="Link to shortcut", width=30, command=link)
linkButton.grid(column=3, row=1)

linkPrivateButton = tkinter.Button(root, text="Link to private channel", width=30, command=linkPrivate)
linkPrivateButton.grid(column=3, row=2)

sendButton = tkinter.Button(root, text="Publish to channel", width=30, command=message)
sendButton.grid(column=3, row=4)

pubToLinkButton = tkinter.Button(root, text="Publish to link", width=30, command=pubToLink)
pubToLinkButton.grid(column=3, row=5)

# Col 4
presenceButton = tkinter.Button(root, text="Presence", width=30, command=presence)
presenceButton.grid(column=4, row=1)

meButton = tkinter.Button(root, text="Me", width=30, command=me)
meButton.grid(column=4, row=2)

result_text = tkinter.Text(root, height=30, width=120)
result_text.grid(column=1, row=8, columnspan=4)

root.mainloop()
