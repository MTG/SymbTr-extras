import os
from symbtrextras.ScoreExtras import ScoreExtras
from symbtrextras.TxtExtras import TxtExtras
import tempfile
import shutil
import filecmp


_curr_folder = os.path.dirname(os.path.abspath(__file__))


def test_with_missing_first_row_usul_name_index_jumps():
    run_all_extras('sedaraban--sazsemaisi--aksaksemai----tanburi_cemil_bey')


def run_all_extras(symbtr_name):
    # I/O, change the name to the desired SymbTr-score accordingly
    txt_file = os.path.join(_curr_folder, 'data', symbtr_name + '.txt')
    mu2_file = os.path.join(_curr_folder, 'data', symbtr_name + '.mu2')
    xml_file = os.path.join(_curr_folder, 'data', symbtr_name + '.xml')

    # create temporary files
    txt_temp = _create_temporary_copy(txt_file)
    mu2_temp = _create_temporary_copy(mu2_file)

    try:
        # Change encoding to UTF-8
        ScoreExtras.change_encoding_to_utf8(txt_temp)
        ScoreExtras.change_encoding_to_utf8(mu2_temp)

        # Change the line break from \r\n (Windows) to \n (Unix)
        ScoreExtras.change_to_unix_linebreak(txt_temp)
        ScoreExtras.change_to_unix_linebreak(mu2_temp)

        # check mu2
        mu2_corrected = os.path.join(_curr_folder, 'data', symbtr_name +
                                     '--corrected.mu2')
        assert filecmp.cmp(mu2_temp, mu2_corrected), \
            'Fault in mu2-extras: {0:s}'.format(symbtr_name)

        # Add usul row if it is not present in the first row
        symbtr_csv = TxtExtras.add_usul_to_first_row(txt_temp, mu2_temp)

        with open(txt_temp, 'w') as f:
            f.write(symbtr_csv)

        # Check usul rows and attempt to fill missing information
        symbtr_csv = TxtExtras.check_usul_row(txt_temp)

        with open(txt_temp, 'w') as text_file:
            text_file.write(symbtr_csv)

        # Force the duration of all gracenotes to 0 and recompute the offset
        # column according to the usul cycle(s)
        symbtr_csv = TxtExtras.correct_offset_gracenote(txt_temp, mu2_temp)
        with open(txt_temp, 'w') as text_file:
            text_file.write(symbtr_csv)

        # check txt
        txt_corrected = os.path.join(_curr_folder, 'data', symbtr_name +
                                     '--corrected.txt')

        assert filecmp.cmp(txt_temp, txt_corrected),\
            'Fault in txt-extras: {0:s}'.format(symbtr_name)

        # Convert the txt file to MusicXML using the additional metadata from
        # mu2 files (and the MusicBrainz mbid)
        symbtr_xml = TxtExtras.to_musicxml(symbtr_name, txt_temp, mu2_temp)

        # with open(xml_file, 'w') as xml_file:
        #     xml_file.write(symbtr_xml)

        with open(xml_file, 'r') as xml_file:
            saved_xml = xml_file.read()

        assert symbtr_xml == saved_xml, \
            'Fault in xml-conversion: {0:s}'.format(symbtr_name)
    finally:  # remove temporary files
        os.remove(txt_temp)
        os.remove(mu2_temp)


def _create_temporary_copy(path):
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, os.path.basename(path))
    shutil.copy2(path, temp_path)
    return temp_path
