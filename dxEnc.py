import base64, zlib, marshal, binascii, codecs, hashlib, py_compile, tempfile, os
from itertools import cycle


a="#~~~*Enc By DxMods*~~~"

CREDIT = """
# ---------------------------------
# 🔐 Python Encoder - By Shishya
# 🌐 By ShishyaCode - Secure Your Code
# ---------------------------------
#_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
# 🕵️‍♂️ Decoding this? 
# 🔒 It's just a waste of time bro
# ⏳ Save your time for greatness.
# ---------------------------------
"""

def compile_to_pyc(source_path):
    """Compile a Python file to .pyc"""
    output_path = source_path + 'c'
    py_compile.compile(source_path, cfile=output_path)
    return output_path

def xor_encrypt(data: bytes, key: bytes) -> bytes:
    """XOR encryption using SHA256-derived key"""
    key_cycle = cycle(hashlib.sha256(key).digest())
    return bytes(b ^ next(key_cycle) for b in data)

def obfuscate_code(pyc_path, key=b'shishya_x'):
    """Compile, transform and deeply obfuscate Python code"""
    with open(pyc_path, 'rb') as f:
        pyc_data = f.read()

    code_data = pyc_data[16:]
    code_obj = marshal.loads(code_data)

    # Multi-layer encoding
    step1 = marshal.dumps(code_obj)
    step2 = zlib.compress(step1)
    step3 = marshal.dumps(step2)
    step4 = zlib.compress(step3)
    step5 = base64.b85encode(step4)
    step6 = xor_encrypt(step5, key)
    step7 = codecs.encode(step6.decode('latin1'), 'rot_13').encode('latin1')
    step8 = binascii.hexlify(step7)
    step9 = base64.b64encode(step8)

    # Final output as integer list
    return list(step9)

def write_stub(encoded_list, output_file, key=b'shishya_x'):
    stub = f'''

# ~~~*Enc BY RADHEY *~~
{CREDIT}
# THIS IS ENCODED BY YOU BABY | LOVE YOU RADHEY
import base64, zlib, marshal, binascii, codecs, hashlib
import sys
from itertools import cycle

def unlock(encoded_numbers):
    data = bytes(encoded_numbers)

    for attempt in range(2):
        try:
            try: data = base64.b64decode(data)
            except: pass
            
            try: data = binascii.unhexlify(data)
            except: pass
            
            try: data = codecs.decode(data.decode('latin1'), 'rot13').encode('latin1')
            except: pass
            
            try:
                data = bytes(b ^ k for b, k in zip(data, cycle(hashlib.sha256(b'{key.decode()}').digest())))
            except: pass
            
            try: data = base64.b85decode(data)
            except: pass
            
            try: data = zlib.decompress(data)
            except: pass
            
            try: data = marshal.loads(data)
            except: pass
            
            try: data = zlib.decompress(data)
            except: pass

            return marshal.loads(data)
        except Exception as e:
            if attempt == 1:
                print("❌ DECRYPTION ERROR:", str(e))
                sys.exit(1)
    raise ValueError("Decryption failed")

exec(unlock({encoded_list}))
'''
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(stub)
def Radhe_obfuscate(input_file, workspace=None):
    output_file = os.path.join(workspace or "", f"enc-{os.path.basename(input_file)}")
    key = b'shishya_x'

    compiled = compile_to_pyc(input_file)
    encoded = obfuscate_code(compiled, key=key)
    write_stub(encoded, output_file, key=key)

    # Clean up compiled file
    try:
        os.remove(compiled)
    except Exception:
        pass

    return output_file
