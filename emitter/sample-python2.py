from emitter import Client
import Tkinter
import json

emitter = Client()

root = Tkinter.Tk()

channel_key = tkinter.StringVar(root, value="8jMLP9F859oDyqmJ3aV4aqnmFZpxApvb")
#channel_key = tkinter.StringVar(root, value="aghbt67CuPawxQvoBfKZ8MpecpPoz7od")#local
channel = tkinter.StringVar(root, value="test/")
shortcut = tkinter.StringVar(root, value="a0")
text_message = tkinter.StringVar(root, value="Hello World")
share_group = tkinter.StringVar(root, value="sg")
share_group_key = tkinter.StringVar(root, value="b7FEsiGFQoSYA6qyeu1dDodFnO0ypp0f")
#share_group_key = tkinter.StringVar(root, value="Q_dM5ODuhWjaR_LNo886hVjoecvt5pMJ") #local

def connect():
	#emitter.connect(host="127.0.0.1", port=8080, secure=False)
	emitter.connect()

	emitter.on_connect = lambda: result_text.insert("0.0", "Connected\n\n")
	emitter.on_disconnect = lambda: result_text.insert("0.0", "Disconnected\n\n")
	emitter.on_presence = lambda p: result_text.insert("0.0", "Presence message: '" + p.as_string() + "'\n\n")
	emitter.on_message = lambda m: result_text.insert("0.0", "Message received on default handler, destined to " + m.channel + ": " + m.as_string() + "\n\n")
	emitter.on_error = lambda e: result_text.insert("0.0", "Error received: " + str(e) + "\n\n")
	emitter.on_me = lambda me: result_text.insert("0.0", "Information about Me received: " + str(me) +"\n\n")
	emitter.loop_start()

def disconnect():
	emitter.loop_stop()
	emitter.disconnect()

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
	emitter.presence(str_key, str_channel, status=True, changes=True)
	result_text.insert("0.0", "Presence on '" + str_channel + "' requested.\n\n")

def message(retain=False):
	if retain:
		emitter.publish(channel_key.get(), channel.get(), text_message.get(), {Client.with_retain()})
	else:
		emitter.publish(channel_key.get(), channel.get(), text_message.get(), {})
	result_text.insert("0.0", "Test message send through '" + channel.get() + "'.\n\n")

def link():
	str_key = channel_key.get()
	str_channel = channel.get()
	str_link = shortcut.get()
	emitter.link(str_key, str_channel, str_link, False, True)

def link_private():
	str_key = channel_key.get()
	str_channel = channel.get()
	str_link = shortcut.get()
	emitter.link(str_key, str_channel, str_link, True, True)

def pub_to_link():
	str_link = shortcut.get()
	emitter.publish_with_link(str_link, text_message.get())

def me():
	emitter.me()

# Col 1
Tkinter.Label(root, text="Channel : ").grid(column=1, row=1)
channel_entry = Tkinter.Entry(root, width=40, textvariable=channel)
channel_entry.grid(column=1, row=2)

Tkinter.Label(root, text="Channel key : ").grid(column=1, row=3)
channel_key_entry = Tkinter.Entry(root, width=40, textvariable=channel_key)
channel_key_entry.grid(column=1, row=4)

Tkinter.Label(root, text="Shortcut : ").grid(column=1, row=5)
shortcut_entry = Tkinter.Entry(root, width=40, textvariable=shortcut)
shortcut_entry.grid(column=1, row=6)

Tkinter.Label(root, text="Message : ").grid(column=1, row=7)
message_entry = Tkinter.Entry(root, width=40, textvariable=text_message)
message_entry.grid(column=1, row=8)

Tkinter.Label(root, text="Share group : ").grid(column=1, row=9)
share_entry = Tkinter.Entry(root, width=40, textvariable=share_group)
share_entry.grid(column=1, row=10)

Tkinter.Label(root, text="Share group key : ").grid(column=1, row=11)
share_key_entry = Tkinter.Entry(root, width=40, textvariable=share_group_key)
share_key_entry.grid(column=1, row=12)


# Col 2
connect_button = Tkinter.Button(root, text="Connect", width=30, command=connect)
connect_button.grid(column=2, row=1)

disconnect_button = Tkinter.Button(root, text="Disconnect", width=30, command=disconnect)
disconnect_button.grid(column=2, row=2)

subscribe_button = Tkinter.Button(root, text="Subscribe", width=30, command=subscribe)
subscribe_button.grid(column=2, row=4)

unsubscribe_button = Tkinter.Button(root, text="Unsubscribe", width=30, command=unsubscribe)
unsubscribe_button.grid(column=2, row=5)

subscribe_share_button = Tkinter.Button(root, text="Subscribe to share", width=30, command=subscribe_share)
subscribe_share_button.grid(column=2, row=6)

# Col 3
link_button = Tkinter.Button(root, text="Link to shortcut", width=30, command=link)
link_button.grid(column=3, row=1)

link_private_button = Tkinter.Button(root, text="Link to private channel", width=30, command=link_private)
link_private_button.grid(column=3, row=2)


send_button = Tkinter.Button(root, text="Publish to channel", width=30, command=message)
send_button.grid(column=3, row=4)

send_button = Tkinter.Button(root, text="Publish to channel with retain", width=30, command=lambda: message(retain=True))
send_button.grid(column=3, row=5)

pub_to_link_button = Tkinter.Button(root, text="Publish to link", width=30, command=pub_to_link)
pub_to_link_button.grid(column=3, row=6)

# Col 4
presence_button = Tkinter.Button(root, text="Presence", width=30, command=presence)
presence_button.grid(column=4, row=1)

me_button = Tkinter.Button(root, text="Me", width=30, command=me)
me_button.grid(column=4, row=2)

# Text area
result_text = Tkinter.Text(root, height=30, width=120)
result_text.grid(column=1, row=14, columnspan=4)

root.mainloop()