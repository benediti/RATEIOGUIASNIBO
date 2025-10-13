"""
==============================
Configuração segura da API Nibo
==============================

1. Instale a biblioteca python-dotenv:
    pip install python-dotenv

2. Crie um arquivo chamado .env na raiz do projeto com o conteúdo:
    NIBO_API_KEY=sua_chave_aqui
    NIBO_API_URL=https://api.nibo.com.br/v1/endpoint

Essas variáveis serão carregadas automaticamente e usadas para enviar o JSON para o Nibo.
"""
import streamlit as st
import pandas as pd
import json
import io
from datetime import datetime

def ensure_exact_balance(cost_centers, target_total):
    """
    Ajusta o valor de um dos centros de custo para garantir que a soma seja 
    EXATAMENTE igual ao valor esperado, sem nenhuma diferença de precisão.
    """
    current_sum = sum(cc['value'] for cc in cost_centers)
    difference = target_total - current_sum
    
    if abs(difference) > 0:
        max_value_center = max(cost_centers, key=lambda x: x['value'])
        max_value_center['value'] = max_value_center['value'] + difference
    
    # Força a formatação para exatamente 2 casas decimais
    for cc in cost_centers:
        cc['value'] = round(cc['value'], 2)
    
    return cost_centers

def process_uploaded_file(uploaded_file, sheet_name):
    """Processa o arquivo carregado pelo usuário"""
    try:
        # Valores padrão
        stakeholder_id = "6dfc6620-16cd-4a35-be92-fc714cd3439e"
        description = "FGTS"
        reference = "ITAU"
        schedule_date = due_date = end_date = "2025-04-20"
        accrual_date = "2005-04-20"
        category_id = "714fea01-1627-4b78-a269-abee8860b936"
        
        # Lê a planilha Excel
        df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
        
        st.write("📊 **Colunas disponíveis na planilha:**")
        st.write(df.columns.tolist())
        
        # Identificar os nomes corretos das colunas
        cost_center_col = 'costCenterId'
        value_col = 'value_1'
        category_id_col = 'categoryId'
        stakeholder_id_col = 'stakeholderId'
        description_col = 'description'
        reference_col = 'reference'
        date_col = 'date'
        accrual_date_col = 'accrualDate'
        value_geral_col = 'value'
        
        # Verifica se as colunas existem
        if cost_center_col not in df.columns:
            st.error(f"❌ Coluna '{cost_center_col}' não encontrada na planilha")
            return None
            
        if value_col not in df.columns:
            st.error(f"❌ Coluna '{value_col}' não encontrada na planilha")
            return None
        
        # Substitui vírgulas por pontos nos valores
        df[value_col] = df[value_col].astype(str).str.replace(',', '.').str.strip()
        df[value_col] = pd.to_numeric(df[value_col], errors="coerce")
        df = df.dropna(subset=[value_col])
        
        # Agrupa por centro de custo e soma os valores
        grouped = df.groupby(cost_center_col)[value_col].sum().reset_index()
        
        # Calcula totais
        total_cost_centers = round(grouped[value_col].sum(), 2)
        category_value = round(float(df[value_geral_col].iloc[0]), 2)
        
        st.write(f"💰 **Soma dos centros de custo:** {total_cost_centers}")
        st.write(f"💰 **Valor total da categoria:** {category_value}")
        
        # Verifica diferença
        balance_difference = round(category_value - total_cost_centers, 2)
        if abs(balance_difference) > 0.0001:
            st.warning(f"⚠️ **Diferença detectada:** {abs(balance_difference):.2f}")
            
            # Interface para ajuste
            st.subheader("🔧 Ajustar Diferença")
            
            # Opção de criar novo centro de custo
            col1, col2 = st.columns(2)
            
            with col1:
                create_new = st.checkbox("Criar novo centro de custo para a diferença")
            
            with col2:
                if create_new:
                    new_cost_center_id = st.text_input("ID do novo centro de custo:", key="new_cc")
                else:
                    # Seleção de centro de custo existente
                    existing_options = [f"{row[cost_center_col]}" for _, row in grouped.iterrows()]
                    selected_cc = st.selectbox("Selecione o centro de custo para ajuste:", existing_options)
            
            if st.button("🔧 Aplicar Ajuste"):
                if create_new and new_cost_center_id:
                    # Adiciona novo centro de custo
                    new_row = pd.DataFrame({
                        cost_center_col: [new_cost_center_id],
                        value_col: [abs(balance_difference)]
                    })
                    grouped = pd.concat([grouped, new_row], ignore_index=True)
                elif not create_new and selected_cc:
                    # Ajusta centro de custo existente
                    for i, row in grouped.iterrows():
                        if str(row[cost_center_col]) == selected_cc:
                            grouped.at[i, value_col] += balance_difference
                            break
                
                st.success("✅ Ajuste aplicado!")
                st.rerun()
        
        # Obtém informações do cabeçalho
        if len(df) > 0:
            primeira_linha = df.iloc[0]
            
            if date_col in df.columns and pd.notna(primeira_linha[date_col]):
                try:
                    date_value = pd.to_datetime(primeira_linha[date_col])
                    schedule_date = due_date = end_date = date_value.strftime("%Y-%m-%d")
                except:
                    pass
                    
            if stakeholder_id_col in df.columns and pd.notna(primeira_linha[stakeholder_id_col]):
                stakeholder_id = str(primeira_linha[stakeholder_id_col])
                
            if description_col in df.columns and pd.notna(primeira_linha[description_col]):
                description = str(primeira_linha[description_col])
                
            if reference_col in df.columns and pd.notna(primeira_linha[reference_col]):
                reference = str(primeira_linha[reference_col])
                
            if category_id_col in df.columns and pd.notna(primeira_linha[category_id_col]):
                category_id = str(primeira_linha[category_id_col])
        
        # Cria estrutura JSON
        cost_centers_json = []
        for _, row in grouped.iterrows():
            cost_centers_json.append({
                "costCenterId": row[cost_center_col],
                "value": float(row[value_col])
            })
        
        # Ajuste final
        cost_centers_json = ensure_exact_balance(cost_centers_json, category_value)
        
        # JSON final
        output = {
            "stakeholderId": stakeholder_id,
            "description": description,
            "reference": reference,
            "scheduleDate": schedule_date,
            "dueDate": due_date,
            "accrualDate": accrual_date,
            "categories": [
                {
                    "categoryId": category_id,
                    "value": round(float(category_value), 2)
                }
            ],
            "costCenterValueType": 0,
            "costCenters": cost_centers_json,
            "recurrence": {
                "enabled": False,
                "intervaltype": 1,
                "interval": 1,
                "recurrenceendtype": 2,
                "maxoccurrences": 0,
                "enddate": end_date
            }
        }
        
        return output
        
    except Exception as e:
        st.error(f"❌ Erro ao processar arquivo: {str(e)}")
        return None

