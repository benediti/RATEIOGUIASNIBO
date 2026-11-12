"""
Sistema Integrado de Rateio NIBO - Novo Fluxo com 5 Abas
Fluxo: 1) Fornecedor -> 2) Categoria -> 3) Datas -> 4) Planilha -> 5) JSON
"""

import streamlit as st
import pandas as pd
import json
import io
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import sys
import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# Adicionar diretório ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar módulos customizados
from modulo_importacao_excel import (
    listar_abas_excel, 
    importar_dados_projeto, 
    validar_estrutura_planilha,
    converter_valor_numerico
)
from modulo_consolidacao_rateio import (
    processar_rateios,
    validar_rateio,
    exportar_rateios_json,
    exportar_rateios_individuais
)

# ========================================
# CONFIGURAÇÃO DA PÁGINA
# ========================================
st.set_page_config(
    page_title="Rateio NIBO - Novo Fluxo",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================================
# INICIALIZAR VARIÁVEIS DE SESSÃO
# ========================================
if "etapa_atual" not in st.session_state:
    st.session_state.etapa_atual = 0
    st.session_state.fornecedor_selecionado = None
    st.session_state.categoria_selecionada = None
    st.session_state.data_agendamento = datetime.now()
    st.session_state.data_vencimento = datetime.now() + timedelta(days=30)
    st.session_state.data_competencia = datetime.now()
    st.session_state.arquivo_enviado = None
    st.session_state.df_processado = None
    st.session_state.rateios = None
    st.session_state.processado = False

# ========================================
# FUNÇÕES AUXILIARES
# ========================================

@st.cache_data
def carregar_fornecedores_nibo():
    """Carrega lista de fornecedores Nibo"""
    try:
        # Procurar fornecedores_nibo.xlsx em diferentes caminhos
        caminhos_possiveis = [
            os.path.join(os.getcwd(), "fornecedores_nibo.xlsx"),
            os.path.join(os.path.dirname(__file__), "fornecedores_nibo.xlsx"),
            "C:\\Users\\bened\\Enviar-Rateio-25\\projeto\\fornecedores_nibo.xlsx",
            "C:\\Users\\bened\\RATEIOGUIASNIBO\\fornecedores_nibo.xlsx",
        ]
        
        for caminho in caminhos_possiveis:
            if os.path.exists(caminho):
                df = pd.read_excel(caminho)
                if len(df.columns) >= 2:
                    return df
        
        # Retornar exemplo padrão
        return pd.DataFrame({
            'Nome': ['Nibo Supplier 1', 'Nibo Supplier 2', 'Nibo Supplier 3', 'Nibo Supplier 4'],
            'ID': ['1b5c6808-754b-4842-8c0d-ee064a695688', 
                   'e00a5c53-1234-5678-9abc-def012345678',
                   'abc12345-6789-abcd-ef01-234567890123',
                   'def67890-1234-5678-9abc-def012345678']
        })
    except Exception as e:
        return pd.DataFrame({
            'Nome': ['Nibo Supplier 1', 'Nibo Supplier 2', 'Nibo Supplier 3', 'Nibo Supplier 4'],
            'ID': ['1b5c6808-754b-4842-8c0d-ee064a695688', 
                   'e00a5c53-1234-5678-9abc-def012345678',
                   'abc12345-6789-abcd-ef01-234567890123',
                   'def67890-1234-5678-9abc-def012345678']
        })

@st.cache_data
def carregar_categorias_nibo():
    """Carrega lista de categorias Nibo"""
    try:
        caminhos_possiveis = [
            os.path.join(os.getcwd(), "categorias_nibo.xlsx"),
            os.path.join(os.path.dirname(__file__), "categorias_nibo.xlsx"),
            "C:\\Users\\bened\\Enviar-Rateio-25\\projeto\\categorias_nibo.xlsx",
            "C:\\Users\\bened\\RATEIOGUIASNIBO\\categorias_nibo.xlsx",
        ]
        
        for caminho in caminhos_possiveis:
            if os.path.exists(caminho):
                df = pd.read_excel(caminho)
                if len(df.columns) >= 1:
                    return df
        
        # Retornar exemplo padrão
        return pd.DataFrame({
            'Categoria': ['13º Salário 3212104', '14º Salário 3212105', 'Férias 3212106', 'FGTS 3212107'],
            'ID': ['3212104', '3212105', '3212106', '3212107']
        })
    except Exception as e:
        return pd.DataFrame({
            'Categoria': ['13º Salário 3212104', '14º Salário 3212105', 'Férias 3212106', 'FGTS 3212107'],
            'ID': ['3212104', '3212105', '3212106', '3212107']
        })

def gerar_template_excel(fornecedor_id: str, fornecedor_nome: str, categoria: str, 
                        data_vencimento: str, data_pagamento: str, data_competencia: str):
    """Gera template Excel para envio para fornecedor"""
    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Rateio"
    
    # ========== SEÇÃO DE INFORMAÇÕES (Linhas 1-8) ==========
    # Linha 1: Títulos
    ws['A1'] = "INFORMAÇÕES DO RATEIO"
    ws['A1'].font = Font(bold=True, size=12)
    
    # Linha 3: Fornecedor
    ws['A3'] = "Fornecedor:"
    ws['B3'] = fornecedor_nome
    ws['B3'].font = Font(bold=True)
    
    # Linha 4: ID Fornecedor
    ws['A4'] = "ID Fornecedor:"
    ws['B4'] = fornecedor_id
    
    # Linha 5: Categoria
    ws['A5'] = "Categoria:"
    ws['B5'] = categoria
    
    # Linha 6: Data Vencimento
    ws['A6'] = "Data Vencimento:"
    ws['B6'] = data_vencimento
    
    # Linha 7: Data Pagamento
    ws['A7'] = "Data Pagamento:"
    ws['B7'] = data_pagamento
    
    # Linha 8: Data Competência
    ws['A8'] = "Data Competência:"
    ws['B8'] = data_competencia
    
    # ========== CABEÇALHOS (Linha 9) ==========
    ws['A9'] = "idsetor"
    ws['B9'] = "valor"
    
    # Formatação cabeçalhos
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF")
    
    for col in ['A', 'B']:
        cell = ws[f'{col}9']
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
    
    # ========== DADOS (Linhas 10+) ==========
    # Adicionar 20 linhas vazias para preenchimento
    for row in range(10, 30):
        ws[f'A{row}'].alignment = Alignment(horizontal="center")
        ws[f'B{row}'].alignment = Alignment(horizontal="right")
        ws[f'B{row}'].number_format = '0.00'
    
    # Larguras das colunas
    ws.column_dimensions['A'].width = 20
    ws.column_dimensions['B'].width = 15
    
    return wb

def processar_resposta_fornecedor(arquivo, fornecedor_id: str, categoria: str, 
                                  data_vencimento: str, data_pagamento: str, data_competencia: str):
    """Processa resposta do fornecedor e gera JSON"""
    
    try:
        # Tentar ler a aba "Rateio"
        try:
            df = pd.read_excel(arquivo, sheet_name="Rateio")
        except:
            # Se não existir, tentar ler a primeira aba
            df = pd.read_excel(arquivo, sheet_name=0)
        
        # Tentar validar headers na linha 9 (índice 8)
        if len(df) > 8:
            headers = [str(df.iloc[8, 0]).strip().lower(), str(df.iloc[8, 1]).strip().lower()]
            
            if headers[0] != 'idsetor' or headers[1] != 'valor':
                # Se não encontrar na linha 9, procurar em outras linhas
                found = False
                for row_idx in range(len(df)):
                    if (str(df.iloc[row_idx, 0]).strip().lower() == 'idsetor' and 
                        str(df.iloc[row_idx, 1]).strip().lower() == 'valor'):
                        # Encontrou headers, usar próxima linha como início dos dados
                        data_start_row = row_idx + 1
                        headers_row = row_idx
                        found = True
                        break
                
                if not found:
                    return None, ["Erro: Não foram encontrados headers 'idsetor' e 'valor' no arquivo"]
            else:
                data_start_row = 9
                headers_row = 8
        else:
            return None, ["Erro: Arquivo Excel muito curto ou vazio"]
        
        # Ler dados a partir da linha indicada
        dados = []
        for idx in range(data_start_row, len(df)):
            try:
                idsetor_val = str(df.iloc[idx, 0]).strip()
                valor_str = df.iloc[idx, 1]
                
                # Pular linhas vazias
                if pd.isna(valor_str) or str(valor_str).strip() == '':
                    continue
                
                valor = converter_valor_numerico(valor_str)
                
                if valor > 0 and idsetor_val and idsetor_val != 'nan' and idsetor_val.upper() != 'IDSETOR':
                    dados.append({
                        'idsetor': idsetor_val,
                        'valor': valor
                    })
            except:
                continue
        
        if not dados:
            return None, ["Erro: Nenhum dado válido encontrado na planilha. Verifique se tem dados nas colunas idsetor e valor"]
        
        # Gerar JSON
        json_rateio = {
            "stakeholderId": fornecedor_id,
            "description": f"Rateio - {categoria}",
            "reference": categoria,
            "scheduleDate": str(data_pagamento),
            "dueDate": str(data_vencimento),
            "accrualDate": str(data_competencia),
            "costCenterValueType": 0,
            "costCenters": [
                {
                    "costCenterId": d['idsetor'],
                    "value": d['valor']
                }
                for d in dados
            ],
            "categories": [
                {
                    "categoryId": categoria,
                    "value": sum(d['valor'] for d in dados)
                }
            ]
        }
        
        # Validar JSON
        total = sum(cc['value'] for cc in json_rateio['costCenters'])
        mensagens = [f"OK: {len(dados)} centros de custo processados. Total: R$ {total:,.2f}"]
        
        return json_rateio, mensagens
        
    except Exception as e:
        return None, [f"Erro ao processar: {str(e)}"]

# ========================================
# HEADER
# ========================================
st.markdown("""
<style>
    .header-main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
    }
    .header-main h1 {
        margin: 0;
    }
</style>
<div class="header-main">
    <h1>💰 Sistema de Rateio NIBO - Novo Fluxo</h1>
    <p>Gestão Integrada: Fornecedor → Categoria → Datas → Planilha → JSON</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ========================================
# SIDEBAR - RESUMO DO FLUXO
# ========================================
with st.sidebar:
    st.subheader("📋 Resumo do Fluxo")
    
    # Indicador de progresso
    etapas = [
        "1️⃣ Fornecedor",
        "2️⃣ Categoria",
        "3️⃣ Datas",
        "4️⃣ Planilha",
        "5️⃣ JSON"
    ]
    
    for i, etapa in enumerate(etapas):
        if i <= st.session_state.etapa_atual:
            st.markdown(f"✅ {etapa}")
        else:
            st.markdown(f"⭕ {etapa}")
    
    st.markdown("---")
    
    # Botão Reset
    if st.button("🔄 Reiniciar Fluxo", use_container_width=True):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

# ========================================
# ABA 1: SELECIONAR FORNECEDOR
# ========================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1️⃣ Fornecedor",
    "2️⃣ Categoria",
    "3️⃣ Datas",
    "4️⃣ Planilha",
    "5️⃣ JSON"
])

with tab1:
    st.header("Passo 1: Selecionar Fornecedor")
    st.write("Escolha o fornecedor que receberá a planilha de rateio")
    
    st.markdown("---")
    
    df_fornecedores = carregar_fornecedores_nibo()
    
    if not df_fornecedores.empty:
        # Criar lista de opções
        col_nome = df_fornecedores.columns[0]
        col_id = df_fornecedores.columns[1]
        
        opcoes = [f"{row[col_nome]} ({row[col_id][:8]}...)" 
                  for idx, row in df_fornecedores.iterrows()]
        
        idx_selecionado = st.selectbox(
            "Selecione o fornecedor:",
            range(len(df_fornecedores)),
            format_func=lambda x: opcoes[x],
            key="select_fornecedor"
        )
        
        fornecedor_selecionado = df_fornecedores.iloc[idx_selecionado]
        # Armazenar como dicionário simples
        st.session_state.fornecedor_selecionado = {
            'nome': str(fornecedor_selecionado[col_nome]),
            'id': str(fornecedor_selecionado[col_id])
        }
        st.session_state.etapa_atual = max(0, st.session_state.etapa_atual)
        
        # Mostrar detalhes
        st.markdown("### Detalhes do Fornecedor")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Nome:** {st.session_state.fornecedor_selecionado['nome']}")
        
        with col2:
            st.write(f"**ID:** `{st.session_state.fornecedor_selecionado['id']}`")
        
        # Botão para próxima etapa
        if st.button("✅ Confirmar e Próxima Etapa", type="primary", use_container_width=True):
            st.session_state.etapa_atual = 1
            st.rerun()
    else:
        st.warning("Nenhum fornecedor disponível. Verifique o arquivo fornecedores_nibo.xlsx")

# ========================================
# ABA 2: SELECIONAR CATEGORIA
# ========================================
with tab2:
    st.header("Passo 2: Selecionar Categoria")
    st.write("Escolha a categoria de rateio (ex: 13º Salário, Férias, etc.)")
    
    st.markdown("---")
    
    if st.session_state.fornecedor_selecionado is not None:
        df_categorias = carregar_categorias_nibo()
        
        if not df_categorias.empty:
            col_categoria = df_categorias.columns[0]
            
            opcoes_categoria = [str(row[col_categoria]) for idx, row in df_categorias.iterrows()]
            
            categoria_selecionada = st.selectbox(
                "Selecione a categoria:",
                opcoes_categoria,
                key="select_categoria"
            )
            
            st.session_state.categoria_selecionada = categoria_selecionada
            st.session_state.etapa_atual = max(1, st.session_state.etapa_atual)
            
            # Mostrar detalhes
            st.markdown("### Detalhes da Categoria")
            st.write(f"**Categoria:** {categoria_selecionada}")
            
            # Botão para próxima etapa
            if st.button("✅ Confirmar e Próxima Etapa", type="primary", use_container_width=True, key="btn_cat"):
                st.session_state.etapa_atual = 2
                st.rerun()
        else:
            st.warning("Nenhuma categoria disponível")
    else:
        st.info("👈 Selecione um fornecedor na aba anterior primeiro")

# ========================================
# ABA 3: SELECIONAR DATAS
# ========================================
with tab3:
    st.header("Passo 3: Definir Datas")
    st.write("Configure as datas de agendamento, vencimento e competência")
    
    st.markdown("---")
    
    if st.session_state.categoria_selecionada is not None:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            data_agendamento = st.date_input(
                "📅 Data de Agendamento:",
                value=st.session_state.data_agendamento,
                key="date_agendamento"
            )
            st.session_state.data_agendamento = data_agendamento
        
        with col2:
            data_vencimento = st.date_input(
                "📅 Data de Vencimento:",
                value=st.session_state.data_vencimento,
                key="date_vencimento"
            )
            st.session_state.data_vencimento = data_vencimento
        
        with col3:
            data_competencia = st.date_input(
                "📅 Data de Competência:",
                value=st.session_state.data_competencia,
                key="date_competencia"
            )
            st.session_state.data_competencia = data_competencia
        
        st.session_state.etapa_atual = max(2, st.session_state.etapa_atual)
        
        # Resumo
        st.markdown("### Resumo das Datas")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write(f"**Agendamento:** {data_agendamento.strftime('%d/%m/%Y')}")
        
        with col2:
            st.write(f"**Vencimento:** {data_vencimento.strftime('%d/%m/%Y')}")
        
        with col3:
            st.write(f"**Competência:** {data_competencia.strftime('%d/%m/%Y')}")
        
        # Botão para próxima etapa
        if st.button("✅ Confirmar e Próxima Etapa", type="primary", use_container_width=True, key="btn_data"):
            st.session_state.etapa_atual = 3
            st.rerun()
    else:
        st.info("👈 Selecione a categoria na aba anterior primeiro")

# ========================================
# ABA 4: UPLOAD PLANILHA
# ========================================
with tab4:
    st.header("Passo 4: Enviar Planilha de Rateio")
    st.write("Faça upload da planilha preenchida pelo fornecedor com os centros de custo e valores")
    
    st.markdown("---")
    
    if st.session_state.data_competencia is not None:
        # Opção 1: Download do template
        st.subheader("📥 Baixar Template")
        st.write("Clique no botão abaixo para baixar um template pronto para enviar ao fornecedor:")
        
        if st.session_state.fornecedor_selecionado is not None and st.session_state.categoria_selecionada is not None:
            fornecedor_nome = st.session_state.fornecedor_selecionado['nome']
            fornecedor_id = st.session_state.fornecedor_selecionado['id']
            categoria = st.session_state.categoria_selecionada
            
            # Gerar template
            wb = gerar_template_excel(
                str(fornecedor_id),
                str(fornecedor_nome),
                str(categoria),
                st.session_state.data_vencimento.strftime('%d/%m/%Y'),
                st.session_state.data_agendamento.strftime('%d/%m/%Y'),
                st.session_state.data_competencia.strftime('%d/%m/%Y')
            )
            
            # Converter para bytes
            buffer = io.BytesIO()
            wb.save(buffer)
            buffer.seek(0)
            
            st.download_button(
                label="📥 Baixar Template Excel",
                data=buffer.getvalue(),
                file_name=f"Template_Rateio_{fornecedor_nome.replace(' ', '_')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        
        st.markdown("---")
        
        # Opção 2: Upload do arquivo preenchido
        st.subheader("📤 Upload do Arquivo Preenchido")
        st.write("Envie a planilha preenchida pelo fornecedor:")
        
        arquivo_enviado = st.file_uploader(
            "Selecione o arquivo Excel preenchido",
            type=["xlsx", "xls"],
            key="upload_planilha"
        )
        
        if arquivo_enviado:
            st.session_state.arquivo_enviado = arquivo_enviado
            st.success("✅ Arquivo carregado com sucesso!")
            
            st.session_state.etapa_atual = max(3, st.session_state.etapa_atual)
            
            # Botão para próxima etapa
            if st.button("✅ Processar e Ir para Próxima Etapa", type="primary", use_container_width=True, key="btn_upload"):
                st.session_state.etapa_atual = 4
                st.rerun()
    else:
        st.info("👈 Defina as datas na aba anterior primeiro")

# ========================================
# ABA 5: GERAR E BAIXAR JSON
# ========================================
with tab5:
    st.header("Passo 5: Visualizar e Exportar JSON")
    st.write("Revise os dados e gere o JSON para envio à API Nibo")
    
    st.markdown("---")
    
    if st.session_state.arquivo_enviado is not None:
        # Processar arquivo
        with st.spinner("Processando arquivo..."):
            json_gerado, mensagens = processar_resposta_fornecedor(
                st.session_state.arquivo_enviado,
                st.session_state.fornecedor_selecionado['id'],
                st.session_state.categoria_selecionada,
                st.session_state.data_vencimento.strftime('%Y-%m-%d'),
                st.session_state.data_agendamento.strftime('%Y-%m-%d'),
                st.session_state.data_competencia.strftime('%Y-%m-%d')
            )
        
        # Exibir mensagens
        for msg in mensagens:
            if "Erro" in msg or "❌" in msg:
                st.error(msg)
            else:
                st.success(msg)
        
        if json_gerado:
            st.session_state.rateios = {
                st.session_state.fornecedor_selecionado['id']: json_gerado
            }
            st.session_state.processado = True
        else:
            st.stop()
    
    if st.session_state.processado and st.session_state.rateios:
        # Exibir JSON
        st.subheader("📊 Informações do Rateio")
        
        fornecedor_id = list(st.session_state.rateios.keys())[0]
        json_rateio = st.session_state.rateios[fornecedor_id]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Fornecedor (Stakeholder):** {json_rateio.get('stakeholderId', 'N/A')}")
            st.write(f"**Descrição:** {json_rateio.get('description', 'N/A')}")
            st.write(f"**Referência:** {json_rateio.get('reference', 'N/A')}")
        
        with col2:
            st.write(f"**Data de Agendamento:** {json_rateio.get('scheduleDate', 'N/A')}")
            st.write(f"**Data de Vencimento:** {json_rateio.get('dueDate', 'N/A')}")
            st.write(f"**Data de Competência:** {json_rateio.get('accrualDate', 'N/A')}")
        
        # Centros de custo
        st.subheader("💰 Centros de Custo")
        df_centros = pd.DataFrame(json_rateio.get('costCenters', []))
        st.dataframe(df_centros, use_container_width=True)
        
        # Total
        total_rateio = sum(cc['value'] for cc in json_rateio.get('costCenters', []))
        st.metric("Valor Total", f"R$ {total_rateio:,.2f}")
        
        # JSON formatado
        st.subheader("📄 JSON para API Nibo")
        json_formatado = json.dumps(json_rateio, indent=2, ensure_ascii=False)
        st.code(json_formatado, language="json")
        
        # Downloads
        st.markdown("---")
        st.subheader("💾 Download")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                label="📥 Download JSON",
                data=json_formatado,
                file_name=f"rateio_{fornecedor_id[:8]}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col2:
            st.download_button(
                label="📥 Download Planilha (CSV)",
                data=st.session_state.arquivo_enviado.getvalue().decode('utf-8') if isinstance(st.session_state.arquivo_enviado.getvalue(), bytes) else st.session_state.arquivo_enviado.getvalue(),
                file_name=f"rateio_dados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    else:
        st.info("👈 Envie a planilha preenchida na aba anterior")

# ========================================
# FOOTER
# ========================================
st.markdown("---")
st.markdown("""
**Dúvidas?**
- ✅ Formato de data: DD/MM/YYYY
- 💰 Valores: use ponto (.) ou vírgula (,) como separador decimal
- 🆔 ID Setor: copie exatamente do arquivo de centros de custo
- 📧 Suporte: contato@equippe.com.br
""")
