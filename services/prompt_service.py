# services/prompt_service.py
import json
import os
from services.rag_service import extract_google_doc_content


def load_chat_prompts() -> dict:
    file_path = os.path.join(os.path.dirname(__file__), "../data/chat_prompts.json")
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


def load_battle_prompts() -> dict:
    file_path = os.path.join(os.path.dirname(__file__), "../data/battle_prompts.json")
    with open(file_path, "r") as file:
        return json.load(file)


def load_npc_info() -> dict:
    file_path = os.path.join(os.path.dirname(__file__), "../data/npc_info.json")
    with open(file_path, "r") as file:
        return json.load(file)


CHAT_PROMPTS = load_chat_prompts()
HELPER_PROMPTS = load_helper_prompts()
SCORING_PROMPTS = load_scoring_prompts()
DETECT_PROMPTS = load_detect_prompts()
BATTLE_PROMPTS = load_battle_prompts()

NPC_INFO = load_npc_info()


def get_battle_prompt(npc_id: str) -> str:
    battle_rule = BATTLE_PROMPTS.get(f"battle_rule", "")
    format_rule = BATTLE_PROMPTS.get(f"format_rule", "")

    battle_profile = extract_google_doc_content("battle")

    return f"{battle_rule}\n{format_rule}\nCharacter Profile:\n{battle_profile}"


def get_chat_prompt(npc_id: str, target_type) -> str:
    chat_rule = CHAT_PROMPTS.get(f"chat_rule", "")
    format_rule = CHAT_PROMPTS.get(f"format_rule", "")

    chat_profile = extract_google_doc_content(target_type)

    return f"{chat_rule}\n{format_rule}\nCharacter Profile:\n{chat_profile}"


def get_helper_prompt(npc_id: str,writing_mode: int) -> str:
    helper_rule = HELPER_PROMPTS.get(f"helper_rule", "")
    format_rule = HELPER_PROMPTS.get(f"format_rule_{writing_mode}", "")

    weaknesses = NPC_INFO.get(npc_id).get("weaknesses", "")
    audience_likes = NPC_INFO.get(npc_id).get("audience_likes", "")
    audience_dislikes = NPC_INFO.get(npc_id).get("audience_dislikes", "")
    return (f"{helper_rule}\n\n{format_rule}\n\n"
            # f"Just for you to understand the user's message, here are some context for you, but don't use the context "
            # f"to write lyrics directly, it's only for you to understand better what the user is talking about.\n\n"
            # f"Here are the weaknesses of the opponent in the rap battle {npc_id}:\n{weaknesses}\n\n"
            # f"Here are the audience preferences:\n{audience_likes}\n\n{audience_dislikes}"
            )


def get_scoring_prompt(npc_id: str) -> str:
    player_scoring_docs = extract_google_doc_content("player_score")
    npc_scoring_docs = extract_google_doc_content("npc_score")
    scoring_prompt = SCORING_PROMPTS.get(f"scoring_prompt", "")
    extra_requirements = SCORING_PROMPTS.get(f"extra_requirements", {})
    format_prompt = SCORING_PROMPTS.get(f"format_prompt", "")

    weaknesses = NPC_INFO.get(npc_id).get("weaknesses", "")
    audience_likes = NPC_INFO.get(npc_id).get("audience_likes", "")
    audience_dislikes = NPC_INFO.get(npc_id).get("audience_dislikes", "")

    return (
        f"{scoring_prompt}\n"
        f"{extra_requirements}\n"
        f"\nHere are examples of scoring 'npc_weakness_score' correctly:\n"
        f"Example 1:\n"
        f"NPC Weakness: 'Is bad at flying and often crashes her bike.'\n"
        f"Player Rap: 'Fly Gull soaring high? Nah, crash-landed on her pride.'\n"
        f"→ Counts as a weakness mention (indirectly mocks her flying skills).\n\n"

        f"Example 2:\n"
        f"NPC Weakness: 'Misses french fries since she gave them up for a celebrity diet.'\n"
        f"Player Rap: 'Starvin’ for clout and fries, girl can’t even munch right.'\n"
        f"→ Counts as a weakness mention (referencing food deprivation).\n\n"

        f"Example 3:\n"
        f"NPC Weakness: 'Has gifted kid syndrome and doesn’t know she’s basic.'\n"
        f"Player Rap: 'Think you’re special, but you're basic in disguise.'\n"
        f"→ Counts as a weakness mention (implies her delusion and lack of self-awareness).\n\n"

        f"Example 4:\n"
        f"Player Rap: 'You're trash, irrelevant, and out of time.'\n"
        f"→ Does **not** count as a weakness mention (too generic, no connection to specific weaknesses).\n\n"

        f"{format_prompt}\n"
        f"Here is the scoring metrics document when scoring the player:\n{player_scoring_docs}\n\n"
        f"Here is the scoring metrics document when scoring the npc:\n{npc_scoring_docs}\n\n"
        f"Here are the weaknesses of this NPC {npc_id}:\n{weaknesses}\n\n"
        f"Here are the audience preferences:\n{audience_likes}\n\n{audience_dislikes}"
    )


def get_detect_prompt(npc_id: str) -> str:
    general_prompt = DETECT_PROMPTS.get(f"general_rule", "")
    detect_prompt = DETECT_PROMPTS.get(f"detect_rule", "")
    classify_prompt = DETECT_PROMPTS.get(f"classify_rule", "")
    format_prompt = DETECT_PROMPTS.get(f"format_rule", "")
    weakness_list = NPC_INFO.get(npc_id).get("weaknesses", "")
    likes_list = NPC_INFO.get(npc_id).get("audience_likes", "")
    dislikes_list = NPC_INFO.get(npc_id).get("audience_dislikes", "")

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
