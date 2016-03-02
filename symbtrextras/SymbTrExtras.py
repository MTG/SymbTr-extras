# -*- coding: utf-8 -*-
from symbtrdataextractor import symbtrreader, extractor
import pandas as pd
import json

class TxtExtras:
    def __init__(self):
        self.symbtr_cols = ['Sira', 'Kod', 'Nota53', 'NotaAE', 'Koma53', 'KomaAE', 
               'Pay', 'Payda', 'Ms', 'LNS', 'Bas', 'Soz1', 'Offset']
        self.usul_dict = json.load(open('./symbtrextras/data/usul_extended.json','r'))

    @staticmethod
    def getSymbTrData(txt_file, mu2_file):
        txt_data = extractor.extract(txt_file)[0]
        mu2_header = symbtrreader.readMu2Header(mu2_file)[0]

        return extractor.merge(txt_data, mu2_header)  # merge        

    def addUsul2FirstRow(self, txt_file, mu2_file):
        # extract symbtr data
        data = self.getSymbTrData(txt_file, mu2_file)

        # get usul variant
        variant = {}
        for vrt in self.usul_dict[data['usul']['symbtr_slug']]['variants']:
            if vrt['mu2_name'] == data['usul']['mu2_name']:
                variant = vrt
                break

        # read the txt score
        df = pd.read_csv(txt_file, sep='\t')

        # create the usul row
        # 1    51            0    0    zaman    mertebe    0    usul_symbtr_internal_id    0    usul_mu2_name    0
        # 1    51            0    0    6    4    0    90    0    Yürüksemâî (6/4)    0
        usul_row = pd.DataFrame({'Sira':1, 'Kod':51, 'Nota53':'', 'NotaAE':'', 'Koma53':0, 'KomaAE':0,
            'Pay':int(variant['num_pulses']),'Payda':int(variant['mertebe']),'Ms':0,'Offset':0,
            'LNS':variant['symbtr_internal_id'],'Bas':0,'Soz1':variant['mu2_name']}, index=[0])

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
                
            df_usul = pd.concat([usul_row, df], ignore_index=True)[self.symbtr_cols]
        else:
            if not df.iloc[0]["LNS"] == usul_row.iloc[0]["LNS"]:
                print data['symbtr'] + " starts with a different usul row. Correcting..."
                df_usul = pd.concat([usul_row, df.ix[1:]], ignore_index=True)[self.symbtr_cols]
            else:
                print data['symbtr'] + " starts with the usul row. Skipping..."
                df_usul = df

        return df_usul.to_csv(None, sep='\t', index=False, encoding='utf-8')

    def correctOffsetGracenote(self, txt_file, mu2_file):
        # extract symbtr data
        data = self.getSymbTrData(txt_file, mu2_file)
        
        # get zaman and mertebe from usul variant
        for usul in self.usul_dict.values():
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
                offset_incr = 0 if row['Payda'] ==0 else float(row['Pay'])/row['Payda']*mertebe/zaman
            if index == 0:
                row['Offset'] = offset_incr
            else:
                prev_row = df.iloc[index-1]
                row['Offset'] = offset_incr + prev_row['Offset']
                        
            # change null to empty string
            for key, val in row.iteritems():
                if pd.isnull(val):
                    row[key] = ''
                    
            # make sure that "Sira" column continues consecutively
            row['Sira'] = index+1
            
            # reassign
            df.iloc[index] = row

        # warn if the last measure end prematurely, i.e. the last note does not have an integer offset
        if not (round(row['Offset']*10000)*0.0001).is_integer():
            print "Ends prematurely!"

        return df.to_csv(None, sep='\t', index=False, encoding='utf-8')
            