import hmac
import hashlib
import requests
import string
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import json
from protobuf_decoder.protobuf_decoder import Parser
import codecs
import time
from datetime import datetime
import urllib3
import base64
from flask import Flask, request, jsonify

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ---- مفتاح API للتحقق ----
API_KEY = "ZIKOB0SS"

# ---- ثوابت من السكريبت الأصلي ----
hex_Key = "32656534343831396539623435393838343531343130363762323831363231383734643064356437616639643866376530306331653534373135623764316533"
MaIn_KeY = bytes.fromhex(hex_Key)

ReGiOnMaP = {
    "ME": "ar", "IND": "hi", "ID": "id", "VN": "vi", "TH": "th",
    "BD": "bn", "PK": "ur", "TW": "zh", "EU": "en", "CIS": "ru",
    "NA": "en", "SAC": "es", "BR": "pt"
}

ReGiOnUrLs = {
    "IND": "https://client.ind.freefiremobile.com/",
    "ID": "https://clientbp.ggpolarbear.com/",
    "BR": "https://client.us.freefiremobile.com/",
    "ME": "https://clientbp.common.ggbluefox.com/",
    "VN": "https://clientbp.ggpolarbear.com/",
    "TH": "https://clientbp.common.ggbluefox.com/",
    "CIS": "https://clientbp.ggpolarbear.com/",
    "BD": "https://clientbp.ggpolarbear.com/",
    "PK": "https://clientbp.ggpolarbear.com/",
    "SG": "https://clientbp.ggpolarbear.com/",
    "NA": "https://client.us.freefiremobile.com/",
    "SAC": "https://client.us.freefiremobile.com/",
    "EU": "https://clientbp.ggpolarbear.com/",
    "TW": "https://clientbp.ggpolarbear.com/"
}

SUPERSCRIPT_MAP = {
    '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
    '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'
}

def to_superscript(num_str):
    return ''.join(SUPERSCRIPT_MAP.get(ch, ch) for ch in num_str)

def GeTlAnG(cOde):
    return ReGiOnMaP.get(cOde)

def GeTuRl(cOde):
    return ReGiOnUrLs.get(cOde)

def eNcVr(nUm):
    if nUm < 0:
        return b''
    rEsUlT = []
    while True:
        bYtE = nUm & 0x7F
        nUm >>= 7
        if nUm:
            bYtE |= 0x80
        rEsUlT.append(bYtE)
        if not nUm:
            break
    return bytes(rEsUlT)

def dEcUiD(hEx):
    n = s = 0
    for b in bytes.fromhex(hEx):
        n |= (b & 0x7F) << s
        if not b & 0x80:
            break
        s += 7
    return n

def cReAtEvAr(fIeLdNuM, vAl):
    fIeLdHeAdEr = (fIeLdNuM << 3) | 0
    return eNcVr(fIeLdHeAdEr) + eNcVr(vAl)

def cReAtElEnGtH(fIeLdNuM, vAl):
    fIeLdHeAdEr = (fIeLdNuM << 3) | 2
    eNcOdEd = vAl.encode() if isinstance(vAl, str) else vAl
    return eNcVr(fIeLdHeAdEr) + eNcVr(len(eNcOdEd)) + eNcOdEd

def cReAtEpRoTo(fIeLdS):
    pAcKeT = bytearray()
    for fIeLd, vAl in fIeLdS.items():
        if isinstance(vAl, dict):
            nEsTeD = cReAtEpRoTo(vAl)
            pAcKeT.extend(cReAtElEnGtH(fIeLd, nEsTeD))
        elif isinstance(vAl, int):
            pAcKeT.extend(cReAtEvAr(fIeLd, vAl))
        elif isinstance(vAl, (str, bytes)):
            pAcKeT.extend(cReAtElEnGtH(fIeLd, vAl))
    return pAcKeT

def eNcAeS(pLaInTeXt):
    pLaIn = bytes.fromhex(pLaInTeXt)
    kEy = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iV = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    cIpHeR = AES.new(kEy, AES.MODE_CBC, iV)
    rEsUlT = cIpHeR.encrypt(pad(pLaIn, AES.block_size))
    return bytes.fromhex(rEsUlT.hex())

def eNcApI(pT):
    pT = bytes.fromhex(pT)
    kEy = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iV = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    cIpHeR = AES.new(kEy, AES.MODE_CBC, iV)
    cT = cIpHeR.encrypt(pad(pT, AES.block_size))
    return cT.hex()

