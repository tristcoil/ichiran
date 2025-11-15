#!/usr/bin/env python3
"""
Flask API wrapper for ichiran-cli.
Exposes /i-api/v1 endpoint for Japanese text analysis.
"""

import subprocess
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/i-api/v1', methods=['GET', 'POST'])
def analyze():
    """
    Analyze Japanese text using ichiran-cli.
    
    GET: ?text=<japanese_text>&format=<format>
    POST: JSON body with "text" and optional "format" field
    
    Format options:
    - "simple" (default): Human-readable text output with -i flag
    - "full": Structured JSON with detailed linguistic data using -f flag
    
    Returns JSON with romaji and analysis.
    """
    # Extract text and format from request
    if request.method == 'GET':
        text = request.args.get('text', '')
        output_format = request.args.get('format', 'simple')
    else:  # POST
        data = request.get_json(silent=True) or {}
        text = data.get('text', '')
        output_format = data.get('format', 'simple')
    
    if not text:
        return jsonify({
            'error': 'No text provided',
            'usage': 'GET: ?text=<text>&format=<simple|full> or POST: {"text": "<text>", "format": "<simple|full>"}'
        }), 400
    
    # Validate format parameter
    if output_format not in ['simple', 'full']:
        return jsonify({
            'error': 'Invalid format',
            'usage': 'Format must be "simple" or "full"'
        }), 400
    
    try:
        # Choose ichiran-cli flag based on format
        flag = '-i' if output_format == 'simple' else '-f'
        
        # Call ichiran-cli with the text
        result = subprocess.run(
            ['ichiran-cli', flag, text],
            capture_output=True,
            text=True,
            timeout=30,
            check=True
        )
        
        if output_format == 'full':
            # Parse JSON output from -f flag
            try:
                structured_data = json.loads(result.stdout)
                return jsonify({
                    'text': text,
                    'format': 'full',
                    'data': structured_data
                }), 200
            except json.JSONDecodeError:
                return jsonify({
                    'error': 'Failed to parse ichiran-cli JSON output',
                    'raw_output': result.stdout
                }), 500
        else:
            # Parse text output from -i flag
            output_lines = result.stdout.strip().split('\n')
            romaji = output_lines[0] if output_lines else ''
            analysis = '\n'.join(output_lines[1:]) if len(output_lines) > 1 else ''
            
            return jsonify({
                'text': text,
                'format': 'simple',
                'romaji': romaji,
                'analysis': analysis,
                'full_output': result.stdout
            }), 200
        
    except subprocess.TimeoutExpired:
        return jsonify({
            'error': 'Analysis timed out (30s limit)'
        }), 504
    
    except subprocess.CalledProcessError as e:
        return jsonify({
            'error': 'ichiran-cli failed',
            'stderr': e.stderr,
            'returncode': e.returncode
        }), 500
    
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500


@app.route('/i-api/v1/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok', 'service': 'ichiran-api'}), 200


if __name__ == '__main__':
    # Run on all interfaces, port 5900
    app.run(host='0.0.0.0', port=5900, debug=False)
