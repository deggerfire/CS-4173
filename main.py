from pyngrok import ngrok
from components import window
from apis import host

# Setup the ngrok port
https_tunnel = ngrok.connect("5173", bind_tls=True)

# Make the main window object
window = window.Start(https_tunnel.public_url)

# Starts the main loop that keeps the program running
window.mainloop()

# Close the ngrok port (for when mainloop is broken)
ngrok.disconnect(https_tunnel.public_url)
print("Disconnect ngrok")
