from Crypto.Util.number import getPrime, bytes_to_long

BANNER = r''' ______     ______     ______     __  __                         
/\  == \   /\  __ \   /\  == \   /\ \_\ \                        
\ \  __<   \ \  __ \  \ \  __<   \ \____ \                       
 \ \_____\  \ \_\ \_\  \ \_____\  \/\_____\                      
  \/_____/   \/_/\/_/   \/_____/   \/_____/                      
                                                                
 __         ______     ______     __  __     ______     _____    
/\ \       /\  ___\   /\  __ \   /\ \/ /    /\  ___\   /\  __-.  
\ \ \____  \ \  __\   \ \  __ \  \ \  _"-.  \ \  __\   \ \ \/\ \ 
 \ \_____\  \ \_____\  \ \_\ \_\  \ \_\ \_\  \ \_____\  \ \____- 
  \/_____/   \/_____/   \/_/\/_/   \/_/\/_/   \/_____/   \/____/ 
                                                                 '''

                                                             
with open("app/flag.txt", "r") as f:
    FLAG = f.read().strip()

BITS = 512
E = 16
LEAK_BITS = 416

def generate_key(bits=BITS):
    p = getPrime(bits)
    q = getPrime(bits)
    while q == p:
        q = getPrime(bits)
    n = p * q
    return n, p, q

def leak_prime(prime):
    return prime & ((1 << LEAK_BITS) - 1)

def main():
    N, P, Q = generate_key()
    P_LEAK = leak_prime(P)

    print(BANNER)
    while True:
        print("=== Welcome to Baby Leaked Cryptosystem ===")
        print("1. Get N")
        print("2. Get Leaked Primes")
        print("3. Input P and Q to get Encrypted Flag")
        print("4. Exit")
        choice = input(">> ").strip()

        if choice == '1':
            print(f"N: {N}")
        elif choice == '2':
            print(f"p_leak: {P_LEAK}")
        elif choice == '3':
            try:
                p_line = input("Input p: ").strip()
                q_line = input("Input q: ").strip()
            except EOFError:
                break

            try:
                inp_p = int(p_line)
                inp_q = int(q_line)
            except ValueError:
                print("Invalid input: integers only.")
                continue

            if inp_p == P and inp_q == Q:
                ct = pow(bytes_to_long(FLAG), E, N)
                print(f"Encrypted Flag: {ct}")
                break
            else:
                print("Incorrect primes!")
        elif choice == '4':
            print("Bye!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
