# INSTRUÇÕES DE DEPLOY - Streamlit Cloud

## ✅ PRÉ-REQUISITOS ATENDIDOS

- [x] Código no GitHub (benediti/RATEIOGUIASNIBO)
- [x] Branch main atualizado
- [x] requirements.txt configurado
- [x] .streamlit/config.toml criado
- [x] Todos os módulos importáveis
- [x] Testes locais passando
- [x] Dados (Excel files) inclusos

## 🚀 PASSO A PASSO PARA DEPLOY

### 1️⃣ Acessar Streamlit Cloud

Abra: https://share.streamlit.io/

![Passo 1: Ir para share.streamlit.io]

### 2️⃣ Fazer Login

- Clique em "Sign in"
- Use sua conta **GitHub**
- Autorize o Streamlit a acessar seus repositórios

### 3️⃣ Criar Novo App

- Clique no botão **"+ New app"** (canto superior esquerdo)

![Passo 2: Botão New app]

### 4️⃣ Configurar o Repositório

Preencha os campos:

| Campo | Valor |
|-------|-------|
| **Repository** | benediti/RATEIOGUIASNIBO |
| **Branch** | main |
| **Main file path** | main.py |

### 5️⃣ Deploy

- Clique em **"Deploy!"**
- Aguarde 3-5 minutos
- Streamlit vai:
  - Clonar o repositório
  - Instalar dependências (requirements.txt)
  - Iniciar a aplicação

### 6️⃣ Acessar o App

Seu URL será algo como:
```
https://rateioguiasnibo-xxxxx.streamlit.app
```

O link será exibido na tela do Streamlit Cloud.

## 🎯 O QUE ESPERAR

Quando o deploy terminar, você verá:

1. **Aba 1: Selecionar Fornecedor**
   - Dropdown com lista de fornecedores

2. **Aba 2: Selecionar Categoria**
   - Dropdown com categorias

3. **Aba 3: Configurar Datas**
   - Campos de data interativos

4. **Aba 4: Enviar Planilha**
   - Widget de upload de arquivo Excel

5. **Aba 5: Gerar JSON**
   - Visualização dos dados
   - Botão para download do JSON

## ⚠️ TROUBLESHOOTING

### Erro: "ModuleNotFoundError: No module named..."
- **Solução**: Verifique requirements.txt
- Vá em Settings > Advanced settings no Streamlit Cloud
- Configure Python version: 3.9 ou superior

### Erro: "No file or directory..."
- **Solução**: Verifique se os arquivos Excel estão no repositório
- Confirme o path em main.py

### Erro: "Connection timeout"
- **Solução**: Aguarde mais alguns minutos
- Streamlit pode estar instalando dependências grandes

### Aba não carrega / branca
- **Solução**: Atualize a página (F5)
- Limpe cache do navegador (Ctrl+Shift+Del)

## 📱 TESTE MANUAL APÓS DEPLOY

1. Selecione um fornecedor
2. Selecione uma categoria
3. Configure as datas
4. Faça upload de um Excel com estrutura: `idsetor | valor`
5. Clique "Gerar JSON"
6. Baixe o arquivo resultante

## 🔗 LINKS ÚTEIS

- Documentação Streamlit: https://docs.streamlit.io/
- Streamlit Cloud Docs: https://docs.streamlit.io/streamlit-cloud/
- Suporte: https://discuss.streamlit.io/

## 📞 SUPORTE

Se encontrar problemas:

1. Verifique os logs do Streamlit Cloud
2. Tente testar localmente: `streamlit run main.py`
3. Consulte a documentação em DEPLOY_STREAMLIT_CLOUD.md

---

**Status**: Pronto para deploy
**Data**: 2026-11-12
**Versão**: 1.0
