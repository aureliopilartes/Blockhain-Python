import datetime
import hashlib
import json
from flask import Flask, jsonify


class Blockchain:
    
    # Testando minha primeira blockchain

    # Construtor que cria o bloco genesis e uma lista de blocos da blockhain
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')

    # Funcao responsavel por criar um bloco da blockchain recebendo como argumentos o nunce e o hash anterior.
    
    def create_block(self, proof, previous_hash): 
    
        block = {'index': len(self.chain) + 1,
                     'timestamp': str(datetime.datetime.now()),
                     'proof': proof,
                     'previous_hash': previous_hash}
        self.chain.append(block)
        return block

    # Retorna o block anterior da blockchain
    
    def get_previous_block(self):
        return self.chain[-1]

    # Esta funcao serve para realizar a validação das transações que ocorrem dentro da rede Blockchain
        # Neste desafio foi que todo hash criado devia ter 0000 no incio de sua string sha256.
        
    def proof_of_work(self, previous_proof): 
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    # Esta funcao cria um json representando o novo bloco e um hash sha256 do novo bloco que foi gerado.
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    # Uma vez que cada bloco da blockchain e criado apartir do hash anterior, esta funcao verifica se esta condicao foi respeitada, se nossa proof o f work esta funcionando perfeitamente.
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True


    
# Criando um servidor web com Flask para interagir com a blockchain.

app = Flask(__name__)

# Instanciando a class Blockchain.

blockchain = Blockchain()


# Criando as rotas de acesso  a mineracao de blocos.

@app.route('/mine_block', methods = ['GET'])

# Funcao de mineracao de blocos pegando todos os dados necessarios para gerar um novo bloco e resolver o enigma criptografico retornando o novo bloco.

def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']  
    proof = blockchain.proof_of_work(previous_proof) 
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Parabens voce acabou de minerar um bloco!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200


# Criando uma roda que rotorna toda a blockchain

@app.route('/get_chain', methods = ['GET'])

# Funcao que retorna toda a blockchain.

def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

# Rota que verifica se o bloco gerado e valido.

@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message' : ' Tudo certo, o blockchain e valido '}
    else:
        response = {'message' : ' O blockchain nao e valido '}
    return jsonify(response), 200

app.run(host = '0.0.0.0', port = 5000)
