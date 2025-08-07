#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2025 Juan Monetta.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


from gnuradio import gr
import numpy as np
import socket
import os
import select

class uds_source(gr.sync_block):
    def __init__(self, socket_path="/tmp/clj_sdr.sock"):
        gr.sync_block.__init__(self,
            name="uds_source",
            in_sig=[],
            out_sig=[np.complex64])

        self.socket_path = socket_path
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

        try:
            self.sock.connect(self.socket_path)
            self.sock.sendall(b'\x02')
            
        except socket.error as e:
            print(f"[UDS Source] Error connecting to socket: {e}")
            raise

    def stop(self):
        try:                        
            self.sock.shutdown(socket.SHUT_WR)
            self.sock.close()
        except:
            pass
        return super().stop()

    def work(self, input_items, output_items):
        out = output_items[0]
        to_read = out.size * 8  # 8 bytes per complex64 (float32 + float32)
        try:
            ready, _, _ = select.select([self.sock], [], [], 0.1)
            if self.sock in ready:
                data = self.sock.recv(to_read)
                n = len(data) // 8
                if n > 0:
                    arr = np.frombuffer(data, dtype=np.complex64)
                    out[:n] = arr
                    return n
        except BlockingIOError:
            pass
        return 0
