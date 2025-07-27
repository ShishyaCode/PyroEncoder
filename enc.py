import os
import time
import base64
import marshal
import zlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from datetime import datetime, timedelta
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from random import randint,choice,shuffle
from binascii import hexlify

key = randint(3, 1000000)
ORIGINAL_KEY = b"ThisIsA32ByteLongEncryptionKey!!"
# Constants
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

credit=CREDIT

APPRECIATE = """#So finally you have decoded it??
#Nice Brother I appreciate your efforts 
#Dm me on telegram: @ShishyaCode and tell me about it"""

# Helper Functions
def generate_fake_code():
    return f'''
__key="abcdefghijklmnopqrstuvwxyz"
__ankush=["Kxz998760"]
x="""\n0-0-0-0-{('113, 71, 121, 78, 81, 51, 108, 51' * 1000).rstrip('=')}\n"""
'''

# Base64 Encoding
def base64_encode(data):
    encoded = base64.b64encode(data.encode('utf-8')).decode('utf-8')
    x1 = f"{CREDIT}\n\n{APPRECIATE}\n\nimport base64\nexec(base64.b64decode('{encoded}').decode('utf-8'))"

    enc2 = compile(x1, "<string>", "exec")
    marshaled = marshal.dumps(enc2)
    reversed_marshaled = marshaled[::-1]
    x2 = f"{CREDIT}\n\n_ = lambda __ : __import__('marshal').loads(__[::-1]);exec((_)({repr(reversed_marshaled)}))"

    compressed = zlib.compress(x2.encode('utf-8'))
    encodedx = compressed.hex()
    x3 = f"\nimport zlib\nexec(zlib.decompress(bytes.fromhex('{encodedx}')).decode('utf-8'))"

    fin_encoded = base64.b64encode(x3.encode('utf-8')).decode('utf-8')
    xfinal = f"{CREDIT}\n\nimport base64\nexec(base64.b64decode('{fin_encoded}').decode('utf-8'))"
    return xfinal

# Marshal Encoding
def marshal_encode(data):
    compiled_code = compile(data, "<string>", "exec")
    marshaled = marshal.dumps(compiled_code)
    reversed_marshaled = marshaled[::-1]
    x1 = f"{CREDIT}\n\n{APPRECIATE}\n\n_ = lambda __ : __import__('marshal').loads(__[::-1]);exec((_)({repr(reversed_marshaled)}))"

    enc2 = compile(x1, "<string>", "exec")
    marshaled = marshal.dumps(enc2)
    reversed_marshaled = marshaled[::-1]
    x2 = f"{CREDIT}\n\n_ = lambda __ : __import__('marshal').loads(__[::-1]);exec((_)({repr(reversed_marshaled)}))"

    compressed = zlib.compress(x2.encode('utf-8'))
    encodedx = compressed.hex()
    x3 = f"\nimport zlib\nexec(zlib.decompress(bytes.fromhex('{encodedx}')).decode('utf-8'))"

    compressed = zlib.compress(x3.encode('utf-8'))
    encodedx = compressed.hex()
    x4 = f"\nimport zlib\nexec(zlib.decompress(bytes.fromhex('{encodedx}')).decode('utf-8'))"
    compiled_code = compile(x4, "<string>", "exec")
    marshaledx = marshal.dumps(compiled_code)
    reversed_marshaledx = marshaledx[::-1]
    final_cont = f"{CREDIT}\n\n_ = lambda __ : __import__('marshal').loads(__[::-1]);exec((_)({repr(reversed_marshaledx)}))"
    return final_cont

# Zlib Encoding
def zlib_encode(data):
    compressed = zlib.compress(data.encode('utf-8'))
    return f"import zlib\nexec(zlib.decompress({repr(compressed)}).decode('utf-8'))"

def special_encode(data):
    """Multi-layer encoding: Base64 + Zlib + Marshal"""
    for _ in range(5):  # Increase for deeper obfuscation
        fake_code = generate_fake_code()
        method = repr(base64.b64encode(zlib.compress(marshal.dumps(compile(data, "", "exec"))))[::-1])
        data = f"{credit}\nexec(__import__('marshal').loads(__import__('zlib').decompress(__import__('base64').b64decode({method}[::-1]))))\n{credit}"

    obfuscated_chars = [ord(char) for char in data]
    encoded_script = f"{credit}\n_ = {obfuscated_chars}\nexec(''.join(chr(__) for __ in _))\n{credit}"

    return encoded_script

