# -*- coding: utf-8 -*-
"""
Functional tests for sdypy.io sub-modules: uff, lvm, sfmov.

All imports go through the namespace: `from sdypy import io`.
Run with:
    <venv>/python.exe -m pytest tests -q
from the sdypy-io clone root.
"""
import struct
import numpy as np
import pytest

from sdypy import io


# ---------------------------------------------------------------------------
# 1. UFF round-trip: complex FRF-like data  (dataset 58, ascii, even spacing)
# ---------------------------------------------------------------------------

class TestUFFRoundTrip:
    """Write a dataset-58 FRF to a tmp file and read it back."""

    def _make_dataset(self, freq, data_complex):
        """Build a prepare_58 dict for a complex FRF."""
        return io.uff.prepare_58(
            binary=0,
            func_type=4,            # frequency response function
            rsp_node=1,
            rsp_dir=1,
            ref_node=1,
            ref_dir=1,
            rsp_ent_name='POINT_1',
            ref_ent_name='POINT_1',
            abscissa_spacing=1,     # even spacing → freq min + inc stored
            abscissa_spec_data_type=18,   # frequency
            ordinate_spec_data_type=12,
            orddenom_spec_data_type=13,
            data=data_complex,
            x=freq,
            id1='test FRF',
        )

    def test_complex_even_roundtrip(self, tmp_path):
        """Write complex FRF with even abscissa, read back, check np.allclose."""
        freq = np.linspace(0.0, 100.0, 50)
        np.random.seed(42)
        frf = (np.random.randn(50) + 1j * np.random.randn(50))

        dset = self._make_dataset(freq, frf)
        uff_path = str(tmp_path / "test_frf.uff")
        uff_obj = io.uff.UFF(uff_path)
        uff_obj.write_sets(dset, mode='overwrite')

        # Read back
        read_obj = io.uff.UFF(uff_path)
        result = read_obj.read_sets(0)

        assert result['type'] == 58
        assert np.allclose(result['data'].real, frf.real, atol=1e-6)
        assert np.allclose(result['data'].imag, frf.imag, atol=1e-6)
        # Frequency axis should match (at least first and last point)
        assert np.isclose(result['x'][0], freq[0], atol=1e-6)
        assert np.isclose(result['x'][-1], freq[-1], atol=1e-3)  # reconstructed from inc

    def test_real_even_roundtrip(self, tmp_path):
        """Write real-valued data (func_type=1 time series), read back."""
        freq = np.arange(0.0, 10.0, 1.0)  # 10 points, even spacing
        np.random.seed(7)
        values = np.random.randn(10)

        dset = io.uff.prepare_58(
            binary=0,
            func_type=1,            # general or time series
            rsp_node=2,
            rsp_dir=1,
            ref_node=1,
            ref_dir=1,
            abscissa_spacing=1,
            abscissa_spec_data_type=17,
            ordinate_spec_data_type=12,
            orddenom_spec_data_type=13,
            data=values,
            x=freq,
            id1='real data test',
        )
        uff_path = str(tmp_path / "real_data.uff")
        io.uff.UFF(uff_path).write_sets(dset, mode='overwrite')
        result = io.uff.UFF(uff_path).read_sets(0)

        assert result['type'] == 58
        assert np.allclose(result['data'], values, atol=1e-8)

    def test_multiple_sets_roundtrip(self, tmp_path):
        """Write two datasets, read both back."""
        freq = np.linspace(0.0, 50.0, 20)
        np.random.seed(99)
        frf1 = np.random.randn(20) + 1j * np.random.randn(20)
        frf2 = np.random.randn(20) + 1j * np.random.randn(20)

        dset1 = self._make_dataset(freq, frf1)
        dset2 = self._make_dataset(freq, frf2)

        uff_path = str(tmp_path / "multi.uff")
        uff_obj = io.uff.UFF(uff_path)
        uff_obj.write_sets([dset1, dset2], mode='overwrite')

        read_obj = io.uff.UFF(uff_path)
        assert read_obj.get_n_sets() == 2
        r1 = read_obj.read_sets(0)
        r2 = read_obj.read_sets(1)
        assert np.allclose(r1['data'].real, frf1.real, atol=1e-6)
        assert np.allclose(r2['data'].real, frf2.real, atol=1e-6)