def gEnNaMe(prefix):
    digits = ''.join(str(random.randint(0, 9)) for _ in range(5))
    sup_digits = to_superscript(digits)
    return prefix + sup_digits

def gEnPaSsWoRd(lEn=9):
    cHaRs = string.ascii_letters + string.digits
    rAnD = ''.join(random.choice(cHaRs) for _ in range(lEn)).upper()
    return f"FPI{rAnD}ZAKARI"

def eNcOdEsTr(oRiG):
    kEyStReAm = [
        0x30, 0x30, 0x30, 0x32, 0x30, 0x31, 0x37, 0x30,
        0x30, 0x30, 0x30, 0x30, 0x32, 0x30, 0x31, 0x37,
        0x30, 0x30, 0x30, 0x30, 0x30, 0x32, 0x30, 0x31,
        0x37, 0x30, 0x30, 0x30, 0x30, 0x30, 0x32, 0x30
    ]
    eNcOdEd = ""
    for i in range(len(oRiG)):
        oRiGbYtE = ord(oRiG[i])
        kEyByTe = kEyStReAm[i % len(kEyStReAm)]
        rEsByTe = oRiGbYtE ^ kEyByTe
        eNcOdEd += chr(rEsByTe)
    return {"open_id": oRiG, "f14": eNcOdEd}

def tOuNiCoDeEsC(sTr):
    return ''.join(c if 32 <= ord(c) <= 126 else f'\\u{ord(c):04x}' for c in sTr)

def pArSeReSuLtS(pR):
    rD = {}
    for r in pR:
        fD = {}
        fD['wt'] = r.wire_type
        if r.wire_type == "varint":
            fD['data'] = r.data
        if r.wire_type == "string":
            fD['data'] = r.data
        if r.wire_type == "bytes":
            fD['data'] = r.data
        elif r.wire_type == 'length_delimited':
            fD["data"] = pArSeReSuLtS(r.data.results)
        rD[r.field] = fD
    return rD

def pArSeRoOm(iT):
    try:
        pR = Parser().parse(iT)
        pRo = pR
        pRd = pArSeReSuLtS(pRo)
        jD = json.dumps(pRd)
        return jD
    except Exception as e:
        return None

def cHoOsErEgIoN(dAtA, jWt):
    uRl = "https://loginbp.ggpolarbear.com/ChooseRegion"
    hEaDeRs = {
        'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 12; M2101K7AG Build/SKQ1.210908.001)",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Content-Type': "application/x-www-form-urlencoded",
        'Expect': "100-continue",
        'Authorization': f"Bearer {jWt}",
        'X-Unity-Version': "2018.4.11f1",
        'X-GA': "v1 1",
        'ReleaseVersion': "OB52"
    }
    rEs = requests.post(uRl, data=dAtA, headers=hEaDeRs, verify=False)
    return rEs.status_code

def gEtLoGiNdAtA(jWt, pL, rEg):
    if rEg.lower() == "me":
        uRl = 'https://clientbp.ggpolarbear.com/GetLoginData'
    else:
        lInK = GeTuRl(rEg)
        uRl = f"{lInK}GetLoginData"

    hEaDeRs = {
        'Expect': '100-continue',
        'Authorization': f'Bearer {jWt}',
        'X-Unity-Version': '2018.4.11f1',
        'X-GA': 'v1 1',
        'ReleaseVersion': 'OB52',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 10; G011A Build/PI)',
        'Host': 'clientbp.ggpolarbear.com',
        'Connection': 'close',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    
    mAxTrY = 3
    aTt = 0

    while aTt < mAxTrY:
        try:
            rEs = requests.post(uRl, headers=hEaDeRs, data=pL, verify=False)
            rEs.raise_for_status()
            x = rEs.content.hex()
            jR = pArSeRoOm(x)
            if jR is None:
                return None
            pD = json.loads(jR)
            return pD
        except Exception:
            aTt += 1
            time.sleep(2)
    return None

