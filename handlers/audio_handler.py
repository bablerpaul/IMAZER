import hashlib
import json
import os
import binascii
import math
import sys
from datetime import datetime
from pymediainfo import MediaInfo

def extract_audio_metadata(file_path):
    if not os.path.isfile(file_path):
        return {"error": "File not found"}

    metadata = {
        "file_info": {},
        "technical_metadata": {},
        "hashes": {},
        "embedded_metadata": [],
        "audio_tracks": [],
        "chapters": [],
        "signatures": {},
        "forensic_analysis": {
            "anomalies": [],
            "header_analysis": {},
            "trailer_analysis": {},
            "steganography_indicators": {}
        }
    }

    try:
        stat = os.stat(file_path)
        metadata["file_info"] = {
            "file_path": os.path.abspath(file_path),
            "file_name": os.path.basename(file_path),
            "file_size": stat.st_size,
            "inode": stat.st_ino,
            "device": stat.st_dev,
            "hard_links": stat.st_nlink,
            "uid": stat.st_uid,
            "gid": stat.st_gid,
            "created_utc": datetime.utcfromtimestamp(stat.st_ctime).isoformat() + "Z",
            "modified_utc": datetime.utcfromtimestamp(stat.st_mtime).isoformat() + "Z",
            "accessed_utc": datetime.utcfromtimestamp(stat.st_atime).isoformat() + "Z",
            "file_extension": os.path.splitext(file_path)[1].lower(),
            "file_permissions": oct(stat.st_mode)[-4:],
            "flags": get_file_flags(file_path)
        }

        metadata["hashes"] = calculate_forensic_hashes(file_path)

        media_info = MediaInfo.parse(file_path)

        for track in media_info.tracks:
            track_data = {}
            raw_values = {}
            for attr in dir(track):
                if not attr.startswith("__") and not callable(getattr(track, attr)):
                    value = getattr(track, attr)
                    if value not in [None, ""]:
                        if isinstance(value, bytes):
                            hex_value = binascii.hexlify(value).decode('utf-8')
                            raw_values[attr + "_hex"] = hex_value
                            value = value.decode('utf-8', errors='replace')
                        track_data[attr] = value

            if raw_values:
                track_data["raw_hex_values"] = raw_values

            if track.track_type == "General":
                metadata["technical_metadata"] = track_data
            elif track.track_type == "Audio":
                metadata["audio_tracks"].append(track_data)
            elif track.track_type == "Menu" and "chapters" in track_data.get("menu_type", "").lower():
                metadata["chapters"].append(track_data)
            elif track.track_type == "Other":
                metadata["embedded_metadata"].append(track_data)

        metadata["signatures"] = file_signature_analysis(file_path)
        metadata["forensic_analysis"].update({
            "header_analysis": analyze_file_header(file_path),
            "trailer_analysis": analyze_file_trailer(file_path),
            "steganography_indicators": detect_steganography_indicators(file_path),
            "anomalies": detect_forensic_anomalies(metadata, file_path)
        })

        return metadata

    except Exception as e:
        return {"error": f"Forensic analysis failed: {str(e)}"}

def calculate_forensic_hashes(file_path):
    hashers = {
        "md5": hashlib.md5(),
        "sha1": hashlib.sha1(),
        "sha256": hashlib.sha256(),
        "sha512": hashlib.sha512(),
        "sha3_256": hashlib.sha3_256(),
        "blake2b": hashlib.blake2b()
    }

    head_hashers = {f"head_1k_{algo}": hashlib.new(algo) for algo in ['md5', 'sha1', 'sha256']}
    tail_hashers = {f"tail_1k_{algo}": hashlib.new(algo) for algo in ['md5', 'sha1', 'sha256']}

    file_size = os.path.getsize(file_path)
    with open(file_path, "rb") as f:
        head_data = f.read(1024)
        for h in head_hashers.values():
            h.update(head_data)

        f.seek(0)
        while chunk := f.read(8192):
            for h in hashers.values():
                h.update(chunk)

        if file_size > 1024:
            f.seek(-1024, os.SEEK_END)
            tail_data = f.read(1024)
            for h in tail_hashers.values():
                h.update(tail_data)

    return {
        **{algo: h.hexdigest() for algo, h in hashers.items()},
        **{algo: h.hexdigest() for algo, h in head_hashers.items()},
        **{algo: h.hexdigest() for algo, h in tail_hashers.items()}
    }

