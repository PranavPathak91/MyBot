import hashlib
import hmac

def pbkdf2_hmac(hash_name, password, salt, iterations, dklen=None):
    """
    Simplified PBKDF2 implementation using standard library functions
    """
    # Ensure inputs are bytes
    if isinstance(password, str):
        password = password.encode('utf-8')
    if isinstance(salt, str):
        salt = salt.encode('utf-8')
    
    # Determine hash function
    if hash_name == 'sha1':
        hash_func = hashlib.sha1
    elif hash_name == 'sha256':
        hash_func = hashlib.sha256
    else:
        raise ValueError(f"Unsupported hash function: {hash_name}")
    
    # If dklen not specified, use hash digest size
    if dklen is None:
        dklen = hash_func().digest_size
    
    # Perform key derivation
    def F(i):
        u = salt + i.to_bytes(4, 'big')
        for _ in range(iterations):
            u = hmac.new(password, u, hash_func).digest()
        return u
    
    # Generate derived key
    T = b''
    block_num = 1
    while len(T) < dklen:
        T += F(block_num)
        block_num += 1
    
    return T[:dklen]

# Monkey patch hashlib to add the missing method
import sys
sys.modules['hashlib'].pbkdf2_hmac = pbkdf2_hmac
