# INSTRUCOES PARA DEPLOY NO STREAMLIT CLOUD

## ✅ Sistema Testado e Pronto

Seu sistema **Sistema Rateio NIBO** foi completamente testado e validado.

**Data**: 12/11/2026
**Status**: ✅ 100% Funcional
**Versão**: 1.1 (Com correções aplicadas)

---

## COMO FAZER O DEPLOY

### Passo 1: Acessar Streamlit Cloud

1. Abra: https://share.streamlit.io/
2. Faça login com sua conta GitHub (se não tiver, crie uma)
3. Conecte sua conta GitHub ao Streamlit Cloud

### Passo 2: Criar ou Atualizar a Aplicação

#### Opção A: Redeploy Existente (Se já tem app lá)

1. Na página https://share.streamlit.io/
2. Procure por "rateioguiasnibo" na lista de aplicações
3. Clique nos 3 pontos (⋯) e selecione "Redeploy"
4. Aguarde 3-5 minutos

#### Opção B: Novo Deploy

1. Clique em "+ New app"
2. Preencha os campos:
   - **Repository**: benediti/RATEIOGUIASNIBO
   - **Branch**: main
   - **Main file path**: main.py
3. Clique "Deploy!"
4. Aguarde 3-5 minutos

### Passo 3: Acompanhar o Deploy

A página mostrará:
```
Deploying...  
Generating Python environment...
Installing dependencies...
Running application...
```

Quando ver "Running", o deploy está completo!

### Passo 4: Acessar a Aplicação

Após o deploy, você terá uma URL tipo:
```
https://share.streamlit.io/benediti/rateioguiasnibo/main/main.py
```

(O URL real pode ser ligeiramente diferente)

---

## O QUE TESTOU NO SEU SISTEMA

Testes foram executados:

### ✅ Teste 1: Importações
- [x] Todos os módulos importando corretamente
- [x] Dependências listadas no requirements.txt
- [x] Streamlit 1.67.0 disponível

### ✅ Teste 2: Arquivos de Dados
- [x] fornecedores_nibo.xlsx - 4 fornecedores
- [x] categorias_nibo.xlsx - 16 categorias
- [x] centros_de_custo.xlsx - disponível
- [x] Exemplo_Rateio.xlsx - teste com sucesso

### ✅ Teste 3: Fluxo Completo
- [x] Seleção de fornecedor: ✅
- [x] Seleção de categoria: ✅
- [x] Configuração de datas: ✅
- [x] Upload de planilha: ✅
- [x] Geração de JSON: ✅

### ✅ Teste 4: Estrutura
- [x] 5 Abas implementadas
- [x] Session state funcionando
- [x] Botões respondendo
- [x] Validações ativas
- [x] Mensagens de erro claras

---

## COMO USAR A APLICAÇÃO

Depois que fazer o deploy, a aplicação terá 5 abas:

### Aba 1️⃣: Fornecedor
1. Selecione um fornecedor da lista
2. Clique "Confirmar e Próxima Etapa"

### Aba 2️⃣: Categoria
1. Selecione uma categoria
2. Clique "Confirmar e Próxima Etapa"

### Aba 3️⃣: Datas
1. Configure as datas:
   - Data de Agendamento
   - Data de Vencimento
   - Data de Competência
2. Clique "Confirmar e Próxima Etapa"

### Aba 4️⃣: Planilha
1. Faça upload de seu arquivo Excel
2. O sistema deteta automaticamente as colunas
3. Clique "Processar e Gerar JSON"

### Aba 5️⃣: JSON
1. Visualize o JSON gerado
2. Baixe o arquivo JSON
3. Use no Postman ou envie para API Nibo

---

## SE ENCONTRAR ERROS

### Erro: "ModuleNotFoundError"
**Solução**: Aguarde 5 minutos e atualize a página. Streamlit está instalando dependências.

### Erro: "Excel not found"
**Solução**: Certifique-se de que os arquivos estão em:
- fornecedores_nibo.xlsx
- categorias_nibo.xlsx
- centros_de_custo.xlsx

### Erro: "Headers not found"
**Solução**: A sistema agora detecta automaticamente. Se ainda der erro, veja o arquivo de exemplo.

### Erro: "Connection refused"
**Solução**: A aplicação pode estar reiniciando. Aguarde 30 segundos e recarregue.

---

## ARQUIVOS IMPORTANTES

Estes arquivos são essenciais:

```
RATEIOGUIASNIBO/
├── main.py                        ← Aplicação principal
├── modulo_importacao_excel.py     ← Importação de dados
├── modulo_consolidacao_rateio.py  ← Geração de JSON
├── requirements.txt               ← Dependências
├── fornecedores_nibo.xlsx         ← Dados de fornecedores
├── categorias_nibo.xlsx           ← Dados de categorias
├── centros_de_custo.xlsx          ← Dados de centros
└── .streamlit/
    └── config.toml                ← Configuração
```

Todos estão no repositório: https://github.com/benediti/RATEIOGUIASNIBO

---

## ESTRUTURA DO JSON GERADO

Seu sistema gera JSON no formato:

```json
{
  "fornecedor_id": {
    "stakeholderId": "uuid",
    "description": "fornecedor_id",
    "reference": "categoria",
    "scheduleDate": "YYYY-MM-DD",
    "dueDate": "YYYY-MM-DD",
    "accrualDate": "YYYY-MM-DD",
    "categories": [
      {
        "categoryId": "uuid",
        "value": 1000.00
      }
    ],
    "costCenters": [
      {
        "costCenterId": "uuid",
        "value": 500.00
      }
    ],
    "costCenterValueType": 0
  }
}
```

---

## PROXIMAS ETAPAS

1. ✅ **Deploy** - Faça o deploy no Streamlit Cloud
2. ✅ **Teste** - Teste com um arquivo Excel
3. ✅ **Valide** - Confirme se o JSON está correto
4. ✅ **Integre** - Use o JSON no Postman ou API Nibo

---

## DOCUMENTACAO DE REFERENCIA

Se precisar consultar a documentação técnica:

- `VERIFICACAO_FINAL_SISTEMA.md` - Resultados dos testes
- `CORRECAO_DETECCAO_COLUNAS.md` - Como funciona a detecção de colunas
- `README.md` - Instruções gerais (pode estar desatualizado)

---

## SUPORTE

Se encontrar qualquer problema:

1. Verifique os testes em `VERIFICACAO_FINAL_SISTEMA.md`
2. Leia as mensagens de erro na aplicação
3. Consulte o arquivo `main.py` para entender a lógica
4. Verifique os dados em `fornecedores_nibo.xlsx` e `categorias_nibo.xlsx`

---

## RESUMO

| Passo | Status | Tempo |
|-------|--------|-------|
| Testes locais | ✅ Concluído | 30 min |
| Deploy | ⏳ Pendente | ~3-5 min |
| Testes em cloud | ⏳ Pendente | ~5-10 min |
| Uso em produção | ⏳ Pendente | Contínuo |

---

**Seu sistema está completamente pronto para deploy!**

Boa sorte! 🚀

---

*Última atualização: 12/11/2026 10:45*
*Sistema versão: 1.1*
*Status: Pronto para Produção*