def multi_layer(data):
   

        code=special_encode(data)
        code1=zlib_enc(code)
        code2=marshal_encode(code1)
        code3=kramer(code2,key)
        code4=zlib_encode(code3)

        return code4

#=============================================================================
strings = "abcdefghijklmnopqrstuvwxyz0123456789"  # Do not change

class Key:
    @staticmethod
    def encrypt(e: str, key: str):
        e1 = Kyrie._ekyrie(e)
        return Kyrie._encrypt(e1, key=key)

    @staticmethod
    def decrypt(e: str, key: str):
        text = Kyrie._decrypt(e, key=key)
        return Kyrie._dkyrie(text)


def ran_int(min: int = 3, max: int = 1000000):
    return randint(min, max + 1)


class Kyrie:
    @staticmethod
    def encrypt(e: str):
        e = Kyrie._ekyrie(e)
        return Kyrie._encrypt(e)

    @staticmethod
    def decrypt(e: str):
        text = Kyrie._decrypt(e)
        return Kyrie._dkyrie(text)

    @staticmethod
    def _ekyrie(text: str):
        r = ""
        for a in text:
            if a in strings:
                a = strings[strings.index(a) - 1]
            r += a
        return r

    @staticmethod
    def _dkyrie(text: str):
        r = ""
        for a in text:
            if a in strings:
                i = strings.index(a) + 1
                if i >= len(strings):
                    i = 0
                a = strings[i]
            r += a
        return r

    @staticmethod
    def _encrypt(text: str, key: str = None):
        if type(key) == str:
            key = sum(ord(i) for i in key)
        t = [chr(ord(t) + key) if t != "\n" else "ζ" for t in text]
        return "".join(t)

    @staticmethod
    def _decrypt(text: str, key: str = None):
        if type(key) == str:
            key = sum(ord(i) for i in key)
        return "".join(chr(ord(t) - key) if t != "ζ" else "\n" for t in text)


