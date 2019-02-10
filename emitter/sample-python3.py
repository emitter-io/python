import emitter
import tkinter
import json

emitter = emitter.Emitter()

def connect():
    options = {"host": "127.0.0.1", "secure": False}
    emitter.connect(options)
    emitter.on("connect", lambda: resultText.insert("0.0", "Connected\n\n"))
    emitter.on("disconnect", lambda: resultText.insert("0.0", "Disconnected\n\n"))
    emitter.on("presence", lambda p: resultText.insert("0.0", "Presence message : '" + str(p) + "'\n\n"))
    emitter.on("message", lambda m: resultText.insert("0.0", "Message received: " + m.asString() + "\n\n"))
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
    emitter.link(strKey, strChannel)

def linkPrivate():
    strKey = emitterKey.get()
    strChannel = channel.get()
    emitter.linkPrivate(strKey, strChannel)

def pubShortcut():
	emitter.publishShortcut("a0", json.dumps({"key1": "value1", "key2": 2}))



root = tkinter.Tk()
#emitterKey = tkinter.StringVar(root, value="5xwvQ9CsH-DYx-P7aR2AzRddQIWYD94S")
emitterKey = tkinter.StringVar(root, value="EckDAy4LHt_T0eTPSBK_0dmOAGhakMgI")
channel = tkinter.StringVar(root, value="test/")

tkinter.Label(root, text="Emitter key : ").grid(column=1, row=1)
emitterKeyEntry = tkinter.Entry(root, width=40, textvariable=emitterKey)
emitterKeyEntry.grid(column=1, row=2)

tkinter.Label(root, text="Channel : ").grid(column=1, row=3)
channelEntry = tkinter.Entry(root, width=40, textvariable=channel)
channelEntry.grid(column=1, row=4)

connectButton = tkinter.Button(root, text="Connect", width=30, command=connect)
connectButton.grid(column=1, row=6)

disconnectButton = tkinter.Button(root, text="Disconnect", width=30, command=disconnect)
disconnectButton.grid(column=1, row=7)

subscribeButton = tkinter.Button(root, text="Subscribe", width=30, command=subscribe)
subscribeButton.grid(column=1, row=8)

unsubscribeButton = tkinter.Button(root, text="Unsubscribe", width=30, command=unsubscribe)
unsubscribeButton.grid(column=1, row=9)

presenceButton = tkinter.Button(root, text="Presence", width=30, command=presence)
presenceButton.grid(column=1, row=10)

sendButton = tkinter.Button(root, text="Send test message", width=30, command=message)
sendButton.grid(column=1, row=11)

#################
linkButton = tkinter.Button(root, text="Link", width=30, command=link)
linkButton.grid(column=2, row=3)

linkPrivateButton = tkinter.Button(root, text="Link Private", width=30, command=linkPrivate)
linkPrivateButton.grid(column=2, row=4)

pubShortcutButton = tkinter.Button(root, text="Publish to shortcut", width=30, command=pubShortcut)
pubShortcutButton.grid(column=2, row=5)
#################
resultText = tkinter.Text(root, height=30, width=120)
resultText.grid(column=1, row=12, columnspan=2)



root.mainloop()
