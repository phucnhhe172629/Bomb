import subprocess
import threading
import time
import socket

subprocess.run(["wget", "-P", "~", "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb"])

subprocess.run(["sudo", "dpkg", "-i", "~/cloudflared-linux-amd64.deb"])

def iframe_thread(port):
    while True:
        time.sleep(0.5)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        if result == 0:
            break
        sock.close()

    print("\nComfyUI finished loading, trying to launch cloudflared (if it gets stuck here, cloudflared is having issues)\n")

    # Start cloudflared tunnel to expose the service
    p = subprocess.Popen(["cloudflared", "tunnel", "--url", "http://127.0.0.1:{}".format(port)], 
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Check for the URL in the cloudflared output
    for line in p.stderr:
        l = line.decode()
        if "trycloudflare.com " in l:
            print("This is the URL to access ComfyUI:", l[l.find("http"):], end='')


# Start the iframe_thread targeting port 8188
threading.Thread(target=iframe_thread, daemon=True, args=(8188,)).start()

# Run your main application (ComfyUI in this case)
# Ensure that main.py exists in your directory and is configured properly
subprocess.run(["python", "main.py", "--dont-print-server"])
