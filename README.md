# 📊 Conversor Nibo - Rateio para JSON

Este é um conversor web que transforma planilhas de rateio Excel em arquivos JSON compatíveis com a API do Nibo.

## 🚀 Acesso Online

> 💡 **Nota:** Para usar a aplicação online, faça o deploy no [Streamlit Community Cloud](https://streamlit.io/cloud) ou execute localmente seguindo as instruções abaixo.

## ✨ Funcionalidades

- 📁 **Upload de planilhas Excel** (.xlsx, .xls)
- 📋 **Seleção automática de abas** da planilha
- 🔧 **Ajuste automático de diferenças** nos valores
- 💾 **Download do JSON** gerado
- 🔢 **Conversor de formato** de números (brasileiro ↔ americano)
- 📊 **Visualização de estatísticas** do processamento
- 🌐 **Interface responsiva** (funciona em desktop e mobile)

## 📋 Como Usar

1. **Faça upload** da sua planilha de rateio Excel
2. **Selecione a aba** correta (geralmente "Contas Rateio")
3. **Revise os dados** exibidos pela aplicação
4. **Ajuste diferenças** se necessário
5. **Baixe o JSON** gerado
6. **Use o JSON** na API do Nibo

## 📊 Estrutura da Planilha

Sua planilha deve conter as seguintes colunas:

- `costCenterId`: ID do centro de custo
- `value_1`: Valor do rateio para cada centro de custo
- `value`: Valor total da categoria
- `categoryId`: ID da categoria (opcional)
- `stakeholderId`: ID do stakeholder (opcional)
- `description`: Descrição (opcional)
- `reference`: Referência (opcional)
- `date`: Data (opcional)
- `accrualDate`: Data de competência (opcional)

## 📥 Como Baixar o Repositório

Existem várias formas de baixar este repositório:

### Opção 1: Usando Git (recomendado)

Se você tem o Git instalado, abra o terminal e execute:

```bash
git clone https://github.com/benediti/RATEIOGUIASNIBO.git
```

### Opção 2: Download como ZIP

1. Acesse o repositório: https://github.com/benediti/RATEIOGUIASNIBO
2. Clique no botão verde **"Code"** (ou **"<> Code"**)
3. Selecione **"Download ZIP"**
4. Extraia o arquivo ZIP no local desejado

### Opção 3: Usando GitHub CLI

Se você tem o GitHub CLI instalado:

```bash
gh repo clone benediti/RATEIOGUIASNIBO
```

## 🔧 Executar Localmente

Após baixar o repositório, siga estes passos:

```bash
# Entre na pasta do projeto
cd RATEIOGUIASNIBO

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
streamlit run conversor_nibo_streamlit.py
```

## 📦 Tecnologias

- **Streamlit**: Framework web para Python
- **Pandas**: Manipulação de dados Excel/CSV
- **OpenPyXL**: Leitura de arquivos Excel

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📞 Suporte

Se você encontrar problemas ou tiver dúvidas:

1. Verifique se sua planilha segue a estrutura esperada
2. Confira se todas as colunas obrigatórias estão presentes
3. Abra uma issue no GitHub se o problema persistir

---

**💡 Dica:** Este conversor foi criado para facilitar a integração com a API do Nibo, automatizando a conversão de planilhas de rateio em JSON.
