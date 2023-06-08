import hashlib
import os
import time


LIMIT_SIZE = 2100000


class MerkleNode:
    def __init__(self, hash_value, left=None, right=None):
        self.hash = hash_value
        self.left = left
        self.right = right


class MerkleTree:
    def __init__(self, file_path, hash_func='SHA-256', block_size=1024):
        self.file_path = file_path
        self.block_size = block_size
        self.time_read_file = 0
        self.hash_func = hash_func
        self.nodes = []
        self.height = 0
        self.root = self.build_tree()

    def build_tree(self):
        file_size = os.path.getsize(self.file_path)
        block_hashes = []
        start = time.time()
        with open(self.file_path, 'rb') as f:
            for _ in range(0, file_size, self.block_size):
                data = f.read(self.block_size)
                if (self.hash_func == 'SHA-256'):
                    hashed_data = hashlib.sha256(data).digest()
                elif (self.hash_func == 'MD-5'):
                    hashed_data = hashlib.md5(data).digest()
                node = MerkleNode(hashed_data)
                block_hashes.append(node)

        self.time_read_file = time.time() - start
        print('read time file: ', self.time_read_file)

        if len(block_hashes) % 2 == 1:
            block_hashes.append(block_hashes[-1])
        self.nodes.append(block_hashes)
        return self.build_tree_from_leaves(self.nodes[-1])

    def build_tree_from_leaves(self, leaves):
        if len(leaves) == 1:
            return leaves[0]
        self.height = self.height + 1
        parents = []
        for i in range(0, len(leaves), 2):
            left = leaves[i]
            if i + 1 < len(leaves):
                right = leaves[i + 1]
                parents.append(self.hash_pair(left, right))
            else:
                parents.append(left)
        self.nodes.append(parents)
        return self.build_tree_from_leaves(self.nodes[-1])

    def hash_pair(self, left, right):
        if (self.hash_func == 'SHA-256'):
            hasher = hashlib.sha256()
        elif (self.hash_func == 'MD-5'):
            hasher = hashlib.md5()
        hasher.update(left.hash)
        hasher.update(right.hash)
        node = MerkleNode(hasher.digest(), left, right)
        return node

    def get_root(self):
        return self.root

    def root_hash(self):
        return self.root.hash if self.root else None

    def get_time_read_file(self):
        return self.time_read_file


file_path = input('name file: ')
file_path = '/app/' + file_path
print(file_path)
type_hash = input('Enter type of hashing: ')
start = time.time()
merkle_tree = MerkleTree(file_path, type_hash, 1024)
time_alg = time.time() - start
print('root hash: ', merkle_tree.root_hash().hex())
print('time:')
print('reading file: ', merkle_tree.get_time_read_file())
print('algorithm all: ', time_alg)