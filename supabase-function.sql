-- Criar função SQL que retorna dados da conta
CREATE OR REPLACE FUNCTION get_account_data(p_helena_account_id TEXT)
RETURNS JSON AS $$
DECLARE
  v_account_id UUID;
  v_result JSON;
BEGIN
  -- Buscar account_id
  SELECT id INTO v_account_id
  FROM accounts
  WHERE helena_account_id = p_helena_account_id;
  
  IF v_account_id IS NULL THEN
    RETURN json_build_object('error', 'Account not found');
  END IF;
  
  -- Retornar dados completos
  SELECT json_build_object(
    'account', json_build_object(
      'id', a.id,
      'name', a.name
    ),
    'categories', (
      SELECT COALESCE(json_agg(
        json_build_object(
          'id', c.id,
          'account_id', c.account_id,
          'name', c.name,
          'icon', c.icon,
          'color', c.color,
          'description', c.description,
          'display_order', c.display_order,
          'created_at', c.created_at,
          'updated_at', c.updated_at
        ) ORDER BY c.display_order
      ), '[]'::json)
      FROM categories c
      WHERE c.account_id = v_account_id
    ),
    'products', (
      SELECT COALESCE(json_agg(
        json_build_object(
          'id', p.id,
          'account_id', p.account_id,
          'category_id', p.category_id,
          'name', p.name,
          'description', p.description,
          'sku', p.sku,
          'status', p.status,
          'created_at', p.created_at,
          'updated_at', p.updated_at,
          'plans', (
            SELECT COALESCE(json_agg(
              json_build_object(
                'id', pl.id,
                'name', pl.name,
                'description', pl.description,
                'price', pl.price,
                'billing_cycle', pl.billing_cycle,
                'sku', pl.sku,
                'features', pl.features,
                'order', pl.display_order
              ) ORDER BY pl.display_order
            ), '[]'::json)
            FROM product_plans pl
            WHERE pl.product_id = p.id
          ),
          'addons', (
            SELECT COALESCE(json_agg(
              json_build_object(
                'id', ad.id,
                'name', ad.name,
                'description', ad.description,
                'price', ad.price,
                'billing_cycle', ad.billing_cycle,
                'sku', ad.sku,
                'type', ad.type,
                'required', ad.required,
                'compatible_plans', ad.compatible_plans
              )
            ), '[]'::json)
            FROM product_addons ad
            WHERE ad.product_id = p.id
          )
        )
      ), '[]'::json)
      FROM products p
      WHERE p.account_id = v_account_id
    )
  ) INTO v_result
  FROM accounts a
  WHERE a.id = v_account_id;
  
  RETURN v_result;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Permitir acesso anônimo à função
GRANT EXECUTE ON FUNCTION get_account_data(TEXT) TO anon;
GRANT EXECUTE ON FUNCTION get_account_data(TEXT) TO authenticated;