def kramer(content: str, key: int) -> str:
    """Kyrie encryption logic."""
    _content_ = Key.encrypt(content, key=key)
    _lines_sep_ = '/'
    content = _lines_sep_.join(hexlify(x.encode()).decode() for x in _content_)
    _names_ = ["_eval", "_exec", "_byte", "_bytes", "_bit", "_bits", "_system", "_encode", "_decode", "_delete", "_exit", "_rasputin", "_execs"]
    _names_ = ["self." + name for name in _names_]
    shuffle(_names_)
    for k in range(12):
        globals()[f'n_{str(k + 1)}'] = _names_[k]
    _types_ = ("str", "float", "bool", "int")
    def _find(chars: str): return "+".join(f"_n7_[{list('abcdefghijklmnopqrstuvwxyz0123456789').index(c)}]" for c in chars)
    _1_ = fr"""_n5_""", fr"""lambda _n9_: "".join(__import__(_n7_[1]+_n7_[8]+_n7_[13]+_n7_[0]+_n7_[18]+_n7_[2]+_n7_[8]+_n7_[8]).unhexlify(str(_n10_)).decode()for _n10_ in str(_n9_).split('{_lines_sep_}'))"""
    _2_ = fr"""_n6_""", r"""lambda _n1_: str(_n4_[_n2_](f"{_n7_[4]+_n7_[-13]+_n7_[4]+_n7_[2]}(''.join(%s),{_n7_[6]+_n7_[11]+_n7_[14]+_n7_[1]+_n7_[0]+_n7_[11]+_n7_[18]}())"%list(_n1_))).encode(_n7_[20]+_n7_[19]+_n7_[5]+_n7_[34]) if _n4_[_n2_] == eval else exit()"""
    _3_ = fr"""_n4_[_n2_]""", fr"""eval"""
    _4_ = fr"""_n1_""", fr"""lambda _n1_: exit() if _n7_[15]+_n7_[17]+_n7_[8]+_n7_[13]+_n7_[19] in open(__file__, errors=_n7_[8]+_n7_[6]+_n7_[13]+_n7_[14]+_n7_[17]+_n7_[4]).read() else "".join(_n1_ if _n1_ not in _n7_ else _n7_[_n7_.index(_n1_)+1 if _n7_.index(_n1_)+1<len(_n7_) else 0] for _n1_ in "".join(chr(ord(t)-{key})if t!="ζ"else"\n"for t in _n5_(_n1_)))"""
    _5_ = fr"""_n7_""", fr"""exit()if _n1_ else 'abcdefghijklmnopqrstuvwxyz0123456789'"""
    _6_ = fr"""_n8_""", fr"""lambda _n12_:_n6_(_n1_(_n12_))"""
    _all_ = [_1_, _2_, _3_, _4_, _5_, _6_]
    shuffle(_all_)
    _vars_content_ = ",".join(s[0] for s in _all_)
    _valors_content_ = ",".join(s[1] for s in _all_)
    _vars_ = _vars_content_ + "=" + _valors_content_
    _final_content_ = fr"""class Shishya():
 def __decode__(self:object,_execute:str)->exec:return(None,_n8_(_execute))[0]
 def __init__(self:object,_n1_:{choice(_types_)}=False,_n2_:{choice(_types_)}=0,*_n3_:{choice(_types_)},**_n4_:{choice(_types_)})->exec:
  {_vars_}
  return self.__decode__(_n4_[(_n7_[-1]+'_')[-1]+_n7_[18]+_n7_[15]+_n7_[0]+_n7_[17]+_n7_[10]+_n7_[11]+_n7_[4]])
Shishya(_n1_=False,_n2_=False,_sparkle='''{content}''')""".strip().replace("_n1_", n_1.removeprefix("self.")).replace("_n2_", n_2.removeprefix("self.")).replace("_n3_", n_3.removeprefix("self.")).replace("_n4_", n_4.removeprefix("self.")).replace("_n5_", n_5).replace("_n6_", n_6).replace("_n7_", n_7).replace("_n8_", n_8).replace("_n9_", n_9.removeprefix("self.")).replace("_n10_", n_10.removeprefix("self.")).replace("_n12_", n_12.removeprefix("self."))
    # final_output = credit + "\n" + _final_content_

    compressed = zlib.compress(_final_content_.encode('utf-8'))
    encodedx = compressed.hex()  
    x3= f"\nimport zlib\nexec(zlib.decompress(bytes.fromhex('{encodedx}')).decode('utf-8'))" 

    compressed = zlib.compress(x3.encode('utf-8'))
    encodedx = compressed.hex()  
    x4= f"\nimport zlib\nexec(zlib.decompress(bytes.fromhex('{encodedx}')).decode('utf-8'))" 
    compiled_code = compile(x4, "<string>", "exec")
    marshaledx = marshal.dumps(compiled_code)  # Marshal the code
    reversed_marshaledx = marshaledx[::-1]  # Reverse the marshaled code
    final_cont=f"{CREDIT}\n\n_ = lambda __ : __import__('marshal').loads(__[::-1]);exec((_)({repr(reversed_marshaledx)}))" 


    _content_ = Key.encrypt(final_cont, key=key)
    _lines_sep_ = '/'
    content = _lines_sep_.join(hexlify(x.encode()).decode() for x in _content_)
    _names_ = ["_eval", "_exec", "_byte", "_bytes", "_bit", "_bits", "_system", "_encode", "_decode", "_delete", "_exit", "_rasputin", "_execs"]
    _names_ = ["self." + name for name in _names_]
    shuffle(_names_)
    for k in range(12):
        globals()[f'n_{str(k + 1)}'] = _names_[k]
    _types_ = ("str", "float", "bool", "int")
    def _find(chars: str): return "+".join(f"_n7_[{list('abcdefghijklmnopqrstuvwxyz0123456789').index(c)}]" for c in chars)
    _1_ = fr"""_n5_""", fr"""lambda _n9_: "".join(__import__(_n7_[1]+_n7_[8]+_n7_[13]+_n7_[0]+_n7_[18]+_n7_[2]+_n7_[8]+_n7_[8]).unhexlify(str(_n10_)).decode()for _n10_ in str(_n9_).split('{_lines_sep_}'))"""
    _2_ = fr"""_n6_""", r"""lambda _n1_: str(_n4_[_n2_](f"{_n7_[4]+_n7_[-13]+_n7_[4]+_n7_[2]}(''.join(%s),{_n7_[6]+_n7_[11]+_n7_[14]+_n7_[1]+_n7_[0]+_n7_[11]+_n7_[18]}())"%list(_n1_))).encode(_n7_[20]+_n7_[19]+_n7_[5]+_n7_[34]) if _n4_[_n2_] == eval else exit()"""
    _3_ = fr"""_n4_[_n2_]""", fr"""eval"""
    _4_ = fr"""_n1_""", fr"""lambda _n1_: exit() if _n7_[15]+_n7_[17]+_n7_[8]+_n7_[13]+_n7_[19] in open(__file__, errors=_n7_[8]+_n7_[6]+_n7_[13]+_n7_[14]+_n7_[17]+_n7_[4]).read() else "".join(_n1_ if _n1_ not in _n7_ else _n7_[_n7_.index(_n1_)+1 if _n7_.index(_n1_)+1<len(_n7_) else 0] for _n1_ in "".join(chr(ord(t)-{key})if t!="ζ"else"\n"for t in _n5_(_n1_)))"""
    _5_ = fr"""_n7_""", fr"""exit()if _n1_ else 'abcdefghijklmnopqrstuvwxyz0123456789'"""
    _6_ = fr"""_n8_""", fr"""lambda _n12_:_n6_(_n1_(_n12_))"""
    _all_ = [_1_, _2_, _3_, _4_, _5_, _6_]
    shuffle(_all_)
    _vars_content_ = ",".join(s[0] for s in _all_)
    _valors_content_ = ",".join(s[1] for s in _all_)
    _vars_ = _vars_content_ + "=" + _valors_content_
    _final_content_ = fr"""class Shishya():
 def __decode__(self:object,_execute:str)->exec:return(None,_n8_(_execute))[0]
 def __init__(self:object,_n1_:{choice(_types_)}=False,_n2_:{choice(_types_)}=0,*_n3_:{choice(_types_)},**_n4_:{choice(_types_)})->exec:
  {_vars_}
  return self.__decode__(_n4_[(_n7_[-1]+'_')[-1]+_n7_[18]+_n7_[15]+_n7_[0]+_n7_[17]+_n7_[10]+_n7_[11]+_n7_[4]])
Shishya(_n1_=False,_n2_=False,_sparkle='''{content}''')""".strip().replace("_n1_", n_1.removeprefix("self.")).replace("_n2_", n_2.removeprefix("self.")).replace("_n3_", n_3.removeprefix("self.")).replace("_n4_", n_4.removeprefix("self.")).replace("_n5_", n_5).replace("_n6_", n_6).replace("_n7_", n_7).replace("_n8_", n_8).replace("_n9_", n_9.removeprefix("self.")).replace("_n10_", n_10.removeprefix("self.")).replace("_n12_", n_12.removeprefix("self."))
    final_output = CREDIT + "\n" + _final_content_



    
    return final_output


