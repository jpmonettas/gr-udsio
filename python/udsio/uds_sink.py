#!/usr/bin/python3

from gnuradio import gr
import numpy as np
import socket

class uds_sink(gr.sync_block):
    def __init__(self, socket_path="/tmp/clj_sdr.sock"):
        gr.sync_block.__init__(self,
            name="uds_sink",
            in_sig=[np.complex64],
            out_sig=[])

        self.socket_path = socket_path
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

        try:
            self.sock.connect(self.socket_path)
            self.sock.sendall(b'\x01')
        except socket.error as e:
            print(f"[UDS Sink] Error connecting to socket: {e}")
            raise

    def stop(self):
        try:
            self.sock.shutdown(socket.SHUT_WR)
            self.sock.close()
        except:
            pass
        return super().stop()

    def work(self, input_items, output_items):
        data = np.asarray(input_items[0], dtype=np.complex64).tobytes()
        try:
            self.sock.sendall(data)
        except socket.error as e:
            print(f"[UDS Sink] Send error: {e}")
            return -1
        return len(input_items[0])
