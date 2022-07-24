import bluetooth

port = 1
sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect(("3C:71:BF:F9:69:4E", port))

sock.send("1")
sock.close()