def file_signature_analysis(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    with open(file_path, "rb") as f:
        header = f.read(32)
        trailer = b''
        if os.path.getsize(file_path) > 1024:
            f.seek(-32, os.SEEK_END)
            trailer = f.read(32)

    return {
        "file_header": header.hex(),
        "file_trailer": trailer.hex(),
        "magic_number": header[:4].hex().upper(),
        "extension_mismatch": check_extension_mismatch(header, ext),
        "known_signatures": identify_known_signatures(header)
    }

def analyze_file_header(file_path):
    with open(file_path, "rb") as f:
        header = f.read(1024)

    return {
        "header_size": len(header),
        "entropy": calculate_entropy(header),
        "null_bytes": header.count(b'\x00'),
        "printable_chars": sum(1 for byte in header if 32 <= byte <= 126),
        "control_chars": sum(1 for byte in header if byte < 32 or byte == 127),
        "signature_matches": identify_known_signatures(header)
    }

def analyze_file_trailer(file_path):
    file_size = os.path.getsize(file_path)
    if file_size < 1024:
        return {"error": "File too small for trailer analysis"}

    with open(file_path, "rb") as f:
        f.seek(-1024, os.SEEK_END)
        trailer = f.read(1024)

    return {
        "trailer_size": len(trailer),
        "entropy": calculate_entropy(trailer),
        "null_bytes": trailer.count(b'\x00'),
        "printable_chars": sum(1 for byte in trailer if 32 <= byte <= 126),
        "control_chars": sum(1 for byte in trailer if byte < 32 or byte == 127),
        "signature_matches": identify_known_signatures(trailer),
        "embedded_signatures": check_embedded_signatures(trailer)
    }

def detect_steganography_indicators(file_path):
    indicators = {}
    file_size = os.path.getsize(file_path)

    with open(file_path, "rb") as f:
        if file_size > 100:
            f.seek(-8, os.SEEK_END)
            last_bytes = f.read(8).hex().upper()
            indicators["eof_markers"] = {
                "value": last_bytes,
                "is_standard_eof": last_bytes in ["FFD9", "00000000", "49454E44AE426082"]
            }

        f.seek(0)
        chunk = f.read(8192) if file_size > 8192 else f.read()
        indicators["entropy"] = calculate_entropy(chunk)

        f.seek(0)
        data = f.read()
        indicators["lzb_signature"] = "LZB" in data[:100].decode('ascii', errors='ignore')
        indicators["invisible_secrets"] = b'INVS' in data[:100]

    return indicators

def detect_forensic_anomalies(metadata, file_path):
    anomalies = []

    reported_size = metadata["technical_metadata"].get("file_size")
    actual_size = os.path.getsize(file_path)
    if reported_size and reported_size != actual_size:
        anomalies.append(f"Size mismatch: Metadata reports {reported_size} bytes, actual is {actual_size} bytes")

    created = datetime.fromisoformat(metadata["file_info"]["created_utc"].rstrip('Z'))
    modified = datetime.fromisoformat(metadata["file_info"]["modified_utc"].rstrip('Z'))
    if created > modified:
        anomalies.append("Creation time is after modification time")

    header_hash = metadata["hashes"].get("head_1k_sha256")
    trailer_hash = metadata["hashes"].get("tail_1k_sha256")
    if header_hash and trailer_hash and header_hash == trailer_hash:
        anomalies.append("Header and trailer hashes match - possible uniform data pattern")

    if metadata["signatures"].get("extension_mismatch"):
        anomalies.append("File extension does not match file signature")

    entropy = metadata["forensic_analysis"]["header_analysis"].get("entropy", 0)
    if entropy > 7.9:
        anomalies.append(f"High header entropy ({entropy:.2f}), possible encrypted content")

    return anomalies

def calculate_entropy(data):
    if not data:
        return 0.0
    entropy = 0.0
    for x in range(256):
        p_x = float(data.count(x)) / len(data)
        if p_x > 0:
            entropy += - p_x * math.log2(p_x)
    return entropy

def identify_known_signatures(data):
    signatures = {
        "ID3": [(b'ID3', "ID3v2 tag")],
        "FLAC": [(b'fLaC', "FLAC header")],
        "WAV": [(b'RIFF', "WAV container")],
        "MP3": [(b'\xFF\xFB', "MP3 frame"), (b'\xFF\xF3', "MP3 frame")],
        "AAC": [(b'\xFF\xF1', "AAC ADTS"), (b'\xFF\xF9', "AAC ADTS")],
        "Ogg": [(b'OggS', "Ogg container")],
        "EXE": [(b'MZ', "DOS executable")],
        "ZIP": [(b'PK\x03\x04', "ZIP archive")],
        "PNG": [(b'\x89PNG', "PNG image")]
    }

    matches = {}
    for sig_type, patterns in signatures.items():
        for pattern, description in patterns:
            if data.startswith(pattern):
                matches[sig_type] = {
                    "description": description,
                    "offset": 0,
                    "hex": binascii.hexlify(pattern).decode('utf-8').upper()
                }
                break
    return matches

def check_extension_mismatch(header, ext):
    signatures = {
        ".mp3": [b'\xFF\xFB', b'\xFF\xF3', b'\xFF\xF2', b'\xFF\xF1', b'ID3'],
        ".wav": [b'RIFF'],
        ".flac": [b'fLaC'],
        ".aac": [b'\xFF\xF1', b'\xFF\xF9'],
        ".ogg": [b'OggS'],
        ".m4a": [b'ftypM4A', b'ftypmp42', b'ftypisom'],
        ".aiff": [b'FORM'],
        ".wma": [b'\x30\x26\xB2\x75\x8E\x66\xCF\x11\xA6\xD9\x00\xAA\x00\x62\xCE\x6C']
    }

    for sig_ext, patterns in signatures.items():
        if any(header.startswith(p) for p in patterns):
            return sig_ext != ext
    return None

def get_file_flags(file_path):
    try:
        if os.name == 'posix':
            import stat
            st = os.stat(file_path)
            flags = []
            if hasattr(st, 'st_flags'):
                if st.st_flags & stat.UF_IMMUTABLE:
                    flags.append("IMMUTABLE")
                if st.st_flags & stat.UF_APPEND:
                    flags.append("APPEND_ONLY")
                if st.st_flags & stat.UF_HIDDEN:
                    flags.append("HIDDEN")
            return flags
        elif os.name == 'nt':
            import ctypes
            from ctypes import wintypes

            FILE_ATTRIBUTE_HIDDEN = 0x2
            FILE_ATTRIBUTE_SYSTEM = 0x4

            GetFileAttributes = ctypes.windll.kernel32.GetFileAttributesW
            GetFileAttributes.argtypes = [wintypes.LPCWSTR]
            GetFileAttributes.restype = wintypes.DWORD

            attrs = GetFileAttributes(file_path)
            flags = []
            if attrs & FILE_ATTRIBUTE_HIDDEN:
                flags.append("HIDDEN")
            if attrs & FILE_ATTRIBUTE_SYSTEM:
                flags.append("SYSTEM")
            return flags
    except:
        pass
    return ["UNKNOWN"]

def check_embedded_signatures(data):
    signatures = {
        "ZIP": b'PK\x03\x04',
        "RAR": b'Rar!\x1a\x07\x00',
        "PDF": b'%PDF-',
        "JPG": b'\xFF\xD8\xFF',
        "PNG": b'\x89PNG',
        "GZIP": b'\x1F\x8B'
    }

    found = []
    for name, pattern in signatures.items():
        if pattern in data:
            offset = data.index(pattern)
            found.append({
                "signature": name,
                "offset": offset,
                "hex": binascii.hexlify(pattern).decode('utf-8').upper()
            })
    return found

audio_handler = extract_audio_metadata

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python audio_forensics.py <audio_file>")
        sys.exit(1)

    result = extract_audio_metadata(sys.argv[1])
    print(json.dumps(result, indent=2, ensure_ascii=False))
