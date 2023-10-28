try:
    from .emitter import Client, EmitterMessage
except ImportError:
    from emitter import Client, EmitterMessage
import tkinter
import json

emitter = Client()

root = tkinter.Tk()

channel_key = tkinter.StringVar(root, value="YIsqdAlw9z9-fNciR2lD5tpob4lPhbgz")
#channel_key = tkinter.StringVar(root, value="aghbt67CuPawxQvoBfKZ8MpecpPoz7od")#local
channel = tkinter.StringVar(root, value="test/")
shortcut = tkinter.StringVar(root, value="a0")
text_message = tkinter.StringVar(root, value="Hello World")
share_group = tkinter.StringVar(root, value="sg")
share_group_key = tkinter.StringVar(root, value="b7FEsiGFQoSYA6qyeu1dDodFnO0ypp0f")
#share_group_key = tkinter.StringVar(root, value="Q_dM5ODuhWjaR_LNo886hVjoecvt5pMJ") #local
master_key = tkinter.StringVar(root, value="CH85YZ_730kfasMZfLtWwlygtmVIYvXQ")

def connect():
	emitter.connect(host="127.0.0.1", port=8080, secure=False)
	#emitter.connect()

	emitter.on_connect = lambda: result_text.insert("0.0", "Connected\n\n")
	emitter.on_disconnect = lambda: result_text.insert("0.0", "Disconnected\n\n")
	emitter.on_presence = lambda p: result_text.insert("0.0", "Presence message on channel: '" + str(p) + "'\n\n")
	emitter.on_message = lambda m: result_text.insert("0.0", "Message received on default handler, destined to " + m.channel + ": " + m.as_string() + "\n\n")
	emitter.on_error = lambda e: result_text.insert("0.0", "Error received: " + str(e) + "\n\n")
	emitter.on_me = lambda me: result_text.insert("0.0", "Information about Me received: " + str(me) + "\n\n")
	emitter.on_keyban = lambda kb: result_text.insert("0.0", "Keyban message received: " + str(kb) + "\n\n")
	emitter.on_history = lambda h : on_history(h)
	emitter.on_keygen = on_keygen
	emitter.loop_start()

# Can't select the key in the text area.
def on_keygen(message):
	result_text.insert("0.0", "Keygen: " + str(message) + "\n\n")
	print(message)

def disconnect():
	emitter.loop_stop()
	emitter.disconnect()


prev_history = None
def on_history(h):
	if len(h["messages"]):
		result_text.insert("0.0", "History message received: " + str(h) + "\n\n")
		global prev_history
		if len(h["messages"]):
			prev_history = h["messages"][0]["id"]
	else:
		prev_history = None
		result_text.insert("0.0", "No more messages in history " + str(h) + "\n\n")

def history():
	str_key = channel_key.get()
	str_channel = channel.get()
	emitter.history(str_key, prev_history)

def subscribe(share_group=None):
	str_key = channel_key.get()
	str_channel = channel.get()
	emitter.subscribe(str_key,
	 str_channel,
	 optional_handler=lambda m: result_text.insert("0.0", "Message received on handler for " + str_channel + ": " + m.as_string() + "\n\n"))
	result_text.insert("0.0", "Subscribtion to '" + str_channel + "' requested.\n\n")

def subscribe_share():
	str_key = share_group_key.get()
	str_channel = channel.get()
	str_share = share_group.get()
	emitter.subscribe_with_group(str_key,
	 str_channel,
	 optional_handler=lambda m: result_text.insert("0.0", "Message received on handler for " + str_channel + ": " + m.as_string() + "\n\n"),
	 share_group=str_share)
	result_text.insert("0.0", "Subscribtion to '" + str_channel + "' requested.\n\n")

def unsubscribe():
	str_key = channel_key.get()
	str_channel = channel.get()
	emitter.unsubscribe(str_key, str_channel)
	result_text.insert("0.0", "Unsubscribtion to '" + str_channel + "' requested.\n\n")

def presence():
	str_key = channel_key.get()
	str_channel = channel.get()
	emitter.presence(str_key, str_channel, status=True, changes=True) #optional_handler=lambda p: result_text.insert("0.0", "Optional handler: '" + str(p) + "'\n\n"))
	result_text.insert("0.0", "Presence on '" + str_channel + "' requested.\n\n")

def message(retain=False):
	if retain:
		emitter.publish(channel_key.get(), channel.get(), text_message.get(), {Client.with_retain()})
	else:
		emitter.publish(channel_key.get(), channel.get(), text_message.get(), {Client.with_ttl(999)})
	result_text.insert("0.0", "Test message sent through '" + channel.get() + "'.\n\n")

