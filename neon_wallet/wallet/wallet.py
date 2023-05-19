"""wallet module"""
# Importer la bibliothèque ecdsa pour utiliser la courbe secp256k1
import json
import os
from typing import Any, List

# Importer le module copy pour cloner les objets
import copy
import ecdsa


# Importer la bibliothèque pydash pour utiliser des fonctions
# similaires à lodash
import pydash

from neon_wallet.transaction.transaction import Transaction
from neon_wallet.transaction.transactions import (
    get_public_key,
    get_transaction_id,
    sign_tx_in,
)
from neon_wallet.transaction.tx_in import TxIn

from neon_wallet.transaction.tx_out import TxOut
from neon_wallet.transaction.unspent_tx_out import UnspentTxOut
from neon_wallet.transaction_pool.transaction_pool import TransactionPool


# Créer un objet ECDSA à partir de la courbe secp256k1
EC = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)

# Définir l'emplacement de la clé privée
privateKeyLocation = os.environ.get("PRIVATE_KEY") or "node/wallet/private_key"
unspentTxOuts: List[UnspentTxOut] = []


# Définir une fonction pour lire la clé privée depuis un fichier
def get_private_from_wallet() -> str:
    """get private from wallet"""
    # Ouvrir le fichier en mode lecture et binaire
    with open(privateKeyLocation, "rb") as file:
        # Lire le contenu du fichier et le convertir en chaîne de caractères
        buffer = file.read()
        return buffer.decode()


# Définir une fonction pour remplacer la liste des UnspentTxOuts
# par une nouvelle liste
def set_unspent_tx_outs(new_unspent_tx_out: List[UnspentTxOut]) -> None:
    """set unspent tx outs"""
    # Afficher la nouvelle liste des UnspentTxOuts
    print(f"replacing unspentTxouts with: {new_unspent_tx_out}")
    # Assigner la nouvelle liste à la variable globale unspentTxOuts
    unspentTxOuts = new_unspent_tx_out


# Définir une fonction pour obtenir la clé publique à partir de la clé privée
def get_public_from_wallet() -> Any:
    """get public from wallet"""
    # Appeler la fonction getPrivateFromWallet pour lire la clé privée
    private_key = get_private_from_wallet()
    # Créer un objet ECDSA à partir de la clé privée en hexadécimal
    key = ecdsa.SigningKey.from_string(
        bytes.fromhex(private_key), curve=ecdsa.SECP256k1
    )
    # Obtenir la clé publique correspondante et l'encoder
    # en hexadécimal compressé
    return key.get_verifying_key().to_string("compressed").hex()


# Définir une fonction pour générer une clé privée aléatoire
def generate_private_key() -> Any:
    """generate private key"""
    # Créer un objet ECDSA à partir de la courbe secp256k1
    key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    # Obtenir la clé privée sous forme de chaîne de caractères en hexadécimal
    return key.to_string().hex()


# Définir une fonction pour initialiser le portefeuille
def init_wallet() -> None:
    """init wallet"""
    pr_key_loc = privateKeyLocation
    # Ne pas écraser les clés privées existantes
    if os.path.exists(pr_key_loc):
        return
    # Générer une nouvelle clé privée
    new_private_key = generate_private_key()
    # Écrire la clé privée dans le fichier
    with open(pr_key_loc, "w", encoding="utf8") as file:
        file.write(new_private_key)
    # Afficher un message indiquant l'emplacement du fichier
    print(f"nouveau portefeuille avec clé privée créé à : {pr_key_loc}")


# Définir une fonction pour supprimer le portefeuille
def delete_wallet() -> None:
    """delete wallet"""
    # Si le fichier existe, le supprimer
    if os.path.exists(privateKeyLocation):
        os.remove(privateKeyLocation)


# Définir une fonction pour obtenir le solde d'une adresse à partir
# des sorties non dépensées
def get_balance(address: str, unspent_tx_outs: List[UnspentTxOut]) -> Any:
    """get balance"""
    # Trouver les sorties non dépensées qui appartiennent à l'adresse
    unspent_tx_outs = pydash.filter_(
        unspent_tx_outs, lambda uTxO: uTxO.address == address
    )
    # Extraire les montants des sorties non dépensées
    amounts = pydash.map_(unspent_tx_outs, lambda uTxO: uTxO.amount)
    # Faire la somme des montants
    return pydash.sum_(amounts)


