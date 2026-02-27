import os
from flask import Flask, request, jsonify
from core.sequencer import ChimeraEngineV5
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

MASTER_KEY = os.environ.get('CHIMERA_MASTER_KEY', 'DEFAULT_INSECURE_KEY')

if MASTER_KEY == 'DEFAULT_INSECURE_KEY':
    print("WARNING: Using insecure default master key")

engine = ChimeraEngineV5(MASTER_KEY)


@app.route('/v1/sequencer/encode', methods=['POST'])
def api_encode():
    if not request.json or 'input_stream' not in request.json:
        return jsonify({"status": "error", "message": "Missing input_stream"}), 400

    raw_input = request.json['input_stream']

    if not isinstance(raw_input, str):
        return jsonify({"status": "error", "message": "input_stream must be string"}), 400

    result = engine.process_encode(raw_input)

    return jsonify({
        "status": "integrated",
        "genome_packet": {
            "sequence": result['sequence'],
            "metadata": {
                "locus": result['locus'],
                "protocol": engine.PROTOCOL
            }
        }
    })


@app.route('/v1/sequencer/decode', methods=['POST'])
def api_decode():
    if not request.json or 'genome_packet' not in request.json:
        return jsonify({"status": "error", "message": "Missing genome_packet"}), 400

    try:
        packet = request.json['genome_packet']
        sequence = packet['sequence']
        metadata = packet['metadata']

        # Validate protocol
        if metadata.get('protocol') != engine.PROTOCOL:
            return jsonify({
                "status": "rejection",
                "message": "Protocol mismatch"
            }), 403

        locus = metadata['locus']

        output = engine.process_decode(sequence, locus)

        return jsonify({
            "status": "resolved",
            "output_stream": output
        })

    except Exception:
        return jsonify({
            "status": "rejection",
            "message": "Invalid Key or Corrupted DNA"
        }), 403


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)