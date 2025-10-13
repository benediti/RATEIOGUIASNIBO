# 📊 Conversor Nibo - Rateio para JSON

Este é um conversor web que transforma planilhas de rateio Excel em arquivos JSON compatíveis com a API do Nibo.

## 🚀 Acesso Online

**🔗 [Clique aqui para usar a aplicação](https://seu-app.streamlit.app)**

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

## 🔧 Executar Localmente

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/conversor-nibo

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
