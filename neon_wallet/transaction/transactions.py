# Définir une fonction qui renvoie l'identifiant de transaction
# d'une transaction
import hashlib
from typing import Any, List

# Importer le module ecdsa pour la signature et la vérification ECDSA
import ecdsa
from neon_wallet.transaction.transaction import Transaction
from neon_wallet.transaction.tx_in import TxIn
from neon_wallet.transaction.tx_out import TxOut
from neon_wallet.transaction.unspent_tx_out import UnspentTxOut


def get_transaction_id(transaction: Transaction) -> str:
    """get transaction id"""
    # Extraire la liste des entrées de transaction de la transaction
    tx_ins = transaction.txIns
    # Concaténer les identifiants et les indices des sorties de
    # transaction des entrées de transaction
    tx_in_content = "".join([tx_in.txOutId + str(tx_in.txOutIndex) for tx_in in tx_ins])
    # Extraire la liste des sorties de transaction de la transaction
    tx_outs = transaction.txOuts
    # Concaténer les adresses et les montants des sorties de transaction
    tx_out_content = "".join(
        [tx_out.address + str(tx_out.amount) for tx_out in tx_outs]
    )

    # Hacher le contenu des entrées et des sorties de transaction
    # avec SHA256 et le convertir en chaîne hexadécimale
    tx_in_out = tx_in_content + tx_out_content
    return hashlib.sha256((tx_in_out).encode()).hexdigest()


# Définir une fonction qui valide une transaction en fonction des sorties de transaction non dépensées
def validate_transaction(
    transaction: Transaction, a_unspent_tx_outs: List[UnspentTxOut]
) -> bool:
    "validate transaction"
    # Vérifier si la structure de la transaction est valide
    if not is_valid_transaction_structure(transaction):
        return False

    # Vérifier si l'identifiant de la transaction correspond
    # au hachage du contenu de la transaction
    if get_transaction_id(transaction) != transaction.id:
        print("invalid tx id: " + transaction.id)
        return False

    # Vérifier si toutes les entrées de transaction sont valides
    has_valid_tx_ins = all(
        [
            validate_tx_in(txIn, transaction, a_unspent_tx_outs)
            for txIn in transaction.txIns
        ]
    )

    if not has_valid_tx_ins:
        print("some of the txIns are invalid in tx: " + transaction.id)
        return False

    # Calculer la somme des montants des entrées de transaction
    total_tx_in_values = sum(
        [get_tx_in_amount(txIn, a_unspent_tx_outs) for txIn in transaction.txIns]
    )

    # Calculer la somme des montants des sorties de transaction
    total_tx_out_values = sum([txOut.amount for txOut in transaction.txOuts])

    # Vérifier si les sommes sont égales
    if total_tx_out_values != total_tx_in_values:
        print(f"totalTxOutValues !== totalTxInValues in tx: {transaction.id}")
        return False

    return True


# Définir une fonction qui valide une entrée de transaction en fonction des sorties de transaction non dépensées
def validate_tx_in(
    tx_in: TxIn,
    transaction: Transaction,
    a_unspent_tx_outs: List[UnspentTxOut],
) -> bool:
    """validate transaction in"""
    # Trouver la sortie de transaction non dépensée qui
    # correspond à l'entrée de transaction
    referenced_uTx_out = next(
        (
            uTxO
            for uTxO in a_unspent_tx_outs
            if (uTxO.txOutId == tx_in.txOutId) and (uTxO.txOutIndex == tx_in.txOutIndex)
        ),
        None,
    )
    if referenced_uTx_out is None:
        print("referenced txOut not found: " + str(tx_in))
        return False

    # Extraire l'adresse de la sortie de transaction non dépensée
    address = referenced_uTx_out.address

    # Créer une clé publique ECDSA à partir de l'adresse
    key = ecdsa.VerifyingKey.from_string(bytes.fromhex(address), curve=ecdsa.SECP256k1)

    # Vérifier la signature de l'entrée de transaction avec la clé publique et l'identifiant de la transaction
    valid_signature = key.verify(
        bytes.fromhex(tx_in.signature), bytes.fromhex(transaction.id)
    )
    if not valid_signature:
        print(
            f"invalid txIn signature: %s txId: %s address: %s {tx_in.signature}, {transaction.id}, {referenced_uTx_out.address}"
        )
        return False

    return True