kira_pre="""
#(+++++++++++++++++++++++++++++++)
#Welcome to ☠️ KiraX Encryption
#A special type of encyrption
#for your code
#(+++++++++++++++++++++++++++++++)
"""

def kira(data):
    data1=kramer(data,key)
    compressed = zlib.compress(data1.encode('utf-8'))
    encodedx = compressed.hex()  
    x3= f"\nimport zlib\nexec(zlib.decompress(bytes.fromhex('{encodedx}')).decode('utf-8'))" 

    data3=kramer(x3,key)
    compressed = zlib.compress(data3.encode('utf-8'))
    encodedx = compressed.hex()  
    x4= f"\n{kira_pre}\n{CREDIT}\nimport zlib\nexec(zlib.decompress(bytes.fromhex('{encodedx}')).decode('utf-8'))" 

    return x4






def zlib_enc(data):

    for xi in range(3):

        
        encoded = base64.b64encode(data.encode('utf-8')).decode('utf-8')
        x1= f"{credit}\n\nimport base64\nexec(base64.b64decode('{encoded}').decode('utf-8'))"

        compressed = zlib.compress(x1.encode('utf-8'))
        encodedx = compressed.hex()  
        x3= f"\n{credit}\nimport zlib\nexec(zlib.decompress(bytes.fromhex('{encodedx}')).decode('utf-8'))" 

        fin_encoded = base64.b64encode(x3.encode('utf-8')).decode('utf-8')
        xfinal= f"\n{credit}\n\nimport base64\nexec(base64.b64decode('{fin_encoded}').decode('utf-8'))"

        compressedx = zlib.compress(xfinal.encode('utf-8'))
        encodedxx = compressedx.hex()  
        x3x= f"{credit}\nimport zlib\nexec(zlib.decompress(bytes.fromhex('{encodedxx}')).decode('utf-8'))" 


    return x3x



def b85_enc(data):
        
    for i in range(3):

        data1= base64.b85encode(data.encode('utf-8')).decode('utf-8')
        x1= f"{credit}\n\nimport base64\nexec(base64.b85decode('{data1}').decode('utf-8'))"

        compressed = zlib.compress(x1.encode('utf-8'))
        encodedx = compressed.hex()  
        x3= f"\n{credit}\nimport zlib\nexec(zlib.decompress(bytes.fromhex('{encodedx}')).decode('utf-8'))" 

        data1= base64.b85encode(x3.encode('utf-8')).decode('utf-8')
        xfinal= f"{credit}\n\nimport base64\nexec(base64.b85decode('{data1}').decode('utf-8'))"


    return xfinal