def gEtPaYlOaD(jWt, nAt, dAtE, rEsP, cOdE, nAmE, uId, pAsS, rEg):
    try:
        tPb = jWt.split('.')[1]
        tPb += '=' * ((4 - len(tPb) % 4) % 4)
        dP = base64.urlsafe_b64decode(tPb).decode('utf-8')
        dP = json.loads(dP)
        nEiD = dP['external_id']
        sMd5 = dP['signature_md5']
        
        nOw = datetime.now()
        nOw = str(nOw)[:len(str(nOw)) - 7]
        
        pL = b':\x071.111.2\xaa\x01\x02ar\xb2\x01 55ed759fcf94f85813e57b2ec8492f5c\xba\x01\x014\xea\x01@6fb7fdef8658fd03174ed551e82b71b21db8187fa0612c8eaf1b63aa687f1eae\x9a\x06\x014\xa2\x06\x014'
        pL = pL.replace(b"2023-12-24 04:21:34", str(nOw).encode())
        pL = pL.replace(b"15f5ba1de5234a2e73cc65b6f34ce4b299db1af616dd1dd8a6f31b147230e5b6", nAt.encode("UTF-8"))
        pL = pL.replace(b"4666ecda0003f1809655a7a8698573d0", nEiD.encode("UTF-8"))
        pL = pL.replace(b"7428b253defc164018c604a1ebbfebdf", sMd5.encode("UTF-8"))
        
        pHex = pL.hex()
        pEnC = eNcApI(pHex)
        pByTeS = bytes.fromhex(pEnC)
        
        dAtA = gEtLoGiNdAtA(jWt, pByTeS, rEg)
        return {
            "data": dAtA,
            "response": rEsP,
            "status_code": cOdE,
            "name": nAmE,
            "uid": uId,
            "password": pAsS
        }
    except Exception:
        return None

def uSeRlOgIn(uId, pAsS, aT, oId, rEsP, cOdE, nAmE, rEg):
    lAnG = GeTlAnG(rEg)
    lB = lAnG.encode("ascii")
    
    hEaDeRs = {
        "Accept-Encoding": "gzip",
        "Authorization": "Bearer",
        "Connection": "Keep-Alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Expect": "100-continue",
        "Host": "loginbp.ggpolarbear.com",
        "ReleaseVersion": "OB52",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)",
        "X-GA": "v1 1",
        "X-Unity-Version": "2018.4.11f1"
    }

    pL = b'\x1a\x132025-08-30 05:19:21"\tfree fire(\x01:\x081.114.13B2Android OS 9 / API-28 (PI/rel.cjw.20220518.114133)J\x08HandheldR\nATM MobilsZ\x04WIFI`\xb6\nh\xee\x05r\x03300z\x1fARMv7 VFPv3 NEON VMH | 2400 | 2\x80\x01\x9c\x0f\x8a\x01\x0fAdreno (TM) 640\x92\x01\rOpenGL ES 3.2\x9a\x01+Google|dfa4ab4b-9dc4-454e-8065-e70c733fa53f\xa2\x01\x0e105.235.139.91\xaa\x01\x02' + lB + b'\xb2\x01 1d8ec0240ede109973f3321b9354b44d\xba\x01\x014\xc2\x01\x08Handheld\xca\x01\x10Asus ASUS_I005DA\xea\x01@afcfbf13334be42036e4f742c80b956344bed760ac91b3aff9b607a610ab4390\xf0\x01\x01\xca\x02\nATM Mobils\xd2\x02\x04WIFI\xca\x03 7428b253defc164018c604a1ebbfebdf\xe0\x03\xa8\x81\x02\xe8\x03\xf6\xe5\x01\xf0\x03\xaf\x13\xf8\x03\x84\x07\x80\x04\xe7\xf0\x01\x88\x04\xa8\x81\x02\x90\x04\xe7\xf0\x01\x98\x04\xa8\x81\x02\xc8\x04\x01\xd2\x04=/data/app/com.dts.freefireth-PdeDnOilCSFn37p1AH_FLg==/lib/arm\xe0\x04\x01\xea\x04_2087f61c19f57f2af4e7feff0b24d9d9|/data/app/com.dts.freefireth-PdeDnOilCSFn37p1AH_FLg==/base.apk\xf0\x04\x03\xf8\x04\x01\x8a\x05\x0232\x9a\x05\n2019118692\xb2\x05\tOpenGLES2\xb8\x05\xff\x7f\xc0\x05\x04\xe0\x05\xf3F\xea\x05\x07android\xf2\x05pKqsHT5ZLWrYljNb5Vqh//yFRlaPHSO9NWSQsVvOmdhEEn7W+VHNUK+Q+fduA3ptNrGB0Ll0LRz3WW0jOwesLj6aiU7sZ40p8BfUE/FI/jzSTwRe2\xf8\x05\xfb\xe4\x06\x88\x06\x01\x90\x06\x01\x9a\x06\x014\xa2\x06\x014\xb2\x06"GQ@O\x00\x0e^\x00D\x06UA\x0ePM\r\x13hZ\x07T\x06\x0cm\\V\x0ejYV;\x0bU5'
    
    pL = pL.replace(b'afcfbf13334be42036e4f742c80b956344bed760ac91b3aff9b607a610ab4390', aT.encode())
    pL = pL.replace(b'1d8ec0240ede109973f3321b9354b44d', oId.encode())
    
    d = eNcApI(pL.hex())
    fP = bytes.fromhex(d)
    
    if rEg.lower() == "me":
        uRl = "https://loginbp.common.ggbluefox.com/MajorLogin"
    else:
        uRl = "https://loginbp.ggpolarbear.com/MajorLogin"
    
    rEs = requests.post(uRl, headers=hEaDeRs, data=fP, verify=False)
    
    if rEs.status_code == 200:
        if len(rEs.text) < 10:
            return False
        
        if lAnG.lower() not in ["ar", "en"]:
            jR = pArSeRoOm(rEs.content.hex())
            if jR is None:
                return False
            pD = json.loads(jR)
            tOkEn = pD['8']['data']
            
            if rEg.lower() == "cis":
                rEg = "RU"
            
            fIeLdS = {1: rEg}
            fByTeS = bytes.fromhex(eNcApI(cReAtEpRoTo(fIeLdS).hex()))
            cR = cHoOsErEgIoN(fByTeS, tOkEn)
            
            if cR == 200:
                return lOgInSeRvEr(uId, pAsS, aT, oId, rEsP, cOdE, nAmE, rEg)
        else:
            tOkEn = rEs.text[rEs.text.find("eyJhbGciOiJIUzI1NiIsInN2ciI6IjEiLCJ0eXAiOiJKV1QifQ"):-1]
        
        sDi = tOkEn.find(".", tOkEn.find(".") + 1)
        time.sleep(0.2)
        tOkEn = tOkEn[:sDi + 44]
        return gEtPaYlOaD(tOkEn, aT, 1, rEsP, cOdE, nAmE, uId, pAsS, rEg)
    return False