# Définir une fonction pour obtenir le solde du compte
def get_account_balance() -> float:
    """get account balance"""
    # Récupérer la clé publique du portefeuille
    public_key = get_public_from_wallet()
    # Récupérer la liste des UnspentTxOuts
    unspent_tx_outs = get_unspent_tx_outs()
    # Renvoyer le solde du compte en fonction de la clé publique
    # et des UnspentTxOuts
    return float(get_balance(public_key, unspent_tx_outs))


# Définir une fonction pour obtenir la liste des UnspentTxOuts
def get_unspent_tx_outs() -> List[UnspentTxOut]:
    """get unspent transaction outs"""
    # Renvoyer une copie profonde de la liste des UnspentTxOuts
    return copy.deepcopy(unspentTxOuts)


def get_my_unspent_transaction_outputs() -> Any:
    """get my unspent transaction outputs"""
    return find_unspent_tx_outs(
        get_public_from_wallet(),
        get_unspent_tx_outs(),
    )


# Définir une fonction pour envoyer une transaction
def send_transaction(address: str, amount: float) -> Transaction:
    """send transaction"""
    tx_pool = TransactionPool()
    # Créer une transaction avec l'adresse, le montant, la clé privée
    # du portefeuille, la liste des UnspentTxOuts et le pool de transactions
    _tx = create_transaction(
        address,
        amount,
        get_private_from_wallet(),
        get_unspent_tx_outs(),
        tx_pool.get_transaction_pool(),
    )
    # Ajouter la transaction au pool de transactions
    tx_pool.add_to_transaction_pool(_tx, get_unspent_tx_outs())
    # Diffuser le pool de transactions aux autres noeuds
    # broadCastTransactionPool()
    # Renvoyer la transaction créée
    return _tx


# Définir une fonction pour trouver les sorties non dépensées qui
# appartiennent à une adresse
def find_unspent_tx_outs(
    owner_address: str, unspent_tx_outs: List[UnspentTxOut]
) -> Any:
    """find unspent tx outs"""
    # Filtrer les sorties non dépensées selon l'adresse
    return pydash.filter_(
        unspent_tx_outs,
        lambda uTxO: uTxO.address == owner_address,
    )


# Définir une fonction pour trouver les sorties de
# transactions pour un montant donné
def find_tx_outs_for_amount(
    amount: float, my_unspent_tx_outs: List[UnspentTxOut]
) -> Any:
    """find tx outs for amount"""
    # Initialiser le montant courant et la liste des sorties de
    # transactions incluses
    current_amount: float = 0
    included_unspent_tx_outs = []
    # Parcourir les sorties de transactions non dépensées
    for my_unspent_tx_out in my_unspent_tx_outs:
        # Ajouter la sortie de transaction à la liste
        included_unspent_tx_outs.append(my_unspent_tx_out)
        # Augmenter le montant courant avec le montant
        # de la sortie de transaction
        current_amount = current_amount + my_unspent_tx_out.amount
        # Si le montant courant est supérieur ou égal au montant demandé
        if current_amount >= amount:
            # Calculer le montant restant
            left_over_amount = current_amount - amount
            # Retourner un dictionnaire avec les sorties de transactions
            # incluses et le montant restant
            return {
                "includedUnspentTxOuts": included_unspent_tx_outs,
                "leftOverAmount": left_over_amount,
            }

    # Si le montant demandé n'est pas atteint, lever une exception
    # avec un message d'erreur
    _e = "Cannot create transaction from the available unspent tx outputs."
    e_msg = (
        _e
        + " Required amount:"
        + str(amount)
        + ". Available unspentTxOuts:"
        + str(my_unspent_tx_outs)
    )
    raise ValueError(e_msg)


# Définir une fonction pour créer des sorties de transactions
def create_tx_outs(
    receiver_address: str,
    my_address: str,
    amount: float,
    left_over_amount: float,
) -> List[TxOut]:
    """create Tx Outs"""
    # Créer une sortie de transaction pour le destinataire
    # avec le montant demandé
    tx_out1 = TxOut(receiver_address, amount)
    # Si le montant restant est nul
    if left_over_amount == 0:
        # Retourner une liste avec la sortie de transaction
        # pour le destinataire
        return [tx_out1]
    # Sinon
    else:
        # Créer une sortie de transaction pour soi-même
        # avec le montant restant
        left_over_tx = TxOut(my_address, left_over_amount)
        # Retourner une liste avec les deux sorties de transactions
        return [tx_out1, left_over_tx]