def safe_url(data):
    for i in range(3):

        data1= base64.urlsafe_b64encode(data.encode('utf-8')).decode('utf-8')
        x1= f"{credit}\n\nimport base64\nexec(base64.urlsafe_b64decode('{data1}').decode('utf-8'))"

        compressed = zlib.compress(x1.encode('utf-8'))
        encodedx = compressed.hex()  
        x3= f"\n{credit}\nimport zlib\nexec(zlib.decompress(bytes.fromhex('{encodedx}')).decode('utf-8'))" 

        data2= base64.urlsafe_b64encode(x3.encode('utf-8')).decode('utf-8')
        xss= f"{credit}\n\nimport base64\nexec(base64.urlsafe_b64decode('{data2}').decode('utf-8'))"


    return xss





p_app="""
#Woww Trying to decode? huhh??
#nice nice continue...
"""
xypher_pre="""
#(+++++++++++++++++++++++++++++++)
#Welcome to ☠️ XypherX Encryption
#A special type of encyrption
#for your code
#(+++++++++++++++++++++++++++++++)
"""


def Cryptobase64_encode(data):



    for xi in range(2):

        
        encoded = base64.b64encode(data.encode('utf-8')).decode('utf-8')
        x1= f"{credit}\n\nimport base64\nexec(base64.b64decode('{encoded}').decode('utf-8'))"

        enc2=  compile(x1, "<string>", "exec")
        marshaled = marshal.dumps(enc2)  
        reversed_marshaled = marshaled[::-1]  
        x2= f"{p_app}\n{credit}\n\n_ = lambda __ : __import__('marshal').loads(__[::-1]);exec((_)({repr(reversed_marshaled)}))" 

        compressed = zlib.compress(x2.encode('utf-8'))
        encodedx = compressed.hex()  
        x3= f"\nimport zlib\nexec(zlib.decompress(bytes.fromhex('{encodedx}')).decode('utf-8'))" 

        fin_encoded = base64.b64encode(x3.encode('utf-8')).decode('utf-8')
        xfinal= f"{xypher_pre}\n{credit}\n\nimport base64\nexec(base64.b64decode('{fin_encoded}').decode('utf-8'))"


    return xfinal


def encrypt_file(data):
    data1= marshal_encode(data)
    data2=Cryptobase64_encode(data1)
    compressed = zlib.compress(data2.encode('utf-8'))
    encodedx = compressed.hex()  
    x3= f"{p_app}\nimport zlib\nexec(zlib.decompress(bytes.fromhex('{encodedx}')).decode('utf-8'))" 

    iv = os.urandom(16)

    # AES encryption
    cipher = AES.new(ORIGINAL_KEY, AES.MODE_CBC, iv)
    encrypted_data = iv + cipher.encrypt(pad(x3.encode('utf-8'), AES.block_size))  # Ensure the data is encoded as bytes
    encrypted_hex = hexlify(encrypted_data).decode("utf-8")
    
    return encrypted_hex

def generate_wrapper_script(encrypted_hex):
    """Generate the wrapper script for the encrypted file."""
    script_content = f"""
#(+++++++++++++++++++++++++++++++)
#Welcome to ☠️ XypherX Encryption
#A special type of encyrption
#for your code
#(+++++++++++++++++++++++++++++++)    
import os
os.system('pip install pycryptodome')
os.system('clear')
from binascii import unhexlify as decode_hex
from os import system as execute_command
key_part1 = "noLetyB23AsIsihT"[::-1]
key_part2 = "!!yeKnoitpyrcnEg"[::-1]
key = key_part1 + key_part2
Code = '.ShishyaPy'  
ShishyaPython = '{encrypted_hex}'  
with open(Code, 'wb') as file:
    file.write(decode_hex(ShishyaPython))
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
with open(Code, 'rb') as file:
    encrypted_data = file.read()
iv = encrypted_data[:16]
ciphertext = encrypted_data[16:]
cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
with open(Code, 'wb') as file:
    file.write(plaintext)
import os, stat
os.chmod(Code, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
execute_command('python ' + Code)
os.remove(Code)
"""
    return script_content

def final_crypto(data):
    encrypted_hex = encrypt_file(data)
    final_script = generate_wrapper_script(encrypted_hex)

    return final_script