def lOgInSeRvEr(uId, pAsS, aT, oId, rEsP, cOdE, nAmE, rEg):
    lAnG = GeTlAnG(rEg)
    lB = lAnG.encode("ascii")
    
    hEaDeRs = {
        "Accept-Encoding": "gzip",
        "Authorization": "Bearer",
        "Connection": "Keep-Alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Expect": "100-continue",
        "Host": "loginbp.ggpolarbear.com",
        "ReleaseVersion": "OB52",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)",
        "X-GA": "v1 1",
        "X-Unity-Version": "2018.4.11f1"
    }

    pL = b'\x1a\x13\x32\x30\x32\x36\x2d\x30\x31\x2d\x31\x34\x20\x31\x35\x3a\x32\x36\x3a\x30\x39\x22\x09\x66\x72\x65\x65\x20\x66\x69\x72\x65\x3a\x07\x31\x2e\x31\x32\x30\x2e\x33\x42\x0a\x69\x4f\x53\x20\x31\x35\x2e\x38\x2e\x32\x4a\x08\x48\x61\x6e\x64\x68\x65\x6c\x64\x65\x64\x52\x0e\x4f\x72\x61\x6e\x67\x65\x20\x54\x75\x6e\x69\x73\x69\x61\x5a\x04\x57\x49\x46\x49\x60\xb6\x0a\x68\xee\x05\x72\x03\x33\x32\x36\x7a\x0d\x61\x72\x6d\x36\x34\x20\x7c\x20\x30\x20\x7c\x20\x32\x80\x01\xd0\x0f\x8a\x01\x0d\x41\x70\x70\x6c\x65\x20\x41\x31\x30\x20\x47\x50\x55\x92\x01\x05\x4d\x65\x74\x61\x6c\x9a\x01\x2a\x41\x70\x70\x6c\x65\x7c\x34\x37\x36\x33\x42\x30\x36\x46\x2d\x31\x41\x46\x42\x2d\x34\x39\x31\x46\x2d\x39\x43\x31\x39\x2d\x37\x46\x43\x46\x38\x42\x38\x30\x39\x32\x33\x30\xa2\x01\x0e\x31\x30\x32\x2e\x31\x35\x32\x2e\x36\x33\x2e\x31\x33\x38\xaa\x01\x05\x67\x70\x74\x2d\x62\x72\xb2\x01\x20\x30\x35\x63\x32\x64\x30\x65\x38\x62\x32\x30\x36\x62\x34\x64\x37\x65\x39\x62\x30\x32\x38\x62\x38\x34\x32\x62\x61\x32\x63\x61\x32\xba\x01\x01\x34\xc2\x01\x08\x48\x61\x6e\x64\x68\x65\x6c\x64\x65\x64\xca\x01\x09\x69\x50\x68\x6f\x6e\x65\x39\x2c\x33\xea\x01\x40\x33\x32\x31\x62\x66\x36\x65\x31\x66\x64\x36\x63\x65\x37\x62\x32\x32\x64\x34\x39\x64\x36\x35\x35\x38\x63\x31\x30\x63\x65\x31\x35\x38\x30\x30\x62\x66\x62\x33\x35\x39\x64\x65\x37\x36\x63\x64\x30\x34\x32\x65\x65\x62\x66\x34\x32\x31\x39\x64\x63\x34\x61\x62\x65\xf0\x01\x01\xf0\x03\xa1\xee\x01\xf8\x03\xbd\x1b\xb0\x04\x02\xc8\x04\x02\xe0\x04\x01\xea\x04\x09\x49\x4f\x53\x44\x65\x76\x69\x63\x65\xf0\x04\x03\xf8\x04\x01\x9a\x05\x07\x31\x2e\x31\x32\x30\x2e\x31\xa8\x05\x03\xb2\x05\x05\x54\x4d\x65\x74\x61\x6c\xb8\x05\xff\x7f\xc0\x05\x04\xe0\x05\xca\xc8\x02\xea\x05\x03\x69\x6f\x73\xf2\x05\x48\x4b\x71\x73\x48\x54\x38\x43\x6a\x38\x69\x6d\x33\x32\x57\x70\x5a\x44\x64\x59\x2f\x6e\x51\x31\x58\x77\x43\x4c\x36\x55\x69\x2f\x32\x37\x48\x6e\x79\x6b\x32\x78\x34\x32\x69\x41\x72\x68\x7a\x64\x61\x30\x75\x4f\x44\x56\x64\x74\x6c\x51\x36\x46\x45\x30\x54\x2f\x52\x49\x7a\x6e\x6c\x70\x41\x3d\x3d\x90\x06\x01\x9a\x06\x01\x34\xa2\x06\x01\x34\xb2\x06\x0e\x60\x00\x17\x12\x72\x13\x59\x58\x21\x54\x5f\x12\x0d\x10\x09\x09\x09\x09\x09\x09\x09\x09\x09'
    
    pL = pL.replace(b'afcfbf13334be42036e4f742c80b956344bed760ac91b3aff9b607a610ab4390', aT.encode())
    pL = pL.replace(b'1d8ec0240ede109973f3321b9354b44d', oId.encode())
    
    d = eNcApI(pL.hex())
    fP = bytes.fromhex(d)
    
    if rEg.lower() == "me":
        uRl = "https://loginbp.common.ggbluefox.com/MajorLogin"
    else:
        uRl = "https://loginbp.ggpolarbear.com/MajorLogin"
    
    rEs = requests.post(uRl, headers=hEaDeRs, data=fP, verify=False)
    
    if rEs.status_code == 200:
        if len(rEs.text) < 10:
            return False
        
        jR = pArSeRoOm(rEs.content.hex())
        if jR is None:
            return False
        pD = json.loads(jR)
        tOkEn = pD['8']['data']
        
        sDi = tOkEn.find(".", tOkEn.find(".") + 1)
        time.sleep(0.2)
        tOkEn = tOkEn[:sDi + 44]
        return gEtPaYlOaD(tOkEn, aT, 1, rEsP, cOdE, nAmE, uId, pAsS, rEg)
    return False

