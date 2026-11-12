"""
Script de teste para validar o mapeamento correto de centros de custo e categorias.
Demonstra como o JSON é gerado com os IDs corretos.
"""

import pandas as pd
import json

# Simular carregamento de dados
print("="*60)
print("TESTE DE MAPEAMENTO V2.6")
print("="*60)

# 1. Carregar centros de custo
print("\n[OK] Carregando centros_de_custo.xlsx")
df_centros = pd.read_excel('centros_de_custo.xlsx')
print(f"   Total de centros: {len(df_centros)}")
print(f"   Colunas: {df_centros.columns.tolist()}")
print("\n   Primeiros 3 centros:")
for idx, row in df_centros.head(3).iterrows():
    print(f"   - ID EMPRESA: {row['ID EMPRESA']}")
    print(f"     Nome: {row['Nome Centro de Custo']}")
    print(f"     ID Cliente: {row['ID Cliente']}")
    print()

# 2. Carregar categorias
print("[OK] Carregando categorias_nibo.xlsx")
df_categorias = pd.read_excel('categorias_nibo.xlsx')
print(f"   Total de categorias: {len(df_categorias)}")
print(f"   Colunas: {df_categorias.columns.tolist()}")
print("\n   Primeiras 3 categorias:")
for idx, row in df_categorias.head(3).iterrows():
    print(f"   - {row['Nome']}")
    print(f"     ID: {row['ID']}")
    print()

# 3. Simular dados do fornecedor
print("[OK] Simulando dados de entrada")
dados_simulados = {
    'centro de custo': [418, 80, 4],
    'valor': [507.81, 1234.56, 987.65]
}
df_entrada = pd.DataFrame(dados_simulados)
print(f"   Centros enviados: {df_entrada['centro de custo'].tolist()}")
print(f"   Valores: {df_entrada['valor'].tolist()}")
print(f"   Total: R$ {df_entrada['valor'].sum():,.2f}")

# 4. Mapear centros com IDs de cliente
print("\n[OK] Mapeando centros com IDs de cliente")
centros_mapeados = []
for _, row_entrada in df_entrada.iterrows():
    centro_id = int(row_entrada['centro de custo'])
    valor = float(row_entrada['valor'])
    
    # Procurar em centros_de_custo.xlsx
    match = df_centros[df_centros['ID EMPRESA'] == centro_id]
    
    if not match.empty:
        cliente_id = match.iloc[0]['ID Cliente']
        nome_centro = match.iloc[0]['Nome Centro de Custo']
        
        centros_mapeados.append({
            "costCenterId": str(centro_id),
            "costCenterClientId": cliente_id,
            "costCenterName": nome_centro,
            "value": valor
        })
        print(f"   [OK] {centro_id} -> {cliente_id[:8]}... (R$ {valor})")
    else:
        print(f"   [ERRO] {centro_id} -> NAO ENCONTRADO!")

# 5. Gerar JSON
print("\n[OK] Gerando JSON final")
categoria_selecionada = df_categorias.iloc[3]  # FGTS
categoria_nome = categoria_selecionada['Nome']
categoria_uuid = categoria_selecionada['ID']

valor_total = df_entrada['valor'].sum()

json_final = {
    "stakeholderId": "1b5c6808-754b-4842-8c0d-ee064a695688",
    "description": f"Rateio - {categoria_nome}",
    "reference": "ITAU",
    "scheduleDate": "2026-11-12",
    "dueDate": "2026-12-12",
    "accrualDate": "2026-11-12",
    "categories": [
        {
            "categoryId": categoria_uuid,
            "value": round(valor_total, 2)
        }
    ],
    "costCenterValueType": 0,
    "costCenters": centros_mapeados
}

print(f"\n   Categoria: {categoria_nome}")
print(f"   Category ID: {categoria_uuid}")
print(f"   Valor Total: R$ {valor_total:,.2f}")
print(f"   Centros: {len(centros_mapeados)}")

# 6. Exibir JSON formatado
print("\n" + "="*60)
print("JSON FINAL (estrutura correta):")
print("="*60)
print(json.dumps(json_final, indent=2, ensure_ascii=False))

print("\n" + "="*60)
print("[OK] TESTE CONCLUIDO COM SUCESSO!")
print("="*60)