# Définir une fonction pour filtrer les UnspentTxOuts qui
# sont utilisés dans le pool de transactions
def filter_tx_pool_txs(
    unspent_tx_outs: List[UnspentTxOut], transaction_pool: List[Transaction]
) -> List[UnspentTxOut]:
    """filter TxPool Txs"""
    # Créer une liste vide pour stocker les txIns du pool de transactions
    tx_ins = []
    # Parcourir les transactions du pool
    for _tx in transaction_pool:
        # Ajouter les txIns de chaque transaction à la liste
        tx_ins.extend(_tx.tx_ins)

    # Créer une liste vide pour stocker les UnspentTxOuts à enlever
    removable = []
    # Parcourir les UnspentTxOuts existants
    for unspent_tx_out in unspent_tx_outs:
        # Chercher si il y a un txIn qui correspond au UnspentTxOut
        tx_in = next(
            (
                aTxIn
                for aTxIn in tx_ins
                if aTxIn.tx_out_index == unspent_tx_out.tx_out_index
                and aTxIn.tx_out_id == unspent_tx_out.tx_out_id
            ),
            None,
        )
        # Si il y a un txIn correspondant, ajouter le UnspentTxOut
        # à la liste à enlever
        if tx_in is not None:
            removable.append(unspent_tx_out)

    # Créer une liste vide pour stocker les UnspentTxOuts filtrés
    filtered = []
    # Parcourir les UnspentTxOuts existants
    for unspent_tx_out in unspent_tx_outs:
        # Si le UnspentTxOut n'est pas dans la liste à enlever,
        # l'ajouter à la liste filtrée
        if unspent_tx_out not in removable:
            filtered.append(unspent_tx_out)

    return filtered


# Définir une fonction pour créer une transaction
def create_transaction(
    receiver_address: str,
    amount: float,
    private_key: str,
    unspent_tx_outs: List[UnspentTxOut],
    tx_pool: List[Transaction],
) -> Transaction:
    """create transaction"""
    print(f"txPool: {json.dumps(tx_pool)}")
    # Récupérer l'adresse du créateur de la transaction
    # à partir de sa clé privée
    my_address = get_public_key(private_key)
    # Filtrer les UnspentTxOuts qui appartiennent au
    # créateur de la transaction
    my_unspent_tx_outs_a = [
        uTxO for uTxO in unspent_tx_outs if uTxO.address == my_address
    ]
    # Filtrer les UnspentTxOuts qui ne sont pas utilisés dans le pool
    # de transactions
    my_unspent_tx_outs = filter_tx_pool_txs(my_unspent_tx_outs_a, tx_pool)

    # Trouver les UnspentTxOuts suffisants pour couvrir le montant de
    # la transaction et le reste
    included_unspent_tx_outs, left_over_amount = find_tx_outs_for_amount(
        amount, my_unspent_tx_outs
    )

    # Créer une fonction pour convertir un UnspentTxOut en un TxIn non signé
    def to_unsigned_tx_in(unspent_tx_out: UnspentTxOut) -> TxIn:
        """to unsigned tx in"""
        tx_in = TxIn("", 0, "")
        tx_in.tx_out_id = unspent_tx_out.tx_out_id
        tx_in.tx_out_index = unspent_tx_out.tx_out_index
        return tx_in

    # Créer une liste de TxIns non signés à partir des UnspentTxOuts trouvés
    i_uns_tx_outs = included_unspent_tx_outs
    unsigned_tx_ins = [to_unsigned_tx_in(uTxO) for uTxO in i_uns_tx_outs]

    # Créer une nouvelle transaction
    _tx = Transaction([], [])
    _tx.tx_ins = unsigned_tx_ins
    _tx.tx_outs = create_tx_outs(
        receiver_address,
        my_address,
        amount,
        left_over_amount,
    )
    _tx.id = get_transaction_id(_tx)

    # Signer les TxIns avec la clé privée du créateur de la transaction
    _tx.tx_ins = [
        sign_tx_in(_tx, index, private_key, unspent_tx_outs)
        for index in range(len(_tx.tx_ins))
    ]

    return _tx