def main():
    st.set_page_config(
        page_title="Conversor Nibo - Rateio para JSON",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Conversor de Rateio para JSON - Nibo")
    st.markdown("---")
    
    # Sidebar para configurações
    with st.sidebar:
        st.header("🔧 Configurações")
        st.markdown("**Instruções:**")
        st.markdown("1. Faça upload da planilha Excel")
        st.markdown("2. Selecione a aba correta")
        st.markdown("3. Ajuste diferenças se necessário")
        st.markdown("4. Baixe o JSON gerado")
    
    # Upload do arquivo
    uploaded_file = st.file_uploader(
        "📁 **Selecione sua planilha de rateio:**",
        type=['xlsx', 'xls'],
        help="Faça upload de um arquivo Excel (.xlsx ou .xls)"
    )
    
    if uploaded_file is not None:
        try:
            # Obtém as abas disponíveis
            excel_file = pd.ExcelFile(uploaded_file)
            sheets = excel_file.sheet_names
            
            st.success(f"✅ Arquivo carregado: **{uploaded_file.name}**")
            
            # Seleção da aba
            if len(sheets) > 1:
                selected_sheet = st.selectbox(
                    "📋 **Escolha a aba da planilha:**",
                    sheets,
                    index=sheets.index("Contas Rateio") if "Contas Rateio" in sheets else 0
                )
            else:
                selected_sheet = sheets[0]
                st.info(f"📋 Usando aba: **{selected_sheet}**")
            
            # Processa o arquivo
            if st.button("🚀 **Gerar JSON**", type="primary"):
                with st.spinner("⏳ Processando arquivo..."):
                    result = process_uploaded_file(uploaded_file, selected_sheet)
                
                if result:
                    st.success("✅ **JSON gerado com sucesso!**")
                    with st.expander("👀 **Visualizar JSON gerado**", expanded=False):
                        st.json(result)
                    # Botão de download
                    json_string = json.dumps(result, ensure_ascii=False, indent=4)
                    st.download_button(
                        label="💾 **Baixar JSON**",
                        data=json_string,
                        file_name="json_postman_por_valor_revisado.json",
                        mime="application/json",
                        type="primary"
                    )
                    # Estatísticas
                    st.markdown("---")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("💰 Valor Total", f"R$ {result['categories'][0]['value']:.2f}")
                    with col2:
                        total_cc = sum(cc['value'] for cc in result['costCenters'])
                        st.metric("🏢 Total Centros Custo", f"R$ {total_cc:.2f}")
                    with col3:
                        st.metric("📊 Centros de Custo", len(result['costCenters']))

                    # Botão para enviar para Nibo
                    import os
                    from dotenv import load_dotenv
                    import requests
                    load_dotenv()
                    api_key = os.getenv("NIBO_API_KEY")
                    nibo_url = os.getenv("NIBO_API_URL")
                    if st.button("🚀 Enviar para Nibo", type="secondary"):
                        if not api_key or not nibo_url:
                            st.error("API Key ou URL da API Nibo não configuradas! Configure no arquivo .env ou nas variáveis de ambiente.")
                        else:
                            headers = {
                                "Authorization": f"Bearer {api_key}",
                                "Content-Type": "application/json"
                            }
                            try:
                                response = requests.post(nibo_url, json=result, headers=headers)
                                if response.status_code == 200:
                                    st.success("Enviado com sucesso!")
                                else:
                                    st.error(f"Erro ao enviar: {response.status_code} - {response.text}")
                            except Exception as e:
                                st.error(f"Erro na requisição: {e}")
        
        except Exception as e:
            st.error(f"❌ Erro ao ler o arquivo: {str(e)}")
    
    # Seção do conversor de números
    st.markdown("---")
    st.subheader("🔢 Conversor de Formato de Números")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Formato Brasileiro → Americano**")
        brazilian_input = st.text_area(
            "Cole valores com vírgula (formato brasileiro):",
            placeholder="1.234,56\n2.345,67\n3.456,78",
            height=150
        )
        
        if st.button("🔄 Converter"):
            if brazilian_input:
                lines = brazilian_input.strip().split('\n')
                converted = []
                for line in lines:
                    # Remove espaços e converte vírgula para ponto
                    american_format = line.strip().replace(',', '.')
                    converted.append(american_format)
                
                result_text = '\n'.join(converted)
                st.text_area("Resultado (formato americano):", value=result_text, height=150)
    
    with col2:
        st.markdown("**📋 Instruções do Conversor**")
        st.info("""
        **Como usar:**
        1. Cole os valores brasileiros (com vírgula)
        2. Clique em "Converter"
        3. Copie o resultado (com ponto)
        
        **Exemplo:**
        - Entrada: `1.234,56`
        - Saída: `1234.56`
        """)

if __name__ == "__main__":
    main()
