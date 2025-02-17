# services/prompt_service.py
import json
import os
from services.rag_service import extract_google_doc_content


def load_personality_prompts() -> dict:
    file_path = os.path.join(os.path.dirname(__file__), "../data/prompts.json")
    with open(file_path, "r") as file:
        return json.load(file)


def load_helper_prompts() -> dict:
    file_path = os.path.join(os.path.dirname(__file__), "../data/help_prompts.json")
    with open(file_path, "r") as file:
        return json.load(file)


NPC_PROMPTS = load_personality_prompts()
HELPER_PROMPTS = load_helper_prompts()


def get_combined_prompt(npc_id: str, mode: str) -> str:
    if mode not in ["chat", "battle"]:
        raise ValueError("Mode must be either 'chat' or 'battle'.")

    global_prompt = NPC_PROMPTS.get(f"general_rule", "")

    # Retrieve global instructions.
    mode_prompt = NPC_PROMPTS.get(f"general_{mode}", "")

    # Retrieve the NPC-specific personality.
    npc_prompts = NPC_PROMPTS.get("npcs", {}).get(npc_id)
    if not npc_prompts:
        raise ValueError(f"NPC '{npc_id}' not found.")

    npc_personality = npc_prompts.get(f"{mode}_personality", "")
    profile = extract_google_doc_content(mode)
    # Combine them.
    return f"{global_prompt}\n{mode_prompt}\n{npc_personality}\n{profile}"


def get_helper_prompt() -> str:
    helper_prompt = HELPER_PROMPTS.get(f"helper_rule", "")
    format_prompt = HELPER_PROMPTS.get(f"format_rule", "")
    return f"{helper_prompt}\n{format_prompt}"