def link():
	str_key = channel_key.get()
	str_channel = channel.get()
	str_link = shortcut.get()
	emitter.link(str_key, str_channel, str_link, True)

def pub_to_link():
	str_link = shortcut.get()
	emitter.publish_with_link(str_link, text_message.get())

def me():
	emitter.me()

def keygen():
	str_master_key = master_key.get()
	str_channel = channel.get()
	emitter.keygen(str_master_key, str_channel, "rwlspx")

def keyban():
	str_target_key = channel_key.get()
	str_master_key = master_key.get()
	emitter.keyban(str_master_key, str_target_key, True)

def keyunban():
	str_target_key = channel_key.get()
	str_master_key = master_key.get()
	emitter.keyban(str_master_key, str_target_key, False)

# Col 1
tkinter.Label(root, text="Channel : ").grid(column=1, row=1)
channel_entry = tkinter.Entry(root, width=40, textvariable=channel)
channel_entry.grid(column=1, row=2)

tkinter.Label(root, text="Channel key : ").grid(column=1, row=3)
channel_key_entry = tkinter.Entry(root, width=40, textvariable=channel_key)
channel_key_entry.grid(column=1, row=4)

tkinter.Label(root, text="Shortcut : ").grid(column=1, row=5)
shortcut_entry = tkinter.Entry(root, width=40, textvariable=shortcut)
shortcut_entry.grid(column=1, row=6)

tkinter.Label(root, text="Message : ").grid(column=1, row=7)
message_entry = tkinter.Entry(root, width=40, textvariable=text_message)
message_entry.grid(column=1, row=8)

tkinter.Label(root, text="Share group : ").grid(column=1, row=9)
share_entry = tkinter.Entry(root, width=40, textvariable=share_group)
share_entry.grid(column=1, row=10)

tkinter.Label(root, text="Share group key : ").grid(column=1, row=11)
share_key_entry = tkinter.Entry(root, width=40, textvariable=share_group_key)
share_key_entry.grid(column=1, row=12)

tkinter.Label(root, text="Master key : ").grid(column=1, row=13)
share_key_entry = tkinter.Entry(root, width=40, textvariable=master_key)
share_key_entry.grid(column=1, row=14)

# Col 2
connect_button = tkinter.Button(root, text="Connect", width=30, command=connect)
connect_button.grid(column=2, row=1)

disconnect_button = tkinter.Button(root, text="Disconnect", width=30, command=disconnect)
disconnect_button.grid(column=2, row=2)

subscribe_button = tkinter.Button(root, text="Subscribe", width=30, command=subscribe)
subscribe_button.grid(column=2, row=4)

unsubscribe_button = tkinter.Button(root, text="Unsubscribe", width=30, command=unsubscribe)
unsubscribe_button.grid(column=2, row=5)

subscribe_share_button = tkinter.Button(root, text="Subscribe to share", width=30, command=subscribe_share)
subscribe_share_button.grid(column=2, row=6)

# Col 3
link_button = tkinter.Button(root, text="Link to shortcut", width=30, command=link)
link_button.grid(column=3, row=1)

send_button = tkinter.Button(root, text="Publish to channel", width=30, command=message)
send_button.grid(column=3, row=4)

send_button = tkinter.Button(root, text="Publish to channel with retain", width=30, command=lambda: message(retain=True))
send_button.grid(column=3, row=5)

pub_to_link_button = tkinter.Button(root, text="Publish to link", width=30, command=pub_to_link)
pub_to_link_button.grid(column=3, row=6)

# Col 4
presence_button = tkinter.Button(root, text="Presence", width=30, command=presence)
presence_button.grid(column=4, row=1)

me_button = tkinter.Button(root, text="Me", width=30, command=me)
me_button.grid(column=4, row=2)

keygen_button = tkinter.Button(root, text="Key gen", width=30, command=keygen)
keygen_button.grid(column=4, row=4)

keyban_button = tkinter.Button(root, text="Key ban", width=30, command=keyban)
keyban_button.grid(column=4, row=5)

keyunban_button = tkinter.Button(root, text="Key unban", width=30, command=keyunban)
keyunban_button.grid(column=4, row=6)

history_button = tkinter.Button(root, text="Get channel history", width=30, command=history)
history_button.grid(column=4, row=7)

# Text area
result_text = tkinter.Text(root, height=30, width=120)
result_text.grid(column=1, row=15, columnspan=4)

root.mainloop()
