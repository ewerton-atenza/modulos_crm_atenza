from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

# Configuração do banco de dados
DB_CONFIG = {
    'host': 'supabase-db',
    'port': 5432,
    'database': 'postgres',
    'user': 'postgres',
    'password': 'atenza515351'
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.route('/health', methods=['GET'])
def health():
    print('=== GET /health ===')
    return jsonify({'status': 'ok'})

@app.route('/api/accounts', methods=['GET'])
def get_accounts():
    print('=== GET /api/accounts ===' )
    helena_account_id = request.args.get('helena_account_id')
    print(f'helena_account_id: {helena_account_id}')
    
    if not helena_account_id:
        return jsonify({'error': 'helena_account_id is required'}), 400
    
    try:
        print('Conectando ao banco...')
        conn = get_db_connection()
        print('Conectado!')
        cur = conn.cursor()
        
        print('Executando query...')
        cur.execute(
            "SELECT id, name FROM accounts WHERE helena_account_id = %s",
            (helena_account_id,)
        )
        
        row = cur.fetchone()
        print(f'Resultado: {row}')
        cur.close()
        conn.close()
        
        if row:
            return jsonify({'id': row[0], 'name': row[1]})
        else:
            return jsonify({'error': 'Account not found'}), 404
            
    except Exception as e:
        print(f'ERRO: {e}')
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories', methods=['GET'])
def get_categories():
    account_id = request.args.get('account_id')
    
    if not account_id:
        return jsonify({'error': 'account_id is required'}), 400
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            "SELECT id, account_id, name, icon, color, description, display_order, created_at, updated_at FROM categories WHERE account_id = %s ORDER BY display_order",
            (account_id,)
        )
        
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        categories = []
        for row in rows:
            categories.append({
                'id': row[0],
                'account_id': row[1],
                'name': row[2],
                'icon': row[3],
                'color': row[4],
                'description': row[5],
                'display_order': row[6],
                'created_at': row[7].isoformat() if row[7] else None,
                'updated_at': row[8].isoformat() if row[8] else None
            })
        
        return jsonify(categories)
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/products', methods=['GET'])
def get_products():
    account_id = request.args.get('account_id')
    
    if not account_id:
        return jsonify({'error': 'account_id is required'}), 400
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            "SELECT id, account_id, category_id, name, description, sku, status, created_at, updated_at FROM products WHERE account_id = %s",
            (account_id,)
        )
        
        rows = cur.fetchall()
        
        products = []
        for row in rows:
            product_id = row[0]
            
            # Buscar plans
            cur.execute(
                "SELECT id, name, description, price, billing_cycle, sku, features, display_order FROM plans WHERE product_id = %s ORDER BY display_order",
                (product_id,)
            )
            plans = []
            for plan_row in cur.fetchall():
                plans.append({
                    'id': plan_row[0],
                    'name': plan_row[1],
                    'description': plan_row[2],
                    'price': float(plan_row[3]) if plan_row[3] else 0,
                    'billing_cycle': plan_row[4],
                    'sku': plan_row[5],
                    'features': plan_row[6],
                    'order': plan_row[7]
                })
            
            # Buscar addons
            cur.execute(
                "SELECT id, name, description, price, billing_cycle, sku, type, required, compatible_plans FROM addons WHERE product_id = %s",
                (product_id,)
            )
            addons = []
            for addon_row in cur.fetchall():
                addons.append({
                    'id': addon_row[0],
                    'name': addon_row[1],
                    'description': addon_row[2],
                    'price': float(addon_row[3]) if addon_row[3] else 0,
                    'billing_cycle': addon_row[4],
                    'sku': addon_row[5],
                    'type': addon_row[6],
                    'required': addon_row[7],
                    'compatible_plans': addon_row[8]
                })
            
            products.append({
                'id': row[0],
                'account_id': row[1],
                'category_id': row[2],
                'name': row[3],
                'description': row[4],
                'sku': row[5],
                'status': row[6],
                'created_at': row[7].isoformat() if row[7] else None,
                'updated_at': row[8].isoformat() if row[8] else None,
                'plans': plans,
                'addons': addons
            })
        
        cur.close()
        conn.close()
        
        return jsonify(products)
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3002, debug=False)
