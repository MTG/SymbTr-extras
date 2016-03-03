# -*- coding: utf-8 -*-
from musicxmlconverter.symbtr2musicxml import symbtrscore
from ScoreExtras import ScoreExtras
import pandas as pd
import os


class TxtExtras:
    symbtr_cols = ['Sira', 'Kod', 'Nota53', 'NotaAE', 'Koma53', 'KomaAE',
                   'Pay', 'Payda', 'Ms', 'LNS', 'Bas', 'Soz1', 'Offset']

    def __init__(self):
        pass

    @classmethod
    def check_usul_row(cls, txt_file):
        mu2_usul_dict, inv_mu2_usul_dict = ScoreExtras.parse_usul_dict()

        df = pd.read_csv(txt_file, sep='\t', encoding='utf-8')

        symbtr_name = os.path.splitext(txt_file)[0]

        for index, row in df.iterrows():
            # change null to empty string
            row_changed = False
            for key, val in row.iteritems():
                if pd.isnull(val):
                    row[key] = ''
                    row_changed = True

            if row['Kod'] == 51:
                usul_id = row['LNS']
                usul_name = row['Soz1']
                if usul_name:  # name given
                    # check if the usul pair matches with the mu2dict
                    if mu2_usul_dict[usul_name]['id'] == usul_id:
                        if not mu2_usul_dict[usul_name]['zaman'] == row['Pay']:
                            print(symbtr_name + ', line ' + str(index) + ': ' + usul_name +
                                  ' and zaman does not match.')
                        if not mu2_usul_dict[usul_name]['mertebe'] == row['Payda']:
                            print(symbtr_name + ', line ' + str(index) + ': ' + usul_name +
                                  ' and mertebe does not match.')
                    else:
                        print(symbtr_name + ', line ' + str(index) + ': ' + usul_name +
                              ' and ' + str(usul_id) + ' does not match.')
                elif usul_id:
                    if usul_id == -1:
                        print(symbtr_name + ', line ' + str(index) + ': Missing usul info')
                    else:
                        print(symbtr_name + ', line ' + str(index) + ': Filling missing ' +
                              inv_mu2_usul_dict[usul_id]['mu2_name'])
                        row['Soz1'] = inv_mu2_usul_dict[usul_id]['mu2_name']
                        if not inv_mu2_usul_dict[usul_id]['zaman'] == row['Pay']:
                            print(symbtr_name + ', line ' + str(index) + ': ' + usul_name +
                                  ' and zaman does not match.')
                        if not inv_mu2_usul_dict[usul_id]['mertebe'] == row['Payda']:
                            print(symbtr_name + ', line ' + str(index) + ': ' + usul_name +
                                  ' and mertebe does not match.')
                        row_changed = True
                else:
                    print("Unexpected operation")

            # reassign
            if row_changed:
                df.iloc[index] = row

        return df.to_csv(None, sep='\t', index=False, encoding='utf-8')

    @classmethod
    def add_usul_to_first_row(cls, txt_file, mu2_file):
        # extract symbtr data
        data = ScoreExtras.get_symbtr_data(txt_file, mu2_file)

        # get usul variant
        variant = {}
        for vrt in ScoreExtras.usul_dict[data['usul']['symbtr_slug']]['variants']:
            if vrt['mu2_name'] == data['usul']['mu2_name']:
                variant = vrt
                break

        # read the txt score
        df = pd.read_csv(txt_file, sep='\t')

        # create the usul row
        # 1    51            0    0    zaman    mertebe    0    usul_symbtr_internal_id    0    usul_mu2_name    0
        # 1    51            0    0    6    4    0    90    0    Yürüksemâî (6/4)    0
        usul_row = pd.DataFrame({'Sira': 1, 'Kod': 51, 'Nota53': '', 'NotaAE': '', 'Koma53': 0, 'KomaAE': 0,
                                 'Pay': int(variant['num_pulses']), 'Payda': int(variant['mertebe']), 'Ms': 0,
                                 'Offset': 0,
                                 'LNS': variant['symbtr_internal_id'], 'Bas': 0, 'Soz1': variant['mu2_name']},
                                index=[0])

        if not df.iloc[0]['Kod'] == 51:
            for index, row in df.iterrows():
                # change null to empty string
                for key, val in row.iteritems():
                    if pd.isnull(val):
                        row[key] = ''

                # make sure that "Sira" column continues consecutively
                row['Sira'] = index + 2  # 2 instead of 1, since we also add the usul row to the start

                # reassign
                df.iloc[index] = row

            df_usul = pd.concat([usul_row, df], ignore_index=True)[cls.symbtr_cols]
        else:
            if not df.iloc[0]["LNS"] == usul_row.iloc[0]["LNS"]:
                print data['symbtr'] + " starts with a different usul row. Correcting..."
                df_usul = pd.concat([usul_row, df.ix[1:]], ignore_index=True)[cls.symbtr_cols]
            else:
                print data['symbtr'] + " starts with the usul row. Skipping..."
                df_usul = df

        return df_usul.to_csv(None, sep='\t', index=False, encoding='utf-8')

    @classmethod
    def correct_offset_gracenote(cls, txt_file, mu2_file):
        # extract symbtr data
        data = ScoreExtras.get_symbtr_data(txt_file, mu2_file)

        # get zaman and mertebe from usul variant
        for usul in ScoreExtras.usul_dict.values():
            for uv in usul['variants']:
                if uv['mu2_name'] == data['usul']['mu2_name']:
                    mertebe = uv['mertebe']
                    zaman = uv['num_pulses']
                    break

        # correct the offsets and the gracenote durations
        df = pd.read_csv(txt_file, sep='\t')
        for index, row in df.iterrows():
            # recompute the erroneous gracenotes with non-zero duration
            if row['Kod'] == 8 and row['Ms'] > 0:
                row['Pay'] = 0
                row['Payda'] = 0
                row['Ms'] = 0

            # recompute zaman and mertebe, if we hit kod 51
            if row['Kod'] == 51:
                zaman = row['Pay']
                mertebe = row['Payda']
                offset_incr = 0
            else:
                # compute offset
                offset_incr = 0 if row['Payda'] == 0 else float(row['Pay']) / row['Payda'] * mertebe / zaman
            if index == 0:
                row['Offset'] = offset_incr
            else:
                prev_row = df.iloc[index - 1]
                row['Offset'] = offset_incr + prev_row['Offset']

            # change null to empty string
            for key, val in row.iteritems():
                if pd.isnull(val):
                    row[key] = ''

            # make sure that "Sira" column continues consecutively
            row['Sira'] = index + 1

            # reassign
            df.iloc[index] = row

        # warn if the last measure end prematurely, i.e. the last note does not have an integer offset
        if not (round(row['Offset'] * 10000) * 0.0001).is_integer():
            print "Ends prematurely!"

        return df.to_csv(None, sep='\t', index=False, encoding='utf-8')

    @classmethod
    def to_musicxml(cls, symbtr_name, txt_file, mu2_file):
        mbids = ScoreExtras.get_mbids(symbtr_name)

        # MusicXML conversion
        piece = symbtrscore(txt_file, mu2_file, symbtrname=symbtr_name, mbid_url=mbids)
        return piece.convertsymbtr2xml(verbose=False)
