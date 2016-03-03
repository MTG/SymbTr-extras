# -*- coding: utf-8 -*-
import json
import os
from symbtrdataextractor import symbtrreader, extractor


class ScoreExtras:
    _symbtr_mbid = json.load(open(  # load symbTr mbids
        os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     '..', '..', 'symbTr_mbid.json'), 'r'))
    usul_dict = json.load(open(  # usul dictionary
        os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     'data', 'usul_extended.json'), 'r'))

    def __init__(self):
        pass

    @staticmethod
    def get_symbtr_data(txt_file, mu2_file):
        txt_data = extractor.extract(txt_file)[0]
        mu2_header = symbtrreader.readMu2Header(mu2_file)[0]

        return extractor.merge(txt_data, mu2_header, verbose=False)

    @classmethod
    def get_mbids(cls, symbtr_name):
        mbids = []  # extremely rare but there can be more than one mbid
        for e in cls._symbtr_mbid:
            if e['name'] == symbtr_name:
                mbids.append(e['uuid'])
        return mbids

    @classmethod
    def parse_usul_dict(cls):
        mu2_usul_dict = {}
        inv_mu2_usul_dict = {}
        for key, val in cls.usul_dict.iteritems():
            for vrt in val['variants']:
                if vrt['mu2_name']:  # if it doesn't have a mu2 name, the usul is not in symbtr collection
                    zaman = int(vrt['num_pulses']) if vrt['num_pulses'] else []
                    mertebe = int(vrt['mertebe']) if vrt['mertebe'] else []
                    if vrt['mu2_name'] == '(Serbest)':
                        zaman = 0
                        mertebe = 0
                    mu2_usul_dict[vrt['mu2_name']] = {'id': int(vrt['symbtr_internal_id']), 'zaman': zaman,
                                                      'mertebe': mertebe}

                    inv_mu2_usul_dict[int(vrt['symbtr_internal_id'])] = {'mu2_name': vrt['mu2_name'],
                                                                         'zaman': zaman, 'mertebe': mertebe}
        return mu2_usul_dict, inv_mu2_usul_dict
