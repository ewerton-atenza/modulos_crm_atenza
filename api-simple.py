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

@app.route('/api/categories', methods=['POST'])
def create_category():
    data = request.json
    account_id = data.get('account_id')
    name = data.get('name')
    description = data.get('description', '')
    icon = data.get('icon', 'package')
    color = data.get('color', '#6366F1')
    
    if not account_id or not name:
        return jsonify({'error': 'account_id and name are required'}), 400
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        cur.execute(
            "INSERT INTO categories (account_id, name, description, icon, color) VALUES (%s, %s, %s, %s, %s) RETURNING id",
            (account_id, name, description, icon, color)
        )
        category_id = cur.fetchone()[0]
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'id': category_id, 'message': 'Categoria criada com sucesso'}), 201
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories/<category_id>', methods=['PUT'])
def update_category(category_id):
    data = request.json
    name = data.get('name')
    description = data.get('description', '')
    icon = data.get('icon')
    color = data.get('color')
    
    if not name:
        return jsonify({'error': 'name is required'}), 400
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        cur.execute(
            "UPDATE categories SET name = %s, description = %s, icon = %s, color = %s WHERE id = %s",
            (name, description, icon, color, category_id)
        )
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'message': 'Categoria atualizada com sucesso'}), 200
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories/<category_id>', methods=['DELETE'])
def delete_category(category_id):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        cur.execute("DELETE FROM categories WHERE id = %s", (category_id,))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'message': 'Categoria deletada com sucesso'}), 200
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.json
    account_id = data.get('account_id')
    category_id = data.get('category_id')
    name = data.get('name')
    description = data.get('description', '')
    sku = data.get('sku', '')
    is_active = data.get('is_active', True)
    
    if not account_id or not category_id or not name:
        return jsonify({'error': 'account_id, category_id and name are required'}), 400
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        cur.execute(
            "INSERT INTO products (account_id, category_id, name, description, sku, is_active) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
            (account_id, category_id, name, description, sku, is_active)
        )
        product_id = cur.fetchone()[0]
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'id': product_id, 'message': 'Produto criado com sucesso'}), 201
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    name = data.get('name')
    description = data.get('description', '')
    sku = data.get('sku', '')
    is_active = data.get('is_active', True)
    
    if not name:
        return jsonify({'error': 'name is required'}), 400
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        cur.execute(
            "UPDATE products SET name = %s, description = %s, sku = %s, is_active = %s WHERE id = %s",
            (name, description, sku, is_active, product_id)
        )
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'message': 'Produto atualizado com sucesso'}), 200
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        cur.execute("DELETE FROM products WHERE id = %s", (product_id,))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'message': 'Produto deletado com sucesso'}), 200
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3002, debug=False)
