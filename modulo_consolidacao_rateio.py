"""
Módulo de Consolidação de Rateio para GUIAS NIBO
Agrupa dados por fornecedor e consolida centros de custo
"""

import pandas as pd
import json
from typing import Dict, List, Tuple
from datetime import datetime
import uuid


def agrupar_por_fornecedor(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Agrupa dados por fornecedor
    
    Retorna dicionário onde:
        - chave: ID do fornecedor
        - valor: DataFrame com dados do fornecedor
    """
    grupos = {}
    
    for fornecedor, grupo_df in df.groupby('fornecedor'):
        grupos[str(fornecedor)] = grupo_df.reset_index(drop=True)
    
    return grupos


def consolidar_centros_custo(df_fornecedor: pd.DataFrame) -> List[Dict]:
    """
    Consolida centros de custo de um fornecedor
    Agrupa por centro de custo e soma valores
    
    Retorna lista de dicts com:
        - costCenterId: ID do centro de custo
        - value: valor consolidado
    """
    if df_fornecedor.empty:
        return []
    
    # Agrupar por centro de custo e somar valores
    consolidado = df_fornecedor.groupby('centro de custo')['valor'].sum().reset_index()
    consolidado.columns = ['costCenterId', 'value']
    
    # Converter para lista de dicts
    centros = []
    for _, row in consolidado.iterrows():
        centros.append({
            'costCenterId': str(row['costCenterId']).strip(),
            'value': round(float(row['value']), 2)
        })
    
    return centros


def calcular_total_rateio(centros_custo: List[Dict]) -> float:
    """Calcula valor total de um rateio"""
    return round(sum(cc['value'] for cc in centros_custo), 2)


def gerar_json_rateio(
    fornecedor_id: str,
    centros_custo: List[Dict],
    description: str = "Rateio Processado",
    reference: str = "PROC",
    schedule_date: str = None,
    due_date: str = None,
    accrual_date: str = None,
    category_id: str = None,
    category_value: float = None
) -> Dict:
    """
    Gera JSON no formato esperado pela API Nibo
    
    Parâmetros:
        - fornecedor_id: ID do stakeholder (fornecedor)
        - centros_custo: lista de dicts com {costCenterId, value}
        - description: descrição do rateio
        - reference: referência (ex: "PROC")
        - schedule_date: data de agendamento (YYYY-MM-DD)
        - due_date: data de vencimento (YYYY-MM-DD)
        - accrual_date: data de competência (YYYY-MM-DD)
        - category_id: ID da categoria
        - category_value: valor da categoria
    
    Retorna JSON estruturado para API Nibo
    """
    
    # Usar datas padrão se não fornecidas
    hoje = datetime.now().strftime("%Y-%m-%d")
    schedule_date = schedule_date or hoje
    due_date = due_date or hoje
    accrual_date = accrual_date or hoje
    
    # Calcular total
    total_value = calcular_total_rateio(centros_custo)
    
    # Se não fornecido valor de categoria, usar total
    if category_value is None:
        category_value = total_value
    
    # Se não fornecido ID de categoria, gerar UUID
    if category_id is None:
        category_id = str(uuid.uuid4())
    
    # Estrutura JSON para API Nibo
    json_rateio = {
        "stakeholderId": str(fornecedor_id),
        "description": str(description),
        "reference": str(reference),
        "scheduleDate": schedule_date,
        "dueDate": due_date,
        "accrualDate": accrual_date,
        "categories": [
            {
                "categoryId": str(category_id),
                "value": round(float(category_value), 2)
            }
        ],
        "costCenterValueType": 0,
        "costCenters": centros_custo
    }
    
    return json_rateio


def processar_rateios(
    df: pd.DataFrame,
    description: str = "Rateio Processado",
    reference: str = "PROC",
    schedule_date: str = None,
    due_date: str = None,
    accrual_date: str = None,
    category_id: str = None
) -> Tuple[Dict[str, Dict], List[str]]:
    """
    Processa todos os rateios da planilha
    
    Retorna:
        - Dictionário com {fornecedor_id: json_rateio}
        - Lista de mensagens/avisos
    """
    mensagens = []
    rateios = {}
    
    if df.empty:
        mensagens.append("❌ Nenhum dado para processar")
        return rateios, mensagens
    
    try:
        # Agrupar por fornecedor
        grupos = agrupar_por_fornecedor(df)
        mensagens.append(f"✅ {len(grupos)} fornecedor(es) encontrado(s)")
        
        # Processar cada fornecedor
        for fornecedor_id, df_fornecedor in grupos.items():
            try:
                # Consolidar centros de custo
                centros = consolidar_centros_custo(df_fornecedor)
                
                if not centros:
                    mensagens.append(f"⚠️ Fornecedor {fornecedor_id}: nenhum centro de custo consolidado")
                    continue
                
                # Calcular total
                total = calcular_total_rateio(centros)
                
                # Gerar JSON
                json_rateio = gerar_json_rateio(
                    fornecedor_id=fornecedor_id,
                    centros_custo=centros,
                    description=description,
                    reference=reference,
                    schedule_date=schedule_date,
                    due_date=due_date,
                    accrual_date=accrual_date,
                    category_id=category_id,
                    category_value=total
                )
                
                rateios[fornecedor_id] = json_rateio
                mensagens.append(
                    f"✅ Fornecedor {fornecedor_id}: "
                    f"{len(centros)} centro(s) de custo, "
                    f"total R$ {total:,.2f}"
                )
                
            except Exception as e:
                mensagens.append(f"❌ Erro ao processar fornecedor {fornecedor_id}: {str(e)}")
        
        if not rateios:
            mensagens.append("❌ Nenhum rateio foi processado com sucesso")
        
        return rateios, mensagens
        
    except Exception as e:
        mensagens.append(f"❌ Erro geral no processamento: {str(e)}")
        return rateios, mensagens


def validar_rateio(json_rateio: Dict) -> Tuple[bool, List[str]]:
    """
    Valida se um JSON de rateio está bem formado
    
    Retorna:
        - True se válido
        - Lista de erros/avisos
    """
    erros = []
    
    # Campos obrigatórios
    campos_obrigatorios = [
        'stakeholderId', 'description', 'reference',
        'scheduleDate', 'dueDate', 'accrualDate',
        'categories', 'costCenters'
    ]
    
    for campo in campos_obrigatorios:
        if campo not in json_rateio:
            erros.append(f"❌ Campo obrigatório faltando: {campo}")
    
    # Validar estrutura de categories
    if 'categories' in json_rateio:
        if not isinstance(json_rateio['categories'], list):
            erros.append("❌ 'categories' deve ser uma lista")
        elif not json_rateio['categories']:
            erros.append("❌ 'categories' não pode estar vazia")
        else:
            for cat in json_rateio['categories']:
                if 'categoryId' not in cat or 'value' not in cat:
                    erros.append("❌ Categoria sem 'categoryId' ou 'value'")
    
    # Validar estrutura de costCenters
    if 'costCenters' in json_rateio:
        if not isinstance(json_rateio['costCenters'], list):
            erros.append("❌ 'costCenters' deve ser uma lista")
        elif not json_rateio['costCenters']:
            erros.append("❌ 'costCenters' não pode estar vazia")
        else:
            for cc in json_rateio['costCenters']:
                if 'costCenterId' not in cc or 'value' not in cc:
                    erros.append("❌ Centro de custo sem 'costCenterId' ou 'value'")
    
    # Validar valores
    try:
        if 'categories' in json_rateio:
            for cat in json_rateio['categories']:
                float(cat.get('value', 0))
        if 'costCenters' in json_rateio:
            for cc in json_rateio['costCenters']:
                float(cc.get('value', 0))
    except:
        erros.append("❌ Valores contêm valores não numéricos")
    
    if erros:
        return False, erros
    
    return True, ["✅ JSON válido"]


def exportar_rateios_json(rateios: Dict[str, Dict], indent: int = 2) -> str:
    """Exporta rateios para string JSON formatada"""
    return json.dumps(rateios, indent=indent, ensure_ascii=False)


def exportar_rateios_individuais(rateios: Dict[str, Dict]) -> Dict[str, str]:
    """
    Exporta cada rateio como JSON individual
    
    Retorna dicionário com {fornecedor_id: json_string}
    """
    resultado = {}
    
    for fornecedor_id, rateio in rateios.items():
        resultado[fornecedor_id] = json.dumps(rateio, indent=2, ensure_ascii=False)
    
    return resultado