def cReAtEaCc(rEg, name_prefix):
    pAsS = gEnPaSsWoRd()
    dAtA = f"password={pAsS}&client_type=2&source=2&app_id=100067"
    mSg = dAtA.encode('utf-8')
    sIg = hmac.new(MaIn_KeY, mSg, hashlib.sha256).hexdigest()

    uRl = "https://100067.connect.garena.com/oauth/guest/register"
    hEaDeRs = {
        "User-Agent": "GarenaMSDK/4.0.19P8(ASUS_Z01QD ;Android 12;en;US;)",
        "Authorization": "Signature " + sIg,
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip",
        "Connection": "Keep-Alive"
    }

    rEsPoNsE = requests.post(uRl, headers=hEaDeRs, data=dAtA)
    try:
        uId = rEsPoNsE.json()['uid']
        return gEtToKeN(uId, pAsS, rEg, name_prefix)
    except:
        return cReAtEaCc(rEg, name_prefix)

def gEtToKeN(uId, pAsS, rEg, name_prefix):
    uRl = "https://100067.connect.garena.com/oauth/guest/token/grant"
    hEaDeRs = {
        "Accept-Encoding": "gzip",
        "Connection": "Keep-Alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "100067.connect.garena.com",
        "User-Agent": "GarenaMSDK/4.0.19P8(ASUS_Z01QD ;Android 12;en;US;)",
    }

    bOdY = {
        "uid": uId,
        "password": pAsS,
        "response_type": "token",
        "client_type": "2",
        "client_secret": MaIn_KeY,
        "client_id": "100067"
    }

    rEsPoNsE = requests.post(uRl, headers=hEaDeRs, data=bOdY)
    oPeNiD = rEsPoNsE.json()['open_id']
    aCcEsStOkEn = rEsPoNsE.json()["access_token"]
    rEfReShToKeN = rEsPoNsE.json()['refresh_token']
    
    rEs = eNcOdEsTr(oPeNiD)
    fIeLd = tOuNiCoDeEsC(rEs['f14'])
    fIeLd = codecs.decode(fIeLd, 'unicode_escape').encode('latin1')
    return rEgMaJoR(aCcEsStOkEn, oPeNiD, fIeLd, uId, pAsS, rEg, name_prefix)

