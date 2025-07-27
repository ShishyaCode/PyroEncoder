import os
import py_compile
import marshal
import zlib
import base64





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


def obfuscate_code(pyc_path):
    """Apply marshal, zlib, and base85 encoding in multiple layers"""
    with open(pyc_path, 'rb') as f:
        pyc_data = f.read()

    code_data = pyc_data[16:]


    code_obj = marshal.loads(code_data)

    step1 = marshal.dumps(code_obj)
    step2 = zlib.compress(step1)
    step3 = marshal.dumps(step2)
    step4 = zlib.compress(step3)
    step5 = base64.b85encode(step4)

    return step5


def generate_stub(encoded_payload):
    """Wrap the obfuscated payload in a decryption/execution stub"""
    stub = f"""
import base64 as __b, marshal as __m, zlib as __z
__d = {repr(encoded_payload)}
__d = __b.b85decode(__d)
__d = __z.decompress(__d)
__d = __m.loads(__d)
__d = __z.decompress(__d)
__c = __m.loads(__d)
getattr(__import__('builtins'), chr(101)+chr(120)+chr(101)+chr(99))(__c)
"""
    return stub


def save_stub(stub_code, output_path='obfuscated.py'):
    """Save the final stub to a Python file"""
    with open(output_path, 'w') as f:
        f.write(stub_code)


def obfuscate_python_script(source_path):
    """Full obfuscation workflow — returns the obfuscated code as a string"""
    if not os.path.isfile(source_path):
        print("Invalid input file.")
        return None

    pyc_path = compile_to_pyc(source_path)
    encoded = obfuscate_code(pyc_path)
    stub = generate_stub(encoded)

    os.remove(pyc_path)
    act_stub=f"\n{a}\n{CREDIT}\n{stub}"
    return act_stub  # Return the final obfuscated code


