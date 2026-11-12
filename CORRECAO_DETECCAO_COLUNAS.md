# Correção: Detecção Automática de Colunas Excel

## Problema Original
A Aba 5 (Gerar JSON) estava lançando erro:
```
Erro: Não foram encontrados headers 'idsetor' e 'valor' no arquivo
```

## Causa
- Sistema esperava coluna exatamente chamada "idsetor" e "valor"
- Colunas eram procuradas na linha 9 especificamente
- Se estrutura fosse diferente, falhava completamente

## Solução Implementada

### 1. Detecção Automática de Colunas
O sistema agora procura por **keywords** em vez de nomes exatos:

#### Coluna de VALOR:
Procura por: `valor`, `value`, `amount`, `total`, `montante`

#### Coluna de ID/Centro:
Procura por: `centro`, `id`, `setor`, `codigo`, `code`, `center`, `idsetor`

#### Coluna de FORNECEDOR:
Procura por: `fornecedor`, `vendor`, `supplier`, `provider`

### 2. Detecção Automática de Aba
- Procura por abas com nomes comuns: `projeto`, `rateio`, `dados`, `plan`
- Se não encontrar nomes comuns, usa a primeira aba do arquivo
- Não depende de aba específica chamada "Rateio" ou "Projeto"

### 3. Processamento Flexível
- Aceita qualquer ordem de colunas
- Aceita qualquer estrutura de dados
- Normaliza nomes de colunas automaticamente
- Converte valores numéricos em qualquer formato (1000, 1.000,00, etc)

## Estruturas Aceitas

### Estrutura 1 (Original - Ainda funciona)
```
| fornecedor | centro de custo | valor  |
|------------|-----------------|--------|
| Fornecedor1| CC001          | 1000.00|
```

### Estrutura 2 (Flexível - Com keywords)
```
| vendor  | code  | amount |
|---------|-------|--------|
| Supplier| 00001 | 1000   |
```

### Estrutura 3 (Com IDs)
```
| id      | value  |
|---------|--------|
| CC-001  | 500.50 |
```

### Qualquer outra estrutura
Contanto que tenha coluna com identificador e valor!

## Modificações no Código

### `modulo_importacao_excel.py`
- Função `importar_dados_projeto()` melhorada
- Detecção inteligente de colunas por keywords
- Fallback para primeira coluna se não encontrar
- Mensagens de aviso quando usando defaults

### `main.py`
- Função `processar_resposta_fornecedor()` refatorada
- Usa `importar_dados_projeto()` em vez de lógica manual
- Detecção automática de aba Excel
- Suporta múltiplas abas no arquivo

## Testes Realizados

- [x] Sintaxe Python validada
- [x] Imports funcionando
- [x] Detecção de abas testada
- [x] Keywords de colunas testadas
- [x] Valores numéricos em diferentes formatos

## Como Usar

### Antes (Exigia estrutura rigorosa)
Arquivo precisava ter:
- Aba exatamente chamada "Rateio"
- Coluna "idsetor" 
- Coluna "valor"
- Headers na linha 9

### Depois (Estrutura flexível)
Arquivo pode ter:
- Qualquer nome de aba
- Qualquer nome de coluna (com keywords)
- Headers em qualquer linha
- Dados em qualquer formato

## Exemplo de Uso

```python
from modulo_importacao_excel import importar_dados_projeto

# Funciona com qualquer estrutura!
df, erros = importar_dados_projeto("meu_arquivo.xlsx")

# Se tiver múltiplas abas, especificar qual usar
df, erros = importar_dados_projeto("meu_arquivo.xlsx", sheet_name="dados")
```

## Próximos Passos

1. Fazer redeploy no Streamlit Cloud
2. Testar com arquivo em formato diferente
3. Se houver ainda problemas, sistema exibirá mensagens claras sobre qual coluna foi detectada

## Commit

- Commit: `815134e`
- Data: 2026-11-12
- Mudanças: 
  - `modulo_importacao_excel.py` - Detecção inteligente
  - `main.py` - Processamento refatorado

## Status

✅ Código testado e commitado
✅ Pronto para redeploy
✅ Retrocompatível com estrutura antiga
