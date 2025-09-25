from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flasgger import Swagger
import lista_desejos

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

class ListaDesejos(Resource):
    def get(self):
        """
        Busca todos os itens da lista de desejos
        ---
        tags:
        - Lista de Desejos
        parameters:
            - name: search
              in: query
              type: string
              required: false
              description: Termo de busca para filtrar por nome do produto
        responses:
            200:
                description: Lista de itens da lista de desejos
                schema:
                    type: object
                    properties:
                        items:
                            type: array
                            items:
                                type: object
                                properties:
                                    id:
                                        type: string
                                        description: ID único do item
                                    nome:
                                        type: string
                                        description: Nome do produto
                                    valor:
                                        type: number
                                        description: Valor do produto
                                    link:
                                        type: string
                                        description: Link do produto
                                    created_at:
                                        type: string
                                        description: Data de criação
        """
        search_term = request.args.get('search')
        
        if search_term:
            items = lista_desejos.search_items(search_term)
        else:
            items = lista_desejos.get_all_items()
        
        return {"items": items}, 200

class ItemDesejo(Resource):
    def get(self, item_id):
        """
        Busca um item específico por ID
        ---
        tags:
        - Lista de Desejos
        parameters:
            - name: item_id
              in: path
              type: string
              required: true
              description: ID do item
        responses:
            200:
                description: Item encontrado
            404:
                description: Item não encontrado
        """
        item = lista_desejos.get_item_by_id(item_id)
        
        if item:
            return item, 200
        else:
            return {"message": "Item não encontrado"}, 404

    def put(self, item_id):
        """
        Atualiza um item existente
        ---
        tags:
        - Lista de Desejos
        parameters:
            - name: item_id
              in: path
              type: string
              required: true
              description: ID do item
            - in: body
              name: body
              required: true
              schema:
                type: object
                properties:
                  nome:
                    type: string
                    description: Nome do produto
                  valor:
                    type: number
                    description: Valor do produto
                  link:
                    type: string
                    description: Link do produto
        responses:
            200:
                description: Item atualizado com sucesso
            400:
                description: Dados inválidos
            404:
                description: Item não encontrado
        """
        data = request.json
        
        if not data:
            return {"message": "Dados não fornecidos"}, 400
        
        existing_item = lista_desejos.get_item_by_id(item_id)
        if not existing_item:
            return {"message": "Item não encontrado"}, 404
        
        success = lista_desejos.update_item(
            item_id=item_id,
            nome=data.get('nome'),
            valor=data.get('valor'),
            link=data.get('link')
        )
        
        if success:
            return {"message": "Item atualizado com sucesso"}, 200
        else:
            return {"message": "Erro ao atualizar item"}, 500

    def delete(self, item_id):
        """
        Remove um item da lista de desejos
        ---
        tags:
        - Lista de Desejos
        parameters:
            - name: item_id
              in: path
              type: string
              required: true
              description: ID do item
        responses:
            200:
                description: Item removido com sucesso
            404:
                description: Item não encontrado
        """
        existing_item = lista_desejos.get_item_by_id(item_id)
        if not existing_item:
            return {"message": "Item não encontrado"}, 404
        
        success = lista_desejos.delete_item(item_id)
        
        if success:
            return {"message": "Item removido com sucesso"}, 200
        else:
            return {"message": "Erro ao remover item"}, 500

class AdicionarItem(Resource):
    def post(self):
        """
        Adiciona um novo item à lista de desejos
        ---
        tags:
        - Lista de Desejos
        parameters:
            - in: body
              name: body
              required: true
              schema:
                type: object
                required:
                  - nome
                  - valor
                  - link
                properties:
                  nome:
                    type: string
                    description: Nome do produto
                  valor:
                    type: number
                    description: Valor do produto
                  link:
                    type: string
                    description: Link do produto
        responses:
            201:
                description: Item adicionado com sucesso
            400:
                description: Dados inválidos ou campos obrigatórios ausentes
        """
        data = request.json
        
        required_fields = ['nome', 'valor', 'link']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return {
                "message": f"Campos obrigatórios ausentes: {', '.join(missing_fields)}"
            }, 400
        
        try:
            valor = float(data['valor'])
            if valor < 0:
                return {"message": "Valor deve ser positivo"}, 400
        except (ValueError, TypeError):
            return {"message": "Valor deve ser um número válido"}, 400
        
        success = lista_desejos.create_item(
            nome=data['nome'],
            valor=valor,
            link=data['link']
        )
        
        if success:
            return {"message": "Item adicionado com sucesso"}, 201
        else:
            return {"message": "Erro ao adicionar item"}, 500

api.add_resource(ListaDesejos, "/lista-desejos")
api.add_resource(AdicionarItem, "/lista-desejos/adicionar")
api.add_resource(ItemDesejo, "/lista-desejos/<string:item_id>")

if __name__ == "__main__":
    app.run(debug=True)