import argparse                                         # parse CLI arguments (initial command)
import hashlib                                          # hashing algorythms  (blacklist check)
import math                                             # math functions 
import os                                               # OS utils 
import re                                               # regex text seach (string detection)
from typing import Dict, List, Tuple #type hints


PRINTABLE_RE = re.compile(rb'[\x20-\x7E]{4,}')

# Core

def compute_hash(path: str) -> Dict[str, str]:
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()
    with open(path, "rb" ) as f:                        # opens path and reads binary (rb) as file
        for chunk in iter(lambda: f.read(8192), b""):   # read it in 8kb chunks
            md5.update(chunk)
            sha1.update(chunk)
            sha256.update(chunk)
                                                        # this updates the systems with the chunks
        return {                                        # return dictionary with all hashes in hex form
            "md5": md5.hexdigest(),
            "sha1": sha1.hexdigest(),
            "sha256": sha256.hexdigest(),
        }

def file_size(path: str) -> int:                                       
    return os.path.getsize(path)

#      entropy -= explanation and use in this project =- 

#      entropry level goes from 0-8 
#      this calculates how random the data is 
#      by converting hex in numbers, it can utilise the Shannon entropy formula [(-p * log2(p)] to determine how random it is
#      the more random, the more encrypted the file is
#      the less random data is, security is low
#      some malware has encrypted data hidden, resulting in high entropry (making the file suspicious)
#      a text file with just "AAAAAAAA" -- entropy ≈ 0 (completely predictable).
#      a novel in english -- entropy ≈ 4–5 (structured, but some randomness).
#      an encrypted file or compressed ZIP -- entropy ≈ 8 (looks totally random).

def entropy(path:str) -> float:   
    with open(path, "rb") as f:
        data = f.read()
    if not data:
        return 0.0
    freq = {}
    for b in data:
        freq[b] = freq.get(b,0) + 1                 # increment byte frequency count
    ent = 0.0
    length = len(data)                              # total
    for count in freq.values():                     # for each unique byte frequency
        p = count / length                          # calculates the probabiliy of the byte occuring
        ent -= p * math.log2(p)
    return ent                                      # returns entropry from 0-8

def extract_strings(path: str, min_len: int = 4) -> List[str]:
    results = []                                                    # list to hold extracted string
    with open(path, "rb") as f:
        data = f.read()
    for m in PRINTABLE_RE.finditer(data) :                          # find printable ASCII substrings
        try:
            s = m.group().decode("latin-1", errors="replace")       # decodes bytes to string using latin-1, safe for byte values
        except Exception:
            continue
        if len(s) >= min_len:
            results.append(s)                                       # adds without overwriting, s into results (s being the decoded bytes)
    return results


def check_magic(path: str) -> List[str]:
    signatures = {
        b"MZ": "PE/Windows executable",                           # windows EXE
        b"\x7fELF": "ELF executable",                             # linux binary
        b"%PDF": "PDF document",                                  # PDF
        b"\x50\x4B\x03\x04": "ZIP archive (or docx/xlsx)",        # ZIP and office documents
        b"\x89PNG": "PNG image",                                  # PNG
        b"GIF87a": "GIF image",                                   # GIF (old)
        b"GIF89a": "GIF image",                                   # GIF (new)
    }
    found = []                                                    # list of found signatures
    with open(path, "rb") as f:
        header = f.read(16)                                       # reads first 16 bytes of the file
    for sig, desc in signatures.items():
        if header.startswith(sig):                                # if it matches adds the description to results
            found.append(desc)                                    # then adds over found and retunrs it
    return found


# score

def score_findings(ent: float, magic: List[str], size: int) -> Dict:
    score = 0
    reasons = []
    if ent > 7.5:
        score += 20
        reasons.append(f"high entropy ({ent:.2f}) possible")
    if magic:
        reasons.append(f"file type signatures: {', '.join(magic)}")
    if score > 100:  
        score = 100
    return {"score": score, "reasons": reasons}


def main():
    ap = argparse.ArgumentParser(description="Simple local file scanner (CLI).")
    ap.add_argument("file", help="Path to file to scan")
    ap.add_argument("--min-strings", help="Minimum printable string length", type=int, default=4)
    args = ap.parse_args()  

    path = args.file
    if not os.path.isfile(path):  
        print(f"[ERROR] File not found: {path}")
        return

    print(f"[+] Scanning: {path}")
    hashes = compute_hash(path)            
    size = file_size(path)   
    ent = entropy(path)           
    magic = check_magic(path)     
    strings = extract_strings(path, min_len=args.min_strings)  #
    result = score_findings(ent, magic, size) 

    # Console summary
    print(f"  - Size: {size} bytes")
    print(f"  - Entropy: {ent:.3f}")
    print(f"  - Magic: {', '.join(magic) if magic else 'Unknown'}")
    print(f"  - Hashes: MD5={hashes['md5']}, SHA1={hashes['sha1']}, SHA256={hashes['sha256']}")
    print(f"  - Score: {result['score']} / 100")
    if result["reasons"]:
        # print("  - Reasons:")
        for r in result["reasons"]:
            print(f"    * {r}")
   
if __name__ == "__main__":
    main()  
