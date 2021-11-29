import os
import cffi

ffi = cffi.FFI()

sources = [os.path.join("lib", "sss", src) for src in ["sss.c", "hazmat.c", "randombytes.c", "tweetnacl.c"]]

ffi.set_source(
    "sss._ffi",
    "#include <sss.h>",
    include_dirs=[os.path.join("lib", "sss")],
    sources=sources
)

# Due to CFFI not supporting calculated values for #define directives and
# using as constants in exported functions, hard-coding the share length is a must.

ffi.cdef("""
#define sss_MLEN ...
#define sss_SHARE_LEN ...

typedef uint8_t sss_Share[113];

void sss_create_shares(sss_Share *out, const uint8_t *data, uint8_t n, uint8_t k);
int sss_combine_shares(uint8_t *data, uint8_t shares[][113], uint8_t k);
""")

if __name__ == "__main__":
    ffi.compile(verbose=True)