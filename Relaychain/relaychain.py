from flask import Flask, request, jsonify,send_file
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from config import config
from Blockchain import Blockchain, ModelTransaction
app = Flask(__name__)

# Load keys

@app.route('/get_public_key', methods=['GET'])
def get_public_key():  
    return send_file(
        './keys/public_key.pem',
        mimetype='application/octet-stream',
        as_attachment=True,
        download_name='public_key.pem'
    )
    
@app.route('/verify_decrypt_and_read', methods=['POST'])
def verify_decrypt_and_read():
    with open('./keys/private_key.pem', 'rb') as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None
        )
    encrypted_aes_key = bytes.fromhex(request.json['encrypted_aes_key'])
    iv = bytes.fromhex(request.json['iv'])
    encrypted_data = bytes.fromhex(request.json['encrypted_data'])
    tag = bytes.fromhex(request.json['tag'])
    aes_key = private_key.decrypt(
        encrypted_aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    cipher = Cipher(algorithms.AES(aes_key), modes.GCM(iv,tag))
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    mtx = ModelTransaction(decrypted_data)
    blockchain.add_transaction(mtx)
    blockchain.mine_block()
    return jsonify({'message': 'Transaction added and block mined successfully!'}), 200

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return jsonify({
        'length': len(chain_data),
        'chain': chain_data,
    }), 200
        
blockchain = Blockchain()    
if __name__ == '__main__':
    app.run(ssl_context=(config.certificate,config.private_key),debug=config.DEBUG)