# ---------------------------------------------------------------------------
# 2. LVM parse: write a minimal valid .lvm text file and parse it
# ---------------------------------------------------------------------------
# The LabVIEW Measurement File (lvm) format used by lvm_read.read_lines:
#
#   Global header section (key<TAB>value lines)
#   LabVIEW Measurement          <- ignored
#   ***End_of_Header***          <- ignored
#   <blank line>                 <- triggers new segment dict
#   Segment block:
#       Channels<TAB>N
#       <channel-meta lines: Delta_X, X0, Samples, Units, ...>
#       X_Value<TAB>Ch1<TAB>Ch2...  <- starts data; first_column = 1 when X_Columns=='No'
#       <data rows as floats, TAB-separated>
#   <blank line>                 <- ends segment
#
# lvm_read key rules observed from read_lines():
#   - lvm_data['X_Columns'] == 'No'  → skip column 0 of data rows (no explicit x column)
#   - first_column = 0 by default; set to 1 when X_Columns == 'No'
#   - nr_of_columns is updated to max(len(line_sp)-1, Channels)
# ---------------------------------------------------------------------------

LVM_TEMPLATE = (
    "LabVIEW Measurement\n"
    "Writer_Version\t2\n"
    "Reader_Version\t2\n"
    "Separator\tTab\n"
    "Decimal_Separator\t.\n"
    "Multi_Headings\tNo\n"
    "X_Columns\tNo\n"
    "Time_Pref\tRelative\n"
    "Operator\tTest\n"
    "Date\t2026-06-12\n"
    "Time\t12:00:00\n"
    "***End_of_Header***\n"
    "\n"                          # blank line → segment 0
    "Channels\t2\n"
    "Samples\t3\t3\n"
    "Date\t2026-06-12\t2026-06-12\n"
    "Time\t12:00:00\t12:00:00\n"
    "Y_Unit_Label\tV\tV\n"
    "X_Dimension\tTime\tTime\n"
    "X0\t0.00000000000000E+0\t0.00000000000000E+0\n"
    "Delta_X\t1\t1\n"
    "***End_of_Header***\n"
    "X_Value\tCh1\tCh2\n"
    "0\t1.0\t4.0\n"
    "1\t2.0\t5.0\n"
    "2\t3.0\t6.0\n"
    "\n"                          # blank line → segment ends
)


class TestLVMParse:
    """Write a minimal .lvm file and check lvm_read parses it correctly."""

    def _write_lvm(self, path):
        path.write_text(LVM_TEMPLATE, encoding='utf-8')

    def test_lvm_basic_parse(self, tmp_path):
        lvm_file = tmp_path / "test_data.lvm"
        self._write_lvm(lvm_file)

        # Pass read_from_pickle=False, dump_file=False to avoid pickle side-effects
        result = io.lvm.read(str(lvm_file), read_from_pickle=False, dump_file=False)

        assert 'Segments' in result
        assert result['Segments'] >= 1

    def test_lvm_segment_structure(self, tmp_path):
        lvm_file = tmp_path / "test_seg.lvm"
        self._write_lvm(lvm_file)

        result = io.lvm.read(str(lvm_file), read_from_pickle=False, dump_file=False)
        seg = result[0]

        assert 'data' in seg
        assert isinstance(seg['data'], np.ndarray)
        assert seg['data'].ndim == 2

    def test_lvm_numeric_roundtrip(self, tmp_path):
        """The two data columns must match what was written."""
        lvm_file = tmp_path / "test_numeric.lvm"
        self._write_lvm(lvm_file)

        result = io.lvm.read(str(lvm_file), read_from_pickle=False, dump_file=False)
        seg = result[0]
        data = seg['data']

        # X_Columns == 'No' means column 0 of the raw rows is skipped,
        # so data columns correspond to Ch1 and Ch2 (first_column=1 in reader).
        # The data array shape is (n_rows, n_channels_kept).
        # Ch1: [1,2,3]   Ch2: [4,5,6]
        expected_ch1 = np.array([1.0, 2.0, 3.0])
        expected_ch2 = np.array([4.0, 5.0, 6.0])

        assert data.shape[0] == 3, f"Expected 3 rows, got {data.shape[0]}"
        # With X_Columns='No', first_column=1 so data rows are trimmed to
        # columns [1:nr_of_columns+1]. nr_of_columns = Channels = 2 → cols 1..2
        # of the raw row [x, ch1, ch2]. Result columns: ch1=col0, ch2=col1.
        assert np.allclose(data[:, 0], expected_ch1), f"Ch1 mismatch: {data[:, 0]}"
        assert np.allclose(data[:, 1], expected_ch2), f"Ch2 mismatch: {data[:, 1]}"

    def test_lvm_header_fields(self, tmp_path):
        """Global header key/value fields are accessible in the top-level dict."""
        lvm_file = tmp_path / "test_header.lvm"
        self._write_lvm(lvm_file)

        result = io.lvm.read(str(lvm_file), read_from_pickle=False, dump_file=False)
        assert result.get('Decimal_Separator') == '.'
        assert result.get('Date') == '2026-06-12'


