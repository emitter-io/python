from emitter import Client
import tkinter
import json

emitter = Client()

def connect():
	options = {"host": "192.168.0.10", "secure": False}
	#options = {"secure": False}
	emitter.connect(options)

	emitter.on_connect = lambda: result_text.insert("0.0", "Connected\n\n")
	emitter.on_disconnect = lambda: result_text.insert("0.0", "Disconnected\n\n")
	emitter.on_presence = lambda p: result_text.insert("0.0", "Presence message: '" + str(p) + "'\n\n")
	emitter.on_message = lambda m: result_text.insert("0.0", "Message received on default handler, destined to " + m.channel + ": " + m.as_string() + "\n\n")
	emitter.on_error = lambda e: result_text.insert("0.0", "Error received: " + str(e) + "\n\n")
	emitter.on_me = lambda me: result_text.insert("0.0", "Information about Me received: " + str(me) +"\n\n")
	emitter.loop_start()

def disconnect():
	emitter.loop_stop()
	emitter.disconnect()

def subscribe(share_group=None):
	str_key = emitter_key.get()
	str_channel = channel.get()
	emitter.subscribe(str_key,
	 str_channel,
	 optional_handler=lambda m: result_text.insert("0.0", "Message received on handler for " + str_channel + ": " + m.as_string() + "\n\n"),
	 share_group=share_group)
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

def message(retain=False):
	emitter.publish(emitter_key.get(), channel.get(), text_message.get(), retain=retain)
	result_text.insert("0.0", "Test message send through '" + channel.get() + "'.\n\n")

def link():
	str_key = emitter_key.get()
	str_channel = channel.get()
	str_link = shortcut.get()
	emitter.link(str_key, str_channel, str_link, False, True)

def link_private():
	str_key = emitter_key.get()
	str_channel = channel.get()
	str_link = shortcut.get()
	emitter.link(str_key, str_channel, str_link, True, True)

def pub_to_link():
	str_link = shortcut.get()
	emitter.publish_with_link(str_link, json.dumps({"key1": "value1", "key2": 2}))

def me():
	emitter.me()

root = tkinter.Tk()
#emitter_key = tkinter.StringVar(root, value="8jMLP9F859oDyqmJ3aV4aqnmFZpxApvb")
emitter_key = tkinter.StringVar(root, value="EckDAy4LHt_T0eTPSBK_0dmOAGhakMgI")#local
channel = tkinter.StringVar(root, value="test/")
shortcut = tkinter.StringVar(root, value="a0")
text_message = tkinter.StringVar(root, value="Hello World")
share_group = tkinter.StringVar(root, value="sg")

# Col 1
tkinter.Label(root, text="Emitter key : ").grid(column=1, row=1)
emitter_key_entry = tkinter.Entry(root, width=40, textvariable=emitter_key)
emitter_key_entry.grid(column=1, row=2)

tkinter.Label(root, text="Channel : ").grid(column=1, row=3)
channel_entry = tkinter.Entry(root, width=40, textvariable=channel)
channel_entry.grid(column=1, row=4)

tkinter.Label(root, text="Shortcut : ").grid(column=1, row=5)
shortcut_entry = tkinter.Entry(root, width=40, textvariable=shortcut)
shortcut_entry.grid(column=1, row=6)

tkinter.Label(root, text="Message : ").grid(column=1, row=7)
message_entry = tkinter.Entry(root, width=40, textvariable=text_message)
message_entry.grid(column=1, row=8)

tkinter.Label(root, text="Share group : ").grid(column=1, row=9)
share_entry = tkinter.Entry(root, width=40, textvariable=share_group)
share_entry.grid(column=1, row=10)


# Col 2
connect_button = tkinter.Button(root, text="Connect", width=30, command=connect)
connect_button.grid(column=2, row=1)

disconnect_button = tkinter.Button(root, text="Disconnect", width=30, command=disconnect)
disconnect_button.grid(column=2, row=2)

subscribe_button = tkinter.Button(root, text="Subscribe", width=30, command=subscribe)
subscribe_button.grid(column=2, row=4)

unsubscribe_button = tkinter.Button(root, text="Unsubscribe", width=30, command=unsubscribe)
unsubscribe_button.grid(column=2, row=5)

subscribe_button = tkinter.Button(root, text="Subscribe to share", width=30, command=lambda: subscribe(share_group.get()))
subscribe_button.grid(column=2, row=6)

# Col 3
link_button = tkinter.Button(root, text="Link to shortcut", width=30, command=link)
link_button.grid(column=3, row=1)

link_private_button = tkinter.Button(root, text="Link to private channel", width=30, command=link_private)
link_private_button.grid(column=3, row=2)


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

# Text area
result_text = tkinter.Text(root, height=30, width=120)
result_text.grid(column=1, row=12, columnspan=4)

root.mainloop()
