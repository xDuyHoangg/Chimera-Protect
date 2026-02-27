import os
import hashlib
import hmac
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

class ChimeraEngineV5:
    """
    Bio-Digital Transformation Core - Đạt chuẩn NIST với lõi AES-256-GCM 
    kết hợp lớp phủ DNA Sequence.
    """
    def __init__(self):
        self._MAP = {0: 'A', 1: 'T', 2: 'G', 3: 'C'}
        self._REV_MAP = {v: k for k, v in self._MAP.items()}
        
        # Lấy khóa từ môi trường
        env_key = os.environ.get('CHIMERA_MASTER_KEY')
        
        if not env_key:
            # Nếu không có, set một giá trị mặc định để TEST (Không dùng cho production!)
            self._MASTER_KEY = "TEMPORARY-INSECURE-KEY-DO-NOT-USE-IN-PROD"
            print("\n" + "!"*60)
            print("CẢNH BÁO BẢO MẬT: CHIMERA_MASTER_KEY chưa được thiết lập.")
            print("Đang sử dụng khóa tạm thời. Hệ thống của bạn ĐANG KHÔNG AN TOÀN.")
            print("!"*60 + "\n")
        else:
            self._MASTER_KEY = env_key

    def _derive_key(self, salt):
        """Sử dụng PBKDF2 để tạo khóa 256-bit từ Master Key (Chuẩn NIST)"""
        return PBKDF2(self._MASTER_KEY, salt, dkLen=32, count=100000)

    def _bytes_to_dna(self, data):
        """Chuyển đổi byte sang chuỗi DNA (Obfuscation layer)"""
        dna = ""
        for b in data:
            for j in range(4):
                dna += self._MAP[(b >> (j * 2)) & 0b11]
        return dna

    def _dna_to_bytes(self, dna):
        """Chuyển đổi chuỗi DNA ngược lại byte"""
        data = bytearray()
        for i in range(0, len(dna), 4):
            val = 0
            for j in range(4):
                val |= (self._REV_MAP[dna[i + j]] << (j * 2))
            data.append(val)
        return bytes(data)

    def process_encode(self, raw_str):
        # 1. Tạo Salt ngẫu nhiên (16 bytes)
        salt = os.urandom(16)
        key = self._derive_key(salt)
        
        # 2. Mã hóa AES-256-GCM
        cipher = AES.new(key, AES.MODE_GCM)
        ciphertext, auth_tag = cipher.encrypt_and_digest(raw_str.encode('utf-8'))
        
        # 3. Đóng gói dữ liệu (Nonce + AuthTag + Ciphertext)
        # Đây là cấu trúc chuẩn để đảm bảo tính toàn vẹn
        encrypted_blob = cipher.nonce + auth_tag + ciphertext
        
        # 4. Chuyển sang DNA stream để "ngụy trang"
        dna_sequence = self._bytes_to_dna(encrypted_blob)
        
        return {
            "sequence": dna_sequence,
            "locus": salt.hex(),
            "ts": datetime.utcnow().isoformat()
        }

    def process_decode(self, dna_sequence, salt_hex):
        try:
            salt = bytes.fromhex(salt_hex)
            encrypted_blob = self._dna_to_bytes(dna_sequence)
            
            # Tách gói dữ liệu (GCM tiêu chuẩn: Nonce 16, Tag 16)
            nonce = encrypted_blob[:16]
            auth_tag = encrypted_blob[16:32]
            ciphertext = encrypted_blob[32:]
            
            # Giải mã
            key = self._derive_key(salt)
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            decrypted_data = cipher.decrypt_and_verify(ciphertext, auth_tag)
            
            return decrypted_data.decode('utf-8')
        except Exception as e:
            # Không trả về lỗi chi tiết để tránh tấn công Side-channel
            raise PermissionError("Decryption failed: Invalid key or corrupted data.")

engine = ChimeraEngineV5()

# --- API Endpoints ---

@app.route('/v1/sequencer/encode', methods=['POST'])
def api_encode():
    data = request.json.get('input_stream')
    if not data: return jsonify({"error": "No data"}), 400
    
    res = engine.process_encode(data)
    return jsonify({
        "status": "integrated",
        "genome_packet": {
            "sequence": res['sequence'],
            "metadata": {"locus": res['locus'], "protocol": "CHIMERA-AES-GCM-V5"}
        }
    })

@app.route('/v1/sequencer/decode', methods=['POST'])
def api_decode():
    try:
        packet = request.json['genome_packet']
        output = engine.process_decode(packet['sequence'], packet['metadata']['locus'])
        return jsonify({"status": "resolved", "output_stream": output})
    except Exception:
        return jsonify({"status": "rejection", "code": 403}), 403

if __name__ == '__main__':
    # Trong thực tế phải chạy bằng Gunicorn/Nginx, không dùng app.run() trực tiếp
    app.run(host='0.0.0.0', port=8080)