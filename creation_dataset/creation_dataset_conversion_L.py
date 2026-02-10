import json
import random
from decimal import Decimal, ROUND_HALF_UP

def fmt(x: Decimal) -> str:
    s = format(x.normalize(), "f")
    return "0" if s in ("-0", "-0.0") else s

# ---------- Pools (grands, uniques, avec décimales) ----------

def build_L_pool(max_size: int = 500):
    """
    Valeurs en L: décimales + entiers (0.01 à 5 L) -> pool large.
    On privilégie des décimales "propres" (pas trop de digits).
    """
    pool = set()

    # décimales courantes (en L)
    steps = [Decimal("0.01"), Decimal("0.02"), Decimal("0.05"),
             Decimal("0.1"), Decimal("0.125"), Decimal("0.2"),
             Decimal("0.25"), Decimal("0.5"), Decimal("0.75")]

    # on construit des valeurs jusqu'à ~5 L
    for step in steps:
        for k in range(1, 501):
            val = step * Decimal(k)
            if val <= Decimal("5"):
                pool.add(val)

    # entiers
    for k in range(1, 6):
        pool.add(Decimal(k))

    pool = sorted(pool)
    return pool[:max_size] if len(pool) > max_size else pool


def build_mL_pool(max_size: int = 500):
    """
    Valeurs en mL: 1 à 5000 mL + quelques décimales utiles.
    """
    pool = set(Decimal(i) for i in range(1, 5001))  # 1..5000 mL
    pool = sorted(pool)
    return pool[:max_size] if len(pool) > max_size else pool


def build_cL_pool(max_size: int = 500):
    """
    Valeurs en cL: 1 à 500 cL + quelques décimales.
    """
    pool = set(Decimal(i) for i in range(1, 501))  # 1..500 cL
    pool = sorted(pool)
    return pool[:max_size] if len(pool) > max_size else pool


# ---------- Générateurs SANS répétitions ----------

def gen_L_to_mL(n, seed=1):
    random.seed(seed)
    examples = []

    L_pool = build_L_pool()
    if n > len(L_pool):
        raise ValueError(f"n={n} > pool L disponible ({len(L_pool)})")

    selected_L = random.sample(L_pool, n)

    for L in selected_L:
        mL = (L * Decimal(1000)).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
        examples.append({
            "instruction": f"Convertis {fmt(L)} L en ml.",
            "input": "",
            "output": f"{fmt(L)} L = {fmt(mL)} ml",
            "model_response": f"{fmt(L)} litre correspond à {fmt(mL)} millilitres"
        })
    return examples


def gen_mL_to_L(n, seed=2):
    random.seed(seed)
    examples = []

    mL_pool = build_mL_pool()
    if n > len(mL_pool):
        raise ValueError(f"n={n} > pool mL disponible ({len(mL_pool)})")

    selected_mL = random.sample(mL_pool, n)

    for mL in selected_mL:
        L = (mL / Decimal(1000)).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
        examples.append({
            "instruction": f"Convertis {fmt(mL)} ml en L.",
            "input": "",
            "output": f"{fmt(mL)} ml = {fmt(L)} L",
            "model_response": f"{fmt(mL)} millilitres correspondent à {fmt(L)} litre"
        })
    return examples


def gen_L_to_cL(n, seed=3):
    random.seed(seed)
    examples = []

    L_pool = build_L_pool()
    if n > len(L_pool):
        raise ValueError(f"n={n} > pool L disponible ({len(L_pool)})")

    selected_L = random.sample(L_pool, n)

    for L in selected_L:
        cL = (L * Decimal(100)).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
        examples.append({
            "instruction": f"Convertis {fmt(L)} L en cl.",
            "input": "",
            "output": f"{fmt(L)} L = {fmt(cL)} cl",
            "model_response": f"{fmt(L)} litre correspond à {fmt(cL)} centilitres"
        })
    return examples


def gen_cL_to_L(n, seed=4):
    random.seed(seed)
    examples = []

    cL_pool = build_cL_pool()
    if n > len(cL_pool):
        raise ValueError(f"n={n} > pool cL disponible ({len(cL_pool)})")

    selected_cL = random.sample(cL_pool, n)

    for cL in selected_cL:
        L = (cL / Decimal(100)).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
        examples.append({
            "instruction": f"Convertis {fmt(cL)} cl en L.",
            "input": "",
            "output": f"{fmt(cL)} cl = {fmt(L)} L",
            "model_response": f"{fmt(cL)} centilitres correspondent à {fmt(L)} litre"
        })
    return examples


def gen_mL_to_cL(n, seed=5):
    random.seed(seed)
    examples = []

    mL_pool = build_mL_pool()
    if n > len(mL_pool):
        raise ValueError(f"n={n} > pool mL disponible ({len(mL_pool)})")

    selected_mL = random.sample(mL_pool, n)

    for mL in selected_mL:
        cL = (mL / Decimal(10)).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
        examples.append({
            "instruction": f"Convertis {fmt(mL)} ml en cl.",
            "input": "",
            "output": f"{fmt(mL)} ml = {fmt(cL)} cl",
            "model_response": f"{fmt(mL)} millilitres correspondent à {fmt(cL)} centilitres"
        })
    return examples


def gen_cL_to_mL(n, seed=6):
    random.seed(seed)
    examples = []

    cL_pool = build_cL_pool()
    if n > len(cL_pool):
        raise ValueError(f"n={n} > pool cL disponible ({len(cL_pool)})")

    selected_cL = random.sample(cL_pool, n)

    for cL in selected_cL:
        mL = (cL * Decimal(10)).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
        examples.append({
            "instruction": f"Convertis {fmt(cL)} cl en ml.",
            "input": "",
            "output": f"{fmt(cL)} cl = {fmt(mL)} ml",
            "model_response": f"{fmt(cL)} centilitres correspondent à {fmt(mL)} millilitres"
        })
    return examples


# ---------- Main ----------

if __name__ == "__main__":
    N = 100  # change ici

    dataset = (
        gen_L_to_mL(N) +
        gen_mL_to_L(N) +
        gen_L_to_cL(N) +
        gen_cL_to_L(N) +
        gen_mL_to_cL(N) +
        gen_cL_to_mL(N)
    )

    # Option bonus: dédup globale (au cas où)
    unique = {}
    for ex in dataset:
        key = (ex["instruction"], ex["output"])
        unique[key] = ex
    dataset = list(unique.values())

    with open("conversion_ingredients_litre.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    print(f"OK : {len(dataset)} exemples uniques générés (conversion_ingredients_litre.json)")
