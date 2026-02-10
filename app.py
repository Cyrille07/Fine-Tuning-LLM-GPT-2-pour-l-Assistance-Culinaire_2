from pathlib import Path
from flask import Flask, render_template, request, jsonify
import torch
import tiktoken

from previous_labs import GPTModel, generate, text_to_token_ids, token_ids_to_text

app = Flask(__name__)

BASE_CONFIG = {
    "vocab_size": 50257,
    "context_length": 1024,
    "drop_rate": 0.0,
    "qkv_bias": True
}

MODEL_CONFIGS = {
    "gpt2-small (124M)": {"emb_dim": 768, "n_layers": 12, "n_heads": 12},
    "gpt2-medium (355M)": {"emb_dim": 1024, "n_layers": 24, "n_heads": 16},
    "gpt2-large (774M)": {"emb_dim": 1280, "n_layers": 36, "n_heads": 20},
    "gpt2-xl (1558M)": {"emb_dim": 1600, "n_layers": 48, "n_heads": 25},
}

CKPT_PATH = "LLM_assistant_cuisine-sft.pth"
CHOOSE_MODEL = "gpt2-medium (355M)"

def build_prompt(instruction: str) -> str:
    return (
        "Below is an instruction that describes a task. Write a response "
        "that appropriately completes the request.\n\n"
        "### Instruction:\n"
        f"{instruction.strip()}\n\n"
        "### Response:\n"
    )

def extract_response(full_text: str, prompt: str) -> str:
    completion = full_text[len(prompt):].strip()
    for stop in ["\n\n### Instruction:", "\n\n### Input:", "\n\n### Response:"]:
        if stop in completion:
            completion = completion.split(stop, 1)[0].strip()
    return completion

# --- Load model once (au démarrage) ---
device = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = tiktoken.get_encoding("gpt2")

ckpt = Path(CKPT_PATH)
if not ckpt.exists():
    raise FileNotFoundError(f"Checkpoint introuvable: {CKPT_PATH}")

cfg = dict(BASE_CONFIG)
cfg.update(MODEL_CONFIGS[CHOOSE_MODEL])

model = GPTModel(cfg).to(device)
state = torch.load(CKPT_PATH, map_location=device)
model.load_state_dict(state)
model.eval()

@torch.no_grad()
def run_generation(instruction: str, max_new_tokens: int = 60, seed: int | None = 123) -> str:
    instruction = (instruction or "").strip()
    if not instruction:
        return ""

    prompt = build_prompt(instruction)

    if seed is not None:
        torch.manual_seed(int(seed))

    idx = text_to_token_ids(prompt, tokenizer).to(device)

    token_ids = generate(
        model=model,
        idx=idx,
        max_new_tokens=int(max_new_tokens),
        context_size=BASE_CONFIG["context_length"],
        eos_id=50256
    )

    full_text = token_ids_to_text(token_ids.detach().cpu(), tokenizer)
    return extract_response(full_text, prompt)

# --- Routes ---
@app.get("/")
def home():
    return render_template("index.html")

@app.post("/api/generate")
def api_generate():
    data = request.get_json(force=True) or {}
    instruction = data.get("instruction", "")
    max_new_tokens = int(data.get("max_new_tokens", 60))
    seed = data.get("seed", 123)
    seed = None if seed in ["", None] else int(seed)

    # petite sécurité sur les bornes
    max_new_tokens = max(1, min(max_new_tokens, 400))

    try:
        result = run_generation(instruction, max_new_tokens, seed)
        return jsonify({"ok": True, "response": result})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

if __name__ == "__main__":
    # http://127.0.0.1:7860
    app.run(host="0.0.0.0", port=7860, debug=True)
