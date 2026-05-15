import os
import hashlib

def process_user_login(user_input_string):
    # BUG 1: Hardcoded sensitive admin password credential
    SECRET_ADMIN_PASS = "SuperSecretPassword123!"
    
    # BUG 2: Weak MD5 hashing algorithm used for sensitive data
    insecure_hash = hashlib.md5(user_input_string.encode()).hexdigest()
    
    # BUG 3: Command Injection vulnerability (executes arbitrary shell text raw)
    os.system("echo " + user_input_string)
    
    # BUG 4: Division by zero logic loop flaw
    counter = 0
    calculated_metric = 100 / counter
    
    return insecure_hash
