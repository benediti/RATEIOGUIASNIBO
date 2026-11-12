import json

# JSON que estava sendo rejeitado com erro de soma
json_rejeitado = {
    "stakeholderId": "1b5c6808-754b-4842-8c0d-ee064a695688",
    "description": "Rateio - FGTS 3212107",
    "reference": "ITAU",
    "scheduleDate": "2026-11-12",
    "dueDate": "2026-12-12",
    "accrualDate": "2026-11-12",
    "value": 2730.02,
    "categories": [
        {
            "categoryId": "714fea01-1627-4b78-a269-abee8860b936",
            "value": 2730.02
        }
    ],
    "costCenterValueType": 0,
    "costCenters": [
        {
            "costCenterId": "ed179965-45cf-4428-b808-ecfc9c681d93",
            "value": 507.81
        },
        {
            "costCenterId": "8c7586fa-8f8b-4f48-93cd-115fec84a5cb",
            "value": 1234.56
        },
        {
            "costCenterId": "30d35d97-d4bd-46bb-8977-39aa1cc9d54c",
            "value": 987.65
        }
    ]
}

# Testes de integridade
print("ANALISE DO JSON REJEITADO:")
print("="*60)

# 1. Soma manual dos costCenters
soma_centros = sum(cc['value'] for cc in json_rejeitado['costCenters'])
print(f"Soma dos costCenters: R$ {soma_centros:,.2f}")

# 2. Valor em categories
valor_categoria = json_rejeitado['categories'][0]['value']
print(f"Valor em categories[0]: R$ {valor_categoria:,.2f}")

# 3. Valor na raiz
valor_root = json_rejeitado.get('value')
print(f"Valor na raiz: R$ {valor_root:,.2f}")

# 4. Validacoes
print("\nVALIDACOES:")
print("="*60)

if soma_centros == valor_root == valor_categoria:
    print("[OK] Todos os valores sao iguais")
else:
    print("[ERRO] Valores nao batem!")
    print(f"  Root == Categoria? {valor_root} == {valor_categoria} = {valor_root == valor_categoria}")
    print(f"  Root == Soma? {valor_root} == {soma_centros} = {valor_root == soma_centros}")
    print(f"  Categoria == Soma? {valor_categoria} == {soma_centros} = {valor_categoria == soma_centros}")

# 5. Verificar se ha valores com mais de 2 casas decimais
print("\nVERIFICACAO DE PRECISAO:")
print("="*60)

problema_encontrado = False
for i, cc in enumerate(json_rejeitado['costCenters']):
    # Converter para string e contar casas decimais
    valor_str = str(cc['value'])
    if '.' in valor_str:
        casas = len(valor_str.split('.')[1])
        if casas > 2:
            print(f"[AVISO] costCenters[{i}] tem {casas} casas decimais: {cc['value']}")
            problema_encontrado = True

if not problema_encontrado:
    print("[OK] Todos os valores tem 2 casas decimais ou menos")

# 6. Verificar tipos de dados
print("\nVERIFICACAO DE TIPOS:")
print("="*60)

print(f"value (raiz) type: {type(valor_root)}")
print(f"categories[0].value type: {type(valor_categoria)}")
print(f"costCenters[0].value type: {type(json_rejeitado['costCenters'][0]['value'])}")

# 7. Verificar se falta algum campo obrigatorio
print("\nCAMPOS PRESENTES:")
print("="*60)
print("Root fields:", list(json_rejeitado.keys()))
print("categories[0] fields:", list(json_rejeitado['categories'][0].keys()))
print("costCenters[0] fields:", list(json_rejeitado['costCenters'][0].keys()))
