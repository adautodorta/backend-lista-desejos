import os
from supabase_config import supabase, TABLE_NAME
from typing import List, Dict, Optional

def get_all_items(user_id: str) -> List[Dict]:
    """
    Busca todos os itens da lista de desejos de um usuário específico
    """
    try:
        response = supabase.table(TABLE_NAME).select("*").eq("user_id", user_id).execute()
        return response.data
    except Exception as e:
        print(f"Erro ao buscar itens: {e}")
        return []

def get_item_by_id(item_id: str, user_id: str) -> Optional[Dict]:
    """
    Busca um item específico por ID
    """
    try:
        response = supabase.table(TABLE_NAME).select("*").eq("id", item_id).eq("user_id", user_id).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Erro ao buscar item: {e}")
        return None

def create_item(nome: str, valor: float, link: str, user_id: str) -> bool:
    """
    Cria um novo item na lista de desejos para o usuário logado
    Converte valor de reais para centavos antes de salvar
    """
    try:
        data = {
            "nome": nome,
            "valor": int(valor * 100),
            "link": link,
            "user_id": user_id
        }
        supabase.table(TABLE_NAME).insert(data).execute()
        return True
    except Exception as e:
        print(f"Erro ao criar item: {e}")
        return False

def update_item(item_id: str, user_id: str, nome: str = None, valor: float = None, link: str = None) -> bool:
    """
    Atualiza um item existente, garantindo que ele pertença ao usuário
    Converte valor de reais para centavos se fornecido
    """
    try:
        update_data = {}
        if nome is not None:
            update_data["nome"] = nome
        if valor is not None:
            update_data["valor"] = int(valor * 100)
        if link is not None:
            update_data["link"] = link

        if not update_data:
            return False
            
        supabase.table(TABLE_NAME).update(update_data).eq("id", item_id).eq("user_id", user_id).execute()
        return True
    except Exception as e:
        print(f"Erro ao atualizar item: {e}")
        return False

def delete_item(item_id: str, user_id: str) -> bool:
    """
    Remove um item da lista de desejos
    """
    try:
        supabase.table(TABLE_NAME).delete().eq("id", item_id).eq("user_id", user_id).execute()
        return True
    except Exception as e:
        print(f"Erro ao deletar item: {e}")
        return False

def search_items(search_term: str, user_id: str) -> List[Dict]:
    """
    Busca itens por nome (busca parcial) nos itens do usuário logado
    """
    try:
        response = supabase.table(TABLE_NAME).select("*").eq("user_id", user_id).ilike("nome", f"%{search_term}%").execute()
        return response.data
    except Exception as e:
        print(f"Erro ao buscar itens: {e}")
        return []