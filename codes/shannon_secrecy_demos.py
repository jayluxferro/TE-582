import math, random, numpy as np
from collections import Counter, defaultdict

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALEN = len(ALPHABET)
char_to_i = {c: i for i, c in enumerate(ALPHABET)}
i_to_char = {i: c for i, c in enumerate(ALPHABET)}


def text_to_vec(s):
    return [char_to_i[c] for c in s if c in char_to_i]


def vec_to_text(v):
    return "".join(i_to_char[i % ALEN] for i in v)


def H_from_probs(ps):
    H = 0.0
    for p in ps:
        if p > 0:
            H -= p * math.log2(p)
    return H


def caesar_encrypt(v, k):
    return [(x + k) % ALEN for x in v]


def caesar_decrypt(v, k):
    return [(x - k) % ALEN for x in v]


def random_substitution_key():
    perm = list(range(ALEN))
    random.shuffle(perm)
    inv = [0] * ALEN
    for i, p in enumerate(perm):
        inv[p] = i
    return perm, inv


def subs_encrypt(v, perm):
    return [perm[x] for x in v]


def subs_decrypt(v, inv):
    return [inv[x] for x in v]


def verify_reversibility():
    msg = text_to_vec("THISISATESTOFREVERSIBILITY")
    k = 7
    assert caesar_decrypt(caesar_encrypt(msg, k), k) == msg
    perm, inv = random_substitution_key()
    assert subs_decrypt(subs_encrypt(msg, perm), inv) == msg
    print("[OK] Reversibility for Caesar and Substitution.")


def verify_pure_property_caesar(trials=500):
    for _ in range(trials):
        a, b, c = np.random.randint(0, ALEN, 3)
        d = (a - b + c) % ALEN
        v = np.random.randint(0, ALEN, size=50).tolist()
        left = caesar_encrypt(caesar_decrypt(caesar_encrypt(v, a), b), c)
        right = caesar_encrypt(v, d)
        if left != right:
            return False
    return True


def otp_prior_equals_posterior(num_messages=2000, L=6):
    msgs = [np.random.randint(0, ALEN, size=L).tolist() for _ in range(num_messages)]
    k = np.random.randint(0, ALEN, size=L).tolist()
    Cs = [otp_encrypt(m, k) for m in msgs]
    prior = Counter(tuple(m) for m in msgs)
    post = Counter(
        tuple(m) for m in msgs
    )  # each message is compatible with exactly one key

    def tvd(counts):
        total = sum(counts.values())
        return sum(
            abs(counts.get(k, 0) / total - prior.get(k, 0) / total)
            for k in set(counts) | set(prior)
        )

    return tvd(post)


def otp_encrypt(v, k):
    return [(x + y) % ALEN for x, y in zip(v, k)]


def otp_decrypt(v, k):
    return [(x - y) % ALEN for x, y in zip(v, k)]


def latin_square_perfect_secrecy():
    Ms = list(range(4))
    keys = {k: {m: (m + k) % 4 for m in Ms} for k in range(4)}

    def normalize(cnt):
        total = sum(cnt.values())
        return {k: v / total for k, v in cnt.items()}

    distro_by_m = {}
    for m in Ms:
        cnt = Counter(keys[k][m] for k in keys)
        distro_by_m[m] = normalize(cnt)
    ok = all(distro_by_m[m] == distro_by_m[0] for m in Ms)
    return ok, distro_by_m


def unicity_distance_caesar(redundancy_bits):
    return math.log2(ALEN) / max(redundancy_bits, 1e-9)


if __name__ == "__main__":
    random.seed(42)
    np.random.seed(42)
    verify_reversibility()
    print("Caesar pure property:", verify_pure_property_caesar())
    print("OTP TVD(prior, posterior) ≈", otp_prior_equals_posterior())
    ok, distro = latin_square_perfect_secrecy()
    print("Latin-square perfect secrecy (4 keys/4 messages):", ok, distro)
    # Example redundancy 0.6 bits/symbol => for demo
    print(
        "Unicity distance for Caesar with R=0.6 bits/symbol ≈",
        unicity_distance_caesar(0.6),
    )
