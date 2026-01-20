# Libs imports
import datetime
import hashlib
import json
import requests
from urllib.parse import urlparse


class Blockchain:
    def __init__(self, difficulty=4):
        """ Blockchain constructor class 

        Arguments:
        - difficulty: Número de ceros requeridos para el PoW (default: 4)
        """
        self.chain = []
        self.transactions = []
        self.difficulty = difficulty
        self.create_block(proof=1, previous_hash='0')
        self.nodes = set()

    def create_block(self, proof, previous_hash, data=None):
        """ New block creation 
        Arguments:
        - proof: Nounce del bloque actual
        - previous_hash: Hash del bloque previo
        - data: Datos o transacciones del bloque (opcional)

        Returns:
        - block: Nuevo bloque creado
        """
        block = {
            'index': len(self.chain)+1,
            'timestamp': datetime.datetime.now().timestamp(),
            'proof': proof,
            'previous_hash': previous_hash,
            'transactions': self.transactions
        }
        self.transactions = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        """ Obtencion del bloque previo de la Blockchain """

        """
    Returns:
      - Obtencion del ultimo bloque de la Blockchain
    """
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        """ Protocolo de concenso Proof of Work (PoW).

         Arguments:
          - previous_proof: Nounce del bloque previo

        Returns:
          - new_proof: Devolución del nuevo nounce obtenido con PoW.
        """
        new_proof = 1
        check_proof = False
        target = '0' * self.difficulty
        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:self.difficulty] == target:
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        """ Calculo del hash de un bloque.

        Arguments:
          - block: Identifica a un bloque de la Blockchain.

        Returns:
          - hash_block: Devuelve el hash del bloque
        """

        encoded_block = json.dumps(block, sort_keys=True, indent=4).encode()
        hash_block = hashlib.sha256(encoded_block).hexdigest()
        return hash_block

    def is_chain_valid(self, chain):
        """ Determina si la blockchain es valida.

        Arguments:
          - chain: Cadena de bloques que contiene toda la información de las trasacciones.

        Returns:
          - True/False: Devuelve un booleano en función de la validez de la Blockchain. 
            (True = Valida, False = Invalida)
        """
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(
                str(proof**2 - previous_proof**2).encode()).hexdigest()
            target = '0' * self.difficulty
            if hash_operation[:self.difficulty] != target:
                return False
            previous_block = block
            block_index += 1
        return True

    def add_transaction(self, sender, receiver, amount):
        """ Añade una nueva transacción a la lista de transacciones
        Arguments:
          - sender: Dirección del emisor
          - receiver: Dirección del receptor
          - amount: Cantidad a transferir
        Returns:
          - index: Índice del bloque que contendrá la transacción
        """
        self.transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1

    def add_node(self, address):
        """ Añade un nuevo nodo a la lista de nodos
        Arguments:
          - address: Dirección del nodo. Ejemplo: 'http://127.0.0.1:5000'
        """
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        """ Reemplaza la cadena por la más larga si es válida
        Returns:
          - True/False: Devuelve un booleano en función de si la cadena fue reemplazada
        """
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False
