## Utilitiy Methods ##

## python imports

import os
import hashlib


def generate_file_md5(rootdir, filename, blocksize=2**20):
    md5 = hashlib.md5()
    with open( os.path.join(rootdir, filename) , "rb" ) as f:
        while True:
            buffer = f.read(blocksize)
            if not buffer:
                break
            md5.update( buffer )
    return md5.hexdigest()

def generate_file_sha(rootdir, filename, blocksize=2**20):
    sha  = hashlib.sha256()
    with open( os.path.join(rootdir, filename) , "rb" ) as f:
        while True:
            buffer = f.read(blocksize)
            if not buffer:
                break
            sha.update( buffer )
    return sha.hexdigest()