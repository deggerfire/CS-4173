from pyngrok import ngrok
from components import window
from apis import host


https_tunnel = ngrok.connect("5173", bind_tls=True)

window = window.Start(https_tunnel.public_url)

window.mainloop()

ngrok.disconnect(https_tunnel.public_url)
print("Disconnect ngrok")
