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


def get_helper_prompt(writing_mode: int) -> str:
    helper_prompt = HELPER_PROMPTS.get(f"helper_rule", "")
    format_prompt = HELPER_PROMPTS.get(f"format_rule_{writing_mode}", "")
    print(f"format_rule: {format_prompt}")
    return f"{helper_prompt}\n{format_prompt}"


def get_scoring_prompt(npc_id: str) -> str:
    player_scoring_docs = extract_google_doc_content("player_score")
    npc_scoring_docs = extract_google_doc_content("npc_score")
    scoring_prompt = SCORING_PROMPTS.get(f"scoring_prompt", "")
    extra_requirements = SCORING_PROMPTS.get(f"extra_requirements", {})
    format_prompt = SCORING_PROMPTS.get(f"format_prompt", "")
    weakness_prompt = NPC_PROMPTS.get("npcs", {}).get(npc_id).get("weaknesses", "")

    return (f"{scoring_prompt}\n{extra_requirements}\n{format_prompt}\n"
            f"Here is the scoring metrics document when scoring the player:\n{player_scoring_docs}\n\n"
            f"Here is the scoring metrics document when scoring the npc:\n{npc_scoring_docs}\n\n"
            f"Here are the weaknesses of this NPC {npc_id}:\n{weakness_prompt}")


def get_audience_chat_prompt(audience_type) -> str:
    profile = extract_google_doc_content(audience_type)

    sys_prompt = (f"You are a {audience_type} of Fly Full. Here are the guidelines of how you "
                  f"should reply:\n {profile} \n\nPlease reply in no more than 40 words.")

    return sys_prompt


def get_detect_prompt(npc_id: str) -> str:
    general_prompt = DETECT_PROMPTS.get(f"general_rule", "")
    detect_prompt = DETECT_PROMPTS.get(f"detect_rule", "")
    classify_prompt = DETECT_PROMPTS.get(f"classify_rule", "")
    format_prompt = DETECT_PROMPTS.get(f"format_rule", "")
    weakness_list = NPC_PROMPTS.get("npcs", {}).get(npc_id).get("weaknesses", "")
    likes_list = NPC_PROMPTS.get("npcs", {}).get(npc_id).get("audience_likes", "")
    dislikes_list = NPC_PROMPTS.get("npcs", {}).get(npc_id).get("audience_dislikes", "")

    sys_prompt = (f"{general_prompt}\n"
                  f"Current NPC opponent is: {npc_id}\n"
                  f"Weaknesses list of this NPC opponent: {weakness_list}\n"
                  f"Likes list of the Audience: {likes_list}\n"
                  f"Dislikes list of the Audience: {dislikes_list}\n"
                  f"Now you have 3 lists.\n"
                  f"Step1:{detect_prompt}\n"
                  f"Step2:{classify_prompt}\n"
                  f"When analyzing a text, look for direct or indirect references to any of those weaknesses, "
                  f"likes and dislikes.\n,"
                  f"{format_prompt}\n"
                  f"Now analyze the following text")
    return sys_prompt