# ---------------------------------------------------------------------------
# 3. sfmov: parse test
#
# The sfmov format is a mixed text-header + raw binary file exported from
# FLIR ResearchIR. The parser (sfmov.py) works as follows:
#
#   get_meta_data(filename):
#       Opens in 'rt' mode with errors='ignore'.
#       Reads lines until it hits one whose first 11 chars == 'saf_padding'.
#       Each earlier line is split on ' ': meta[a[0]] = a[1].
#       Then casts meta['xPixls'], meta['yPixls'], meta['NumDPs'] to int.
#
#   get_data(filename):
#       Calls get_meta_data to get xPixls, yPixls, NumDPs, DaType.
#       Opens in 'rb', seeks to find(b'DATA')+6, then reads
#       np.fromfile(dtype) and reshapes to (-1, yPixls, xPixls).
#
# So a minimal synthetic .sfmov file must contain:
#   - Text header lines: "key value\n" for each metadata key
#   - The required keys are xPixls, yPixls, NumDPs, DaType
#   - A terminator line starting with 'saf_padding'
#   - Then some bytes (the gap of 6 after 'DATA'), then the binary payload
#
# 'DATA' marker: get_data does f.read().find(b'DATA')+6, so we must embed
# the literal bytes b'DATA' somewhere after the text header, followed by
# 2 bytes of padding, then the float32 pixel data.
# ---------------------------------------------------------------------------

def _make_sfmov(path, xPixls=4, yPixls=3, n_frames=2, dtype='Flt32'):
    """
    Write a minimal synthetic .sfmov file that sfmov.get_meta_data and
    sfmov.get_data can parse.

    File layout (all written in binary mode to avoid line-ending surprises):
        <text header lines as UTF-8>
        saf_padding ...\n
        <arbitrary gap bytes, does NOT contain b'DATA'>
        DATA\x00\x00    <- 'DATA' literal + 2 filler bytes (skip 6 from 'D')
        <raw float32 pixel data: n_frames * yPixls * xPixls values>
    """
    n_pixels = n_frames * yPixls * xPixls
    np.random.seed(13)
    pixel_data = np.random.rand(n_pixels).astype(np.float32)

    header_lines = (
        f"xPixls {xPixls}\n"
        f"yPixls {yPixls}\n"
        f"NumDPs {n_frames}\n"
        f"DaType {dtype}\n"
        "saf_padding 000000\n"
    )

    with open(path, 'wb') as f:
        f.write(header_lines.encode('utf-8'))
        # 'DATA' marker followed by exactly 2 filler bytes so that seek lands
        # at the start of pixel data (find(b'DATA')+6 skips 'D','A','T','A'
        # plus 2 filler bytes).
        f.write(b'DATA\x00\x00')
        f.write(pixel_data.tobytes())

    return pixel_data.reshape(n_frames, yPixls, xPixls)


class TestSfmov:
    """Tests for sfmov.get_meta_data and sfmov.get_data."""

    def test_sfmov_get_meta_data(self, tmp_path):
        """get_meta_data returns correct integer fields."""
        sf_path = str(tmp_path / "sample.sfmov")
        _make_sfmov(sf_path, xPixls=4, yPixls=3, n_frames=2)

        meta = io.sfmov.get_meta_data(sf_path)
        assert meta['xPixls'] == 4
        assert meta['yPixls'] == 3
        assert meta['NumDPs'] == 2
        assert meta['DaType'] == 'Flt32'

    def test_sfmov_get_data_shape(self, tmp_path):
        """get_data returns an array with shape (n_frames, yPixls, xPixls)."""
        sf_path = str(tmp_path / "sample_shape.sfmov")
        _make_sfmov(sf_path, xPixls=4, yPixls=3, n_frames=2)

        data = io.sfmov.get_data(sf_path)
        assert data.shape == (2, 3, 4)

    def test_sfmov_get_data_values(self, tmp_path):
        """Pixel values read back match the synthetic data written."""
        sf_path = str(tmp_path / "sample_vals.sfmov")
        expected = _make_sfmov(sf_path, xPixls=4, yPixls=3, n_frames=2)

        data = io.sfmov.get_data(sf_path)
        assert data.dtype == np.float32
        assert np.allclose(data, expected, atol=1e-6)

    def test_sfmov_nonexistent_file_raises(self, tmp_path):
        """Reading a nonexistent file raises an exception."""
        missing = str(tmp_path / "nonexistent.sfmov")
        with pytest.raises(Exception):
            io.sfmov.get_meta_data(missing)

    def test_sfmov_import(self):
        """sfmov module is importable and exposes the expected callables."""
        assert callable(io.sfmov.get_meta_data)
        assert callable(io.sfmov.get_data)
