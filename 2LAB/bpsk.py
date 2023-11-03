#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: BPSK_mod
# GNU Radio version: 3.10.1.1

from gnuradio import blocks
from gnuradio import channels
from gnuradio.filter import firdes
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation

## New Imports ##
import verificador as Ver
import numpy as np
import csv
## ########### ##



class bpsk(gr.top_block):
    #Change the initialization to recieve: noise, loopB
    def __init__(self, noise, loopB):
        gr.top_block.__init__(self, "BPSK_mod", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 8
        self.samp_rate = samp_rate = 32000
        self.rolloff = rolloff = 0.75
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(1.0,samp_rate,samp_rate/sps,rolloff,11*sps)
        self.noise = noise
        self.loopB = loopB
        self.BPSK = BPSK = digital.constellation_calcdist([-1+0j, 1+0j], [0, 1],
        2, 1, digital.constellation.AMPLITUDE_NORMALIZATION).base()

        ##################################################
        # Blocks
        ##################################################
        self.fir_filter_xxx_0 = filter.fir_filter_ccc(1, rrc_taps)
        self.fir_filter_xxx_0.declare_sample_delay(0)
        self.digital_symbol_sync_xx_0 = digital.symbol_sync_cc(
            digital.TED_SIGNAL_TIMES_SLOPE_ML,
            sps,
            loopB,
            1.0,
            1.0,
            1.5,
            1,
            digital.constellation_bpsk().base(),
            digital.IR_MMSE_8TAP,
            128,
            [])
        self.digital_constellation_modulator_0 = digital.generic_mod(
            constellation=BPSK,
            differential=False,
            samples_per_symbol=sps,
            pre_diff_code=True,
            excess_bw=rolloff,
            verbose=False,
            log=False,
            truncate=False)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=noise,
            frequency_offset=0.0,
            epsilon=1.0,
            taps=[1],
            noise_seed=0,
            block_tags=False)
        self.blocks_vector_source_x_0 = blocks.vector_source_b([240, 240, 240, 15, 15, 15, 240, 240, 240, ] + [10,29,43,10, 31, 66, 10, 35, 92, ] + [15, 15, 15, 240, 240, 240, 15, 15, 15, 0, 0, 0, 0, 0, 0, 0, 0], False, 1, [])
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_pack_k_bits_bb_0 = blocks.pack_k_bits_bb(8)
        self.blocks_file_sink_1 = blocks.file_sink(gr.sizeof_char*1, 'bpsk_rec.dat', False)
        self.blocks_file_sink_1.set_unbuffered(True)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, 'bpsk_sent.dat', False)
        self.blocks_file_sink_0.set_unbuffered(True)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_real_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.blocks_pack_k_bits_bb_0, 0), (self.blocks_file_sink_1, 0))
        self.connect((self.blocks_throttle_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.digital_constellation_modulator_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.fir_filter_xxx_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.blocks_pack_k_bits_bb_0, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.digital_symbol_sync_xx_0, 0))


    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_rrc_taps(firdes.root_raised_cosine(1.0,self.samp_rate,self.samp_rate/self.sps,self.rolloff,11*self.sps))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_rrc_taps(firdes.root_raised_cosine(1.0,self.samp_rate,self.samp_rate/self.sps,self.rolloff,11*self.sps))
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_rolloff(self):
        return self.rolloff

    def set_rolloff(self, rolloff):
        self.rolloff = rolloff
        self.set_rrc_taps(firdes.root_raised_cosine(1.0,self.samp_rate,self.samp_rate/self.sps,self.rolloff,11*self.sps))

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps
        self.fir_filter_xxx_0.set_taps(self.rrc_taps)

    def get_noise(self):
        return self.noise

    def set_noise(self, noise):
        self.noise = noise
        self.channels_channel_model_0.set_noise_voltage(self.noise)

    def get_loopB(self):
        return self.loopB

    def set_loopB(self, loopB):
        self.loopB = loopB
        self.digital_symbol_sync_xx_0.set_loop_bandwidth(self.loopB)

    def get_BPSK(self):
        return self.BPSK

    def set_BPSK(self, BPSK):
        self.BPSK = BPSK




def main(top_block_cls=bpsk, options=None):
    noise = np.arange(0, 4.1, 0.5)
    loopB = [round(num, 2) for num in np.arange(0, 0.501, 0.01)]

    results = [["Noise Voltage"]]
    results[0].extend(loopB)

    for n in noise:
        dif_list = [n]
        for lb in loopB:
            tb = top_block_cls(n, lb)

            def sig_handler(sig=None, frame=None):
                tb.stop()
                tb.wait()

                sys.exit(0)

            signal.signal(signal.SIGINT, sig_handler)
            signal.signal(signal.SIGTERM, sig_handler)

            tb.start()

            tb.wait()
            dif_list.append(Ver.runBPSK())
            print("Run over - Noise: {} Loop Bandwidth: {}".format(tb.noise, tb.loopB))
        results.append(dif_list)

    with open("results_bpsk.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(results)


if __name__ == '__main__':
    main()
