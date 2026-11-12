# DEPLOY NO STREAMLIT CLOUD - Guia Rápido

## Status Atual
✅ Repositório GitHub: https://github.com/benediti/RATEIOGUIASNIBO
✅ Branch: main (atualizado)
✅ Código: main.py (pronto)
✅ Dependências: requirements.txt (configurado)
✅ Configuração Streamlit: .streamlit/config.toml (criado)
✅ Dados: fornecedores_nibo.xlsx, categorias_nibo.xlsx, centros_de_custo.xlsx

## Passo 1: Acessar Streamlit Cloud
1. Vá para: https://share.streamlit.io/
2. Faça login com GitHub
3. Clique em "+ New app"

## Passo 2: Configurar o Deploy
Na tela "Create new app", preencha:
- **Repository**: benediti/RATEIOGUIASNIBO
- **Branch**: main
- **Main file path**: main.py

## Passo 3: Deploy
1. Clique em "Deploy!"
2. Aguarde 3-5 minutos
3. Seu link será algo como: https://rateioguiasnibo-xxxxx.streamlit.app

## O que será implantado
- Sistema com 5 abas funcionais
- Seleção de fornecedor
- Seleção de categoria
- Datas de vencimento e competência
- Upload de planilha Excel
- Geração e download de JSON

## Troubleshooting
Se houver erro de módulo:
1. Verifique se requirements.txt tem todas as dependências
2. No Streamlit Cloud, vá em "Settings" > "Advanced settings"
3. Configure Python version como 3.9 ou superior

## Ambiente Local (Teste)
Para testar antes de fazer deploy:
```
streamlit run main.py
```

A aplicação iniciará em http://localhost:8501

## Próximos passos após deploy
- Compartilhe o link com seus usuários
- Teste o fluxo completo
- Colha feedback para melhorias
