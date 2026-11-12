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
    
    Retorna:
        - DataFrame com os dados
        - Lista de erros/avisos (vazio se tudo OK)
    """
    erros = []
    
    try:
        # Ler arquivo
        df = pd.read_excel(arquivo, sheet_name=sheet_name)
        
        if df.empty:
            erros.append(f"⚠️ Aba '{sheet_name}' está vazia")
            return df, erros
        
        # Verificar colunas esperadas (case-insensitive)
        colunas_normalizado = {col.lower().strip(): col for col in df.columns}
        
        colunas_necessarias = ['fornecedor', 'centro de custo', 'valor']
        colunas_encontradas = {}
        
        for col_necessaria in colunas_necessarias:
            if col_necessaria in colunas_normalizado:
                colunas_encontradas[col_necessaria] = colunas_normalizado[col_necessaria]
            else:
                # Tentar encontrar colunas parciais
                matches = [k for k in colunas_normalizado.keys() if col_necessaria in k]
                if matches:
                    colunas_encontradas[col_necessaria] = colunas_normalizado[matches[0]]
        
        if len(colunas_encontradas) < len(colunas_necessarias):
            faltantes = [c for c in colunas_necessarias if c not in colunas_encontradas]
            erros.append(f"⚠️ Colunas não encontradas: {', '.join(faltantes)}")
            erros.append(f"ℹ️ Colunas disponíveis: {', '.join(df.columns)}")
            return df, erros
        
        # Renomear colunas para padrão
        df = df.rename(columns={v: k for k, v in colunas_encontradas.items()})
        
        # Remover linhas completamente vazias
        df = df.dropna(how='all')
        
        # Converter valores
        df['valor'] = df['valor'].apply(converter_valor_numerico)
        
        # Remover linhas onde valor é 0 ou nulo
        df = df[df['valor'] > 0]
        
        if df.empty:
            erros.append("⚠️ Nenhuma linha com valor válido foi encontrada")
            return df, erros
        
        # Validar dados
        if df['fornecedor'].isna().any():
            linhas_na = df[df['fornecedor'].isna()].index.tolist()
            erros.append(f"⚠️ Linhas com fornecedor vazio: {linhas_na}")
            df = df.dropna(subset=['fornecedor'])
        
        if df['centro de custo'].isna().any():
            linhas_na = df[df['centro de custo'].isna()].index.tolist()
            erros.append(f"⚠️ Linhas com centro de custo vazio: {linhas_na}")
            df = df.dropna(subset=['centro de custo'])
        
        # Limpar valores de texto
        df['fornecedor'] = df['fornecedor'].astype(str).str.strip()
        df['centro de custo'] = df['centro de custo'].astype(str).str.strip()
        
        return df, erros
        
    except Exception as e:
        erros.append(f"❌ Erro ao importar: {str(e)}")
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