# Définir une fonction qui vérifie si la structure d'une transaction est valide
def is_valid_transaction_structure(transaction: Transaction) -> bool:
    """check if is valid transaction structure"""
    # Vérifier si l'identifiant de la transaction est une chaîne de caractères
    if not isinstance(transaction.id, str):
        print("transactionId missing")
        return False

    # Vérifier si les entrées de transaction sont une liste
    if not isinstance(transaction.txIns, list):
        print("invalid txIns type in transaction")
        return False

    # Vérifier si toutes les entrées de transaction ont une structure valide
    if not all([is_valid_tx_in_structure(txIn) for txIn in transaction.txIns]):
        return False

    # Vérifier si les sorties de transaction sont une liste
    if not isinstance(transaction.txOuts, list):
        print("invalid txOuts type in transaction")
        return False

    # Vérifier si toutes les sorties de transaction ont une structure valide
    if not all([is_valid_tx_out_structure(txOut) for txOut in transaction.txOuts]):
        return False

    return True


def is_valid_tx_in_structure(tx_in: TxIn) -> bool:
    """check if valid tx in structure"""
    if tx_in is None:
        print("txIn is null")
        return False
    elif not isinstance(tx_in.signature, str):
        print("invalid signature type in txIn")
        return False
    elif not isinstance(tx_in.txOutId, str):
        print("invalid txOutId type in txIn")
        return False
    elif not isinstance(tx_in.txOutIndex, float):
        print("invalid txOutIndex type in txIn")
        return False
    else:
        return True


def is_valid_tx_out_structure(tx_out: TxOut) -> bool:
    """is valid tx out structure"""
    if tx_out is None:
        print("txOut is null")
        return False
    elif not isinstance(tx_out.address, str):
        print("invalid address type in txOut")
        return False
    elif not is_valid_address(tx_out.address):
        print("invalid TxOut address")
        return False
    elif not isinstance(tx_out.amount, float):
        print("invalid amount type in txOut")
        return False
    else:
        return True


# Définir une fonction qui vérifie si une adresse est valide
def is_valid_address(address: str) -> bool:
    """is valid address"""
    # Vérifier si la longueur de l'adresse est de 130 caractères
    if len(address) != 130:
        print(address)
        print("invalid public key length")
        return False
    # Vérifier si l'adresse ne contient que des caractères hexadécimaux
    elif not address.isalnum():
        print("public key must contain only hex characters")
        return False
    # Vérifier si l'adresse commence par 04
    elif not address.startswith("04"):
        print("public key must start with 04")
        return False
    return True


# Définir une fonction qui renvoie le montant d'une
# entrée de transaction en fonction des sorties de
# transaction non dépensées
def get_tx_in_amount(
    tx_in: TxIn,
    a_unspent_tx_outs: List[UnspentTxOut],
) -> float:
    """get transaction Amount in"""
    return float(
        find_unspent_tx_out(tx_in.txOutId, tx_in.txOutIndex, a_unspent_tx_outs).amount
    )


# Définir une fonction qui trouve la sortie de transaction
#  non dépensée qui correspond à un identifiant et un indice
# de transaction
def find_unspent_tx_out(
    transaction_id: str, index: int, a_unspent_tx_outs: List[UnspentTxOut]
) -> Any:
    """find unspent Tx out"""
    return next(
        (
            uTxO
            for uTxO in a_unspent_tx_outs
            if uTxO.txOutId == transaction_id and uTxO.txOutIndex == index
        ),
        None,
    )
