from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import json

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    'host': 'supabase-db',
    'port': 5435,
    'database': 'postgres',
    'user': 'postgres',
    'password': 'atenza515351'
}

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/api/catalog', methods=['GET'])
def get_catalog():
    helena_account_id = request.args.get('id')
    
    if not helena_account_id:
        return jsonify({'error': 'id parameter is required'}), 400
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        cur.execute("SELECT get_account_data(%s)", (helena_account_id,))
        result = cur.fetchone()[0]
        
        cur.close()
        conn.close()
        
        return jsonify(result)
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3002, debug=False)
