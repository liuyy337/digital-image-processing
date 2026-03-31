import numpy as np
from astropy.io import fits

def write_fits(filename, data):
    dtype2bitpix = {
        np.dtype('uint8'): 8,
        np.dtype('int16'): 16,
        np.dtype('int32'): 32,
        np.dtype('int64'): 64,
        np.dtype('float32'): -32,
        np.dtype('float64'): -64
    }
    bitpix = dtype2bitpix[data.dtype]

    big_endian_data = data.astype(data.dtype.newbyteorder('>'))
    header_cards = []
    
    def add_card(keyword, value, comment=""):
        keyword_str = f"{keyword:<8}"[:8]
        if isinstance(value, bool):
            val_str = "T" if value else "F"
            val_field = f"{val_str:>20}"
        elif isinstance(value, int):
            val_field = f"{value:>20}"
        else:
            val_field = f"'{value}'"[:20].ljust(20)
        card_str = f"{keyword_str}= {val_field} / {comment}"
        header_cards.append(f"{card_str:<80}"[:80].encode('ascii'))

    add_card("SIMPLE", True, "conforms to FITS standard")
    add_card("BITPIX", bitpix, "Bits per pixel")
    add_card("NAXIS", data.ndim, "Number of array dimensions")
    
    # 把 shape 逆序
    reversed_shape = data.shape[::-1]
    for i, dim_size in enumerate(reversed_shape, start=1):
        add_card(f"NAXIS{i}", dim_size, "")

    add_card("TELESCOP", "SDO", "NASA's Solar Dynamics Observatory")
    end_card = f"{'END':<80}".encode('ascii')
    header_cards.append(end_card)

    header_bytes = b"".join(header_cards)
    header_padding_len = (2880 - (len(header_bytes) % 2880)) % 2880
    header_bytes += b" " * header_padding_len
    data_bytes = big_endian_data.tobytes()
    data_padding_len = (2880 - (len(data_bytes) % 2880)) % 2880
    data_padding_bytes = b"\x00" * data_padding_len

    with open(filename, 'wb') as f:
        f.write(header_bytes)
        f.write(data_bytes)
        f.write(data_padding_bytes)
        
    print(f"Saved: {filename}")
    print(f"Header: {len(header_bytes)} bytes")
    print(f"Data: {len(data_bytes) + len(data_padding_bytes)} bytes")

if __name__ == "__main__":
    with fits.open('hw2/sdo_image.fits') as hdul:
        data = hdul[0].data
    data = data.astype(np.float32)
    write_fits("hw2/output.fits", data)