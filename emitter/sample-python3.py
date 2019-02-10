import emitter
import tkinter
import json

emitter = emitter.Emitter()

def connect():
	options = {"host": "192.168.0.4", "secure": False}
	#options = {"secure": False}
	emitter.connect(options)
	emitter.on("connect", lambda: resultText.insert("0.0", "Connected\n\n"))
	emitter.on("disconnect", lambda: resultText.insert("0.0", "Disconnected\n\n"))
	emitter.on("presence", lambda p: resultText.insert("0.0", "Presence message: '" + str(p) + "'\n\n"))
	emitter.on("message", lambda m: resultText.insert("0.0", "Message received on " + m.channel + ": " + m.asString() + "\n\n"))
	emitter.on("error", lambda e: resultText.insert("0.0", "Error received: " + str(e) + "\n\n"))
	emitter.on("me", lambda me: resultText.insert("0.0", "Information about Me received: " + str(me) +"\n\n"))
	emitter.loopStart()

def disconnect():
	emitter.loopStop()
	emitter.disconnect()

def subscribe():
	strKey = emitterKey.get()
	strChannel = channel.get()
	emitter.subscribe(strKey, strChannel)
	resultText.insert("0.0", "Subscribtion to '" + strChannel + "' requested.\n\n")

def unsubscribe():
	strKey = emitterKey.get()
	strChannel = channel.get()
	emitter.unsubscribe(strKey, strChannel)
	resultText.insert("0.0", "Unsubscribtion to '" + strChannel + "' requested.\n\n")    

def presence():
	strKey = emitterKey.get()
	strChannel = channel.get()
	emitter.presence(strKey, strChannel)
	resultText.insert("0.0", "Presence on '" + strChannel + "' requested.\n\n")   

def message():
	strKey = emitterKey.get()
	strChannel = channel.get()
	emitter.publish(strKey, strChannel, json.dumps({"key1": "value1", "key2": 2}))
	resultText.insert("0.0", "Test message send through '" + strChannel + "'.\n\n") 
	
def link():
	strKey = emitterKey.get()
	strChannel = channel.get()
	strLink = shortcut.get()
	emitter.link(strKey, strChannel, strLink, False, True)

def linkPrivate():
	strKey = emitterKey.get()
	strChannel = channel.get()
	strLink = shortcut.get()
	emitter.link(strKey, strChannel, strLink, True, True)

def pubToLink():
	strLink = shortcut.get()
	emitter.publishWithLink(strLink, json.dumps({"key1": "value1", "key2": 2}))

def me():
	emitter.me()

root = tkinter.Tk()
#emitterKey = tkinter.StringVar(root, value="5xwvQ9CsH-DYx-P7aR2AzRddQIWYD94S")
#emitterKey = tkinter.StringVar(root, value="3YvSkz0vf-y68P58WThGUWhL12eV36z1")
emitterKey = tkinter.StringVar(root, value="EckDAy4LHt_T0eTPSBK_0dmOAGhakMgI")
channel = tkinter.StringVar(root, value="test/")
shortcut = tkinter.StringVar(root, value="a0")

# Col 1
tkinter.Label(root, text="Emitter key : ").grid(column=1, row=1)
emitterKeyEntry = tkinter.Entry(root, width=40, textvariable=emitterKey)
emitterKeyEntry.grid(column=1, row=2)

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

resultText = tkinter.Text(root, height=30, width=120)
resultText.grid(column=1, row=8, columnspan=4)

root.mainloop()
