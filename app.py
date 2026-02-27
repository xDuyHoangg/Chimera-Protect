import os
from flask import Flask, request, jsonify
from core.sequencer import ChimeraEngineV5
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Cấu hình bảo mật từ ENV
MASTER_KEY = os.environ.get('CHIMERA_MASTER_KEY', 'DEFAULT_INSECURE_KEY')

engine = ChimeraEngineV5(MASTER_KEY)

@app.route('/v1/sequencer/encode', methods=['POST'])
def api_encode():
    data = request.json.get('input_stream')
    res = engine.process_encode(data)
    return jsonify({"status": "integrated", "genome_packet": {"sequence": res['sequence'], "metadata": {"locus": res['locus']}}})

@app.route('/v1/sequencer/decode', methods=['POST'])
def api_decode():
    try:
        packet = request.json['genome_packet']
        output = engine.process_decode(packet['sequence'], packet['metadata']['locus'])
        return jsonify({"status": "resolved", "output_stream": output})
    except Exception:
        return jsonify({"status": "rejection", "message": "Invalid Key or Corrupted DNA"}), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)