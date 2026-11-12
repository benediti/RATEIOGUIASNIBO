"""
Módulo de Importação Excel para Rateio GUIAS NIBO
Importa dados da aba "projeto" e valida estrutura
"""

import pandas as pd
import io
from typing import Dict, List, Tuple, Optional
import re


def normalizar_codigo_inteiro(valor):
    """Normaliza valores para código inteiro"""
    if pd.isna(valor):
        return None

    if not isinstance(valor, str):
        try:
            numero = float(valor)
            if numero.is_integer():
                return int(numero)
        except:
            pass

    s = str(valor).strip().replace('\xa0', '').replace(' ', '')
    if not s:
        return None

    if re.fullmatch(r'\d+([.,]0+)?', s):
        return int(float(s.replace(',', '.')))

    if re.fullmatch(r'\d{1,3}([.,]\d{3})+', s):
        return int(s.replace('.', '').replace(',', ''))

    apenas_digitos = re.sub(r'\D', '', s)
    return int(apenas_digitos) if apenas_digitos else None


def converter_valor_numerico(valor):
    """Converte valor para float"""
    if pd.isna(valor):
        return 0.0
    try:
        if isinstance(valor, str):
            valor = valor.replace(',', '.')
        return float(valor)
    except:
        return 0.0


def listar_abas_excel(arquivo) -> List[str]:
    """Lista todas as abas disponíveis no arquivo Excel"""
    try:
        excel_file = pd.ExcelFile(arquivo)
        return excel_file.sheet_names
    except Exception as e:
        raise ValueError(f"Erro ao ler arquivo Excel: {str(e)}")


def importar_dados_projeto(arquivo, sheet_name: str = "projeto") -> Tuple[pd.DataFrame, List[str]]:
    """
    Importa dados da aba 'projeto' do arquivo Excel
    Detecta automaticamente colunas de ID, centro de custo e valor
    
    Retorna:
        - DataFrame com os dados padronizados
        - Lista de erros/avisos (vazio se tudo OK)
    """
    erros = []
    
    try:
        # Ler arquivo
        df = pd.read_excel(arquivo, sheet_name=sheet_name)
        
        if df.empty:
            erros.append(f"Aba '{sheet_name}' está vazia")
            return df, erros
        
        # Criar mapa de colunas normalizadas
        colunas_normalizado = {col.lower().strip(): col for col in df.columns}
        colunas_lista = list(colunas_normalizado.keys())
        
        # Detectar coluna de VALOR (procura por: valor, value, amount, total)
        col_valor = None
        valor_keywords = ['valor', 'value', 'amount', 'total', 'montante']
        for keyword in valor_keywords:
            matches = [c for c in colunas_lista if keyword in c]
            if matches:
                col_valor = colunas_normalizado[matches[0]]
                break
        
        if col_valor is None:
            # Se não encontrou, usar última coluna como valor
            col_valor = df.columns[-1]
            erros.append(f"Coluna 'valor' não encontrada explicitamente. Usando '{col_valor}'")
        
        # Detectar coluna de ID/Centro de Custo (procura por: centro, id, setor, codigo, code)
        col_id = None
        id_keywords = ['centro', 'id', 'setor', 'codigo', 'code', 'center', 'idsetor']
        for keyword in id_keywords:
            matches = [c for c in colunas_lista if keyword in c and c != col_valor.lower()]
            if matches:
                col_id = colunas_normalizado[matches[0]]
                break
        
        if col_id is None:
            # Se não encontrou ID separado, usar primeira coluna
            col_id = df.columns[0]
            erros.append(f"Coluna 'centro de custo/ID' não encontrada. Usando '{col_id}'")
        
        # Detectar coluna de FORNECEDOR (procura por: fornecedor, vendor, supplier)
        col_fornecedor = None
        fornecedor_keywords = ['fornecedor', 'vendor', 'supplier', 'provider']
        for keyword in fornecedor_keywords:
            matches = [c for c in colunas_lista if keyword in c]
            if matches:
                col_fornecedor = colunas_normalizado[matches[0]]
                break
        
        # Se não houver coluna de fornecedor, criar uma com valor fixo
        if col_fornecedor is None:
            erros.append("Coluna 'fornecedor' não encontrada. Usando valor padrão.")
            df['fornecedor'] = 'FORNECEDOR_UNICO'
            col_fornecedor = 'fornecedor'
        
        # Criar dataframe padronizado
        df_novo = pd.DataFrame()
        df_novo['fornecedor'] = df[col_fornecedor].astype(str).str.strip()
        df_novo['centro de custo'] = df[col_id].astype(str).str.strip()
        df_novo['valor'] = df[col_valor].apply(converter_valor_numerico)
        
        # Remover linhas completamente vazias
        df_novo = df_novo.dropna(how='all')
        
        # Remover linhas onde valor é 0 ou nulo
        df_novo = df_novo[df_novo['valor'] > 0]
        
        if df_novo.empty:
            erros.append("Nenhuma linha com valor válido foi encontrada")
            return df_novo, erros
        
        # Validar dados
        if df_novo['fornecedor'].isna().any():
            df_novo = df_novo.dropna(subset=['fornecedor'])
        
        if df_novo['centro de custo'].isna().any():
            df_novo = df_novo.dropna(subset=['centro de custo'])
        
        erros.append(f"OK: {len(df_novo)} linhas importadas com sucesso")
        return df_novo, erros
        
    except Exception as e:
        erros.append(f"Erro ao importar: {str(e)}")
        return pd.DataFrame(), erros


def validar_estrutura_planilha(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Valida se a planilha tem a estrutura esperada
    
    Retorna:
        - True se válida, False caso contrário
        - Lista de mensagens de validação
    """
    mensagens = []
    
    # Verificar colunas necessárias
    colunas_necessarias = ['fornecedor', 'centro de custo', 'valor']
    colunas_faltantes = [col for col in colunas_necessarias if col not in df.columns]
    
    if colunas_faltantes:
        mensagens.append(f"❌ Colunas obrigatórias faltando: {', '.join(colunas_faltantes)}")
        return False, mensagens
    
    # Verificar se há dados
    if df.empty:
        mensagens.append("❌ Planilha vazia")
        return False, mensagens
    
    # Validações adicionais
    if df['fornecedor'].isnull().all():
        mensagens.append("❌ Coluna 'fornecedor' toda vazia")
        return False, mensagens
    
    if df['centro de custo'].isnull().all():
        mensagens.append("❌ Coluna 'centro de custo' toda vazia")
        return False, mensagens
    
    if df['valor'].isnull().all():
        mensagens.append("❌ Coluna 'valor' toda vazia")
        return False, mensagens
    
    # Avisos
    if (df['valor'] <= 0).any():
        linhas_negativas = df[df['valor'] <= 0].index.tolist()
        mensagens.append(f"⚠️ Encontradas linhas com valor <= 0: {linhas_negativas}")
    
    if df['fornecedor'].isnull().any():
        mensagens.append(f"⚠️ Encontradas linhas com fornecedor vazio")
    
    if df['centro de custo'].isnull().any():
        mensagens.append(f"⚠️ Encontradas linhas com centro de custo vazio")
    
    mensagens.append("✅ Estrutura válida")
    return True, mensagens