def rEgMaJoR(aT, oId, f, uId, pAsS, rEg, name_prefix):
    uRl = "https://loginbp.ggpolarbear.com/MajorRegister"
    nAmE = gEnNaMe(name_prefix)

    hEaDeRs = {
        "Accept-Encoding": "gzip",
        "Authorization": "Bearer",
        "Connection": "Keep-Alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Expect": "100-continue",
        "Host": "loginbp.ggpolarbear.com",
        "ReleaseVersion": "OB52",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)",
        "X-GA": "v1 1",
        "X-Unity-Version": "2018.4."
    }

    pAyLoAd = {
        1: nAmE,
        2: aT,
        3: oId,
        5: 102000007,
        6: 4,
        7: 1,
        13: 1,
        14: f,
        15: "en",
        16: 1,
        17: 1
    }

    pHex = cReAtEpRoTo(pAyLoAd).hex()
    pEnC = eNcAeS(pHex).hex()
    bOdY = bytes.fromhex(pEnC)

    rEs = requests.post(uRl, headers=hEaDeRs, data=bOdY, verify=False)
    return uSeRlOgIn(uId, pAsS, aT, oId, rEs.content.hex(), rEs.status_code, nAmE, rEg)

def generate_accounts(region, name_prefix, count, max_allowed=5):
    region = region.upper()
    if region not in ReGiOnMaP:
        raise ValueError("Invalid region")
    if count > max_allowed:
        raise ValueError(f"Maximum allowed accounts is {max_allowed}")
    
    accounts = []
    for i in range(count):
        try:
            result = cReAtEaCc(region, name_prefix)
            if result and result.get('status_code') == 200:
                accounts.append({
                    "name": result.get('name'),
                    "uid": result.get('uid'),
                    "password": result.get('password')
                })
            else:
                accounts.append({"error": f"Failed to generate account {i+1}"})
        except Exception as e:
            accounts.append({"error": f"Account {i+1} error: {str(e)}"})
    return accounts

# ---- واجهة Flask API مع التحقق من المفتاح ----
app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    # التحقق من مفتاح API
    api_key = request.headers.get('X-API-Key')
    if not api_key or api_key != API_KEY:
        return jsonify({"error": "Unauthorized: Invalid or missing API key"}), 401

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    
    count = data.get('count')
    region = data.get('region')
    name_prefix = data.get('name_prefix')
    
    if not all([count, region, name_prefix]):
        return jsonify({"error": "Missing parameters: count, region, name_prefix"}), 400
    
    try:
        count = int(count)
    except:
        return jsonify({"error": "count must be integer"}), 400
    
    MAX_ACCOUNTS = 5  # يمكن تعديله حسب رغبتك
    try:
        accounts = generate_accounts(region, name_prefix, count, MAX_ACCOUNTS)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    return jsonify({"accounts": accounts})

# للاختبار المحلي
if __name__ == "__main__":
    app.run(debug=True)