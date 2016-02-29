# -*- coding: utf-8 -*-
from symbtrdataextractor import symbtrreader, extractor
import pandas as pd 
import json

class Extras:
    def __init__(self):
        self.symbtr_cols = ['Sira', 'Kod', 'Nota53', 'NotaAE', 'Koma53', 'KomaAE', 
               'Pay', 'Payda', 'Ms', 'LNS', 'Bas', 'Soz1', 'Offset']
        self.usuldict = json.load(open('./symbtrextras/data/usul_extended.json','r'))

    def addUsul2FirstRow(self, txt_file, mu2_file):
        # extract symbtr data
        txtdata = extractor.extract(txt_file)[0]
        mu2header = symbtrreader.readMu2Header(mu2_file)[0]

        data = extractor.merge(txtdata, mu2header)  # merge

        # get usul variant
        variant = {}
        for vrt in self.usuldict[data['usul']['symbtr_slug']]['variants']:
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
                row['Sira'] = index + 2

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