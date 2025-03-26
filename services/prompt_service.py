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


def load_scoring_prompts() -> dict:
    file_path = os.path.join(os.path.dirname(__file__), "../data/score_prompts.json")
    with open(file_path, "r") as file:
        return json.load(file)


def load_detect_prompts() -> dict:
    file_path = os.path.join(os.path.dirname(__file__), "../data/detect_prompts.json")
    with open(file_path, "r") as file:
        return json.load(file)


NPC_PROMPTS = load_personality_prompts()
HELPER_PROMPTS = load_helper_prompts()
SCORING_PROMPTS = load_scoring_prompts()
DETECT_PROMPTS = load_detect_prompts()


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


def get_scoring_prompt(npc_id: str) -> str:
    scoring_docs = extract_google_doc_content("score")
    scoring_prompt = SCORING_PROMPTS.get(f"scoring_prompt", "")
    prediction_prompt = SCORING_PROMPTS.get(f"prediction_prompt", "")
    extra_requirements = SCORING_PROMPTS.get(f"extra_requirements", {})
    format_prompt = SCORING_PROMPTS.get(f"format_prompt", "")
    weakness_prompt = NPC_PROMPTS.get("npcs", {}).get(npc_id).get("weaknesses", "")

    return (f"{scoring_prompt}\n{extra_requirements}\n{prediction_prompt}\n{format_prompt}\n"
            f"Here is the scoring metrics document:\n{scoring_docs}\n\n"
            f"Here are the weaknesses of this NPC {npc_id}:\n{weakness_prompt}")


def get_gossip_prompt() -> str:
    bystander = extract_google_doc_content("bystander")
    fan = extract_google_doc_content("fan")

    return (f"You might be a bystander of Fly Gull or you might be a fan. Here are the guidelines of how you should "
            f"reply.\n If you are a bystander:\n{bystander}\nIf you are a fan:\n{fan}")


def get_detect_prompt(npc_id: str) -> str:
    detect_prompt = DETECT_PROMPTS.get(f"detect_rule", "")
    format_prompt = DETECT_PROMPTS.get(f"format_rule", "")
    weakness_prompt = NPC_PROMPTS.get("npcs", {}).get(npc_id).get("weaknesses", "")

    sys_prompt = (f"{detect_prompt}\n"
                  f"Current NPC opponent is: {npc_id}\n"
                  f"Weaknesses list of this NPC opponent: {weakness_prompt}\n"
                  f"When analyzing a text, look for direct or indirect references to any of those weaknesses, "
                  f"and highlight the relative text fragments.\n"
                  f"{format_prompt}\n"
                  f"Now analyze the following text")
    return sys_prompt
