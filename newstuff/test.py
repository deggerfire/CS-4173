from pyngrok import ngrok
import time

# Open a HTTP tunnel on the default port 80
# <NgrokTunnel: "https://<public_sub>.ngrok.io" -> "http://localhost:80">
https_tunnel = ngrok.connect(bind_tls=True)


while True:
    print("Running " + https_tunnel.public_url)
    time.sleep(2.5)
