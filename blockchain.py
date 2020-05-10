import time

from block import Block


def is_valid_proof(block, block_hash):
    """
    Check if block_hash is valid hash of block and satisfies
    the difficulty criteria.
    """
    return (block_hash.startswith('0' * BlockChain.difficulty) and
            block_hash == block.compute_hash())


def proof_of_work(block):
    """
    Function that tries different values of the nonce to get a hash
    that satisfies our difficulty criteria.
    """
    block.nonce = 0

    computed_hash = block.compute_hash()
    while not computed_hash.startswith('0' * BlockChain.difficulty):
        block.nonce += 1
        computed_hash = block.compute_hash()

    return computed_hash


class BlockChain:
    # difficulty of our PoW algorithm
    difficulty = 5

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    @property
    def last_block(self):
        return self.chain[-1]

    def create_genesis_block(self):
        """
        A function to generate genesis block and appends it to
        the chain. The block has index 0, previous_hash as 0, and
        a valid hash.
        """
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    def add_block(self, block, proof):
        """
        A function that adds the block to the chain after verification.
        Verification includes:
        * Checking if the proof is valid.
        * The previous_hash referred in the block and the hash of a latest block
          in the chain match.
        """
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False
        if not is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self):
        """
        This function serves as an interface to add the pending
        transactions to the blockchain by adding them to the block
        and figuring out Proof Of Work.
        """
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block

        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)

        proof = proof_of_work(new_block)
        self.add_block(new_block, proof)

        self.unconfirmed_transactions = []
        return new_block.index
