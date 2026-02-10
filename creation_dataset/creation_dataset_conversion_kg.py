import json
import random
from decimal import Decimal, getcontext

getcontext().prec = 12


def fmt_decimal(x: Decimal) -> str:
    s = format(x.normalize(), "f")
    return "0" if s in ("-0", "-0.0") else s


# ---------- POOLS ----------

def build_grams_pool(max_examples: int):
    """
    Génère automatiquement un pool large de grammes
    incluant entiers + décimaux pédagogiques
    """
    pool = set()

    # entiers
    for g in range(1, max_examples * 50):
        pool.add(Decimal(g))

    # décimaux utiles
    decimals = ["0.1", "0.25", "0.5", "0.75"]
    for d in decimals:
        for base in range(1, max_examples * 10):
            pool.add(Decimal(d) * Decimal(base))

    return sorted(pool)


def build_kg_pool(max_examples: int):
    """
    Pool kg compatible *1000 => grammes entiers
    """
    pool = set()

    for i in range(1, max_examples * 5):
        pool.add(Decimal(i))

    decimals = ["0.001", "0.01", "0.05", "0.1", "0.25", "0.5", "0.75"]
    for d in decimals:
        for base in range(1, max_examples * 10):
            pool.add(Decimal(d) * Decimal(base))

    return sorted(pool)


# ---------- GENERATORS ----------

def gen_g_to_kg_examples(n: int, seed: int = 42):
    random.seed(seed)
    grams_pool = build_grams_pool(n)

    selected = random.sample(grams_pool, n)
    examples = []

    for g in selected:
        kg = g / Decimal("1000")

        g_str = fmt_decimal(g)
        kg_str = fmt_decimal(kg)

        examples.append({
            "instruction": f"Convertis {g_str} g en kg.",
            "input": "",
            "output": f"{g_str} g = {kg_str} kg",
            "model_response": f"{g_str} grammes correspondent à {kg_str} kilogrammes"
        })

    return examples


def gen_kg_to_g_examples(n: int, seed: int = 43):
    random.seed(seed)
    kg_pool = build_kg_pool(n)

    selected = random.sample(kg_pool, n)
    examples = []

    for kg in selected:
        g = kg * Decimal("1000")

        kg_str = fmt_decimal(kg)
        g_str = fmt_decimal(g)

        examples.append({
            "instruction": f"Convertis {kg_str} kg en g.",
            "input": "",
            "output": f"{kg_str} kg = {g_str} g",
            "model_response": f"{kg_str} kilogrammes correspondent à {g_str} grammes"
        })

    return examples


# ---------- SAVE ----------

def save_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    N = 200  

    g_to_kg = gen_g_to_kg_examples(N, seed=1)
    kg_to_g = gen_kg_to_g_examples(N, seed=2)

    dataset = g_to_kg + kg_to_g
    save_json(dataset, "conversion_ingredients_kg.json")

    print(f"✅ Dataset généré : {len(dataset)} exemples (g→kg={N}, kg→g={N})")
