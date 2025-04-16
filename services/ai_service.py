from openai import OpenAI
import json
from data.config import OPENAI_API_KEY, OPENAI_MODEL
from services.prompt_service import get_combined_prompt, get_helper_prompt, get_scoring_prompt, \
    get_audience_chat_prompt, \
    get_detect_prompt
from services.conversation_manager import conversation_manager

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_chat_response(request):
    target_type = request.target_type
    npc_id = request.chat_target_id
    conversation_id = request.conversation_id
    user_input = request.user_input
    new_session = request.new_session

    conversation_history = conversation_manager.get_conversation_history(conversation_id)

    if new_session or not conversation_history:
        if target_type == "rapper":
            system_prompt = get_combined_prompt(npc_id, "chat")
        else:
            system_prompt = get_audience_chat_prompt(target_type)
        system_message = {"role": "system", "content": system_prompt}
        conversation_manager.update_conversation_history(conversation_id, system_message)

    if user_input:
        user_message = {"role": "user", "content": user_input}
        conversation_manager.update_conversation_history(conversation_id, user_message)

    messages = conversation_manager.get_conversation_history(conversation_id)

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=0.8
    )

    raw_reply = response.choices[0].message.content
    npc_message = {"role": "assistant", "content": raw_reply}
    conversation_manager.update_conversation_history(conversation_id, npc_message)

    return raw_reply


def generate_gossip_response(request):
    print("Wrong function to call")
    return


def generate_battle_response(request):
    npc_id = request.npc_id
    conversation_id = request.conversation_id
    user_input = request.user_input
    new_game = request.new_game

    conversation_history = conversation_manager.get_conversation_history(conversation_id)

    if new_game or not conversation_history:
        system_prompt = get_combined_prompt(npc_id, "battle")
        system_message = {"role": "system", "content": system_prompt}
        conversation_manager.update_conversation_history(conversation_id, system_message)

    if user_input:
        user_message = {"role": "user", "content": user_input}
        conversation_manager.update_conversation_history(conversation_id, user_message)

    messages = conversation_manager.get_conversation_history(conversation_id)

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=0.8,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "help_response_schema",
                "schema": {
                    "type": "object",
                    "properties": {
                        "npc_full_bar_1": {
                            "description": "A string",
                            "type": "string"
                        },
                        "npc_full_bar_2": {
                            "description": "A string",
                            "type": "string"
                        },
                        "npc_full_bar_3": {
                            "description": "A string",
                            "type": "string"
                        },
                        "npc_full_bar_4": {
                            "description": "A string",
                            "type": "string"
                        }
                    },
                    "required": ["npc_full_bar_1", "npc_full_bar_2", "npc_full_bar_3", "npc_full_bar_4"],
                    "additionalProperties": False
                }
            }
        }
    )

    # Extract the raw AI reply
    raw_reply = response.choices[0].message.content
    npc_message = {"role": "assistant", "content": raw_reply}
    conversation_manager.update_conversation_history(conversation_id, npc_message)

    return raw_reply


def generate_help_response(request):
    writing_mode = request.writing_mode
    npc_id = request.npc_id
    conversation_id = request.conversation_id
    user_input = request.user_input
    new_session = request.new_session

    conversation_history = conversation_manager.get_conversation_history(conversation_id)

    system_prompt = get_helper_prompt(writing_mode)
    system_message = {"role": "system", "content": system_prompt}
    conversation_manager.update_conversation_history(conversation_id, system_message)

    if user_input:
        user_message = {"role": "user", "content": user_input}
        conversation_manager.update_conversation_history(conversation_id, user_message)

    messages = conversation_manager.get_conversation_history(conversation_id)

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=0.8,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "help_response_schema",
                "schema": {
                    "type": "object",
                    "properties": {
                        "incomplete_bar_1": {
                            "description": "A string",
                            "type": "string"
                        },
                        "incomplete_bar_2": {
                            "description": "A string",
                            "type": "string"
                        },
                        "incomplete_bar_3": {
                            "description": "A string",
                            "type": "string"
                        },
                        "incomplete_bar_4": {
                            "description": "A string",
                            "type": "string"
                        },
                    },
                    "required": ["incomplete_bars"],
                    "additionalProperties": False
                }
            }
        }
    )

    raw_reply = response.choices[0].message.content
    npc_message = {"role": "assistant", "content": raw_reply}
    conversation_manager.update_conversation_history(conversation_id, npc_message)

    return raw_reply


def generate_score_response(request):
    npc_id = request.npc_id
    player_id = request.player_id
    conversation_id = request.conversation_id
    scoree = request.scoree
    rap_lyrics = request.rap_lyrics

    system_prompt = get_scoring_prompt(npc_id)
    system_message = {"role": "system", "content": system_prompt}

    history = conversation_manager.get_conversation_history(conversation_id)
    round_prompt = (f"This is a rap battle between the NPC: {npc_id} and the player: {player_id}! "
                    f"You are going to score the {scoree}'s rap in this round, "
                    f"which is as follows:\n{rap_lyrics}. "
                    f"\n\nAnd Here is the scoring history in this battle for your reference:\n{history}")
    user_message = {"role": "user", "content": round_prompt}
    messages = [system_message, user_message]
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=0.8,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "score_response_schema",
                "schema": {
                    "type": "object",
                    "properties": {
                        "clarity_score": {
                            "description": "An integer between 0 and 10",
                            "type": "integer"
                        },
                        "story_consistency_score": {
                            "description": "An integer between 0 and 10",
                            "type": "integer"
                        },
                        "cleverness_score": {
                            "description": "An integer between 0 and 10",
                            "type": "integer"
                        },
                        "npc_weakness_score": {
                            "description": "An integer between 0 and 30",
                            "type": "integer"
                        },
                        "rhyming_ability_score": {
                            "description": "An integer between 0 and 30",
                            "type": "integer"
                        },
                        "audience_preference_score": {
                            "description": "An integer between 0 and 30",
                            "type": "integer"
                        },
                        "comment": {
                            "description": "A string",
                            "type": "string"
                        },
                    },
                    "required": ["clarity_score", "story_consistency_score", "cleverness_score", "npc_weakness_score",
                                 "rhyming_ability_score", "audience_preference_score", "comment"],
                    "additionalProperties": False
                }
            }
        }
    )
    raw_reply = response.choices[0].message.content
    update_rap = {"role": "user", "content": f"{scoree}:{rap_lyrics}"}
    conversation_manager.update_conversation_history(conversation_id, update_rap)
    score_message = {"role": "assistant", "content": raw_reply}
    conversation_manager.update_conversation_history(conversation_id, score_message)

    return raw_reply


def generate_detect_response(request):
    npc_id = request.npc_id
    input_text = request.input_text

    system_prompt = get_detect_prompt(npc_id)
    system_message = {"role": "system", "content": system_prompt}
    user_message = {"role": "user", "content": input_text}
    messages = [system_message, user_message]

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=0.8,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "detect_response_schema",
                "schema": {
                    "type": "object",
                    "properties": {
                        "detected": {
                            "type": "boolean",
                            "description": "True if any weakness, like, or dislike is detected in the message; false "
                                           "otherwise."
                        },
                        "highlights": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "A list of short text fragments to highlight in the message (or an empty "
                                           "list if none)."
                        },
                        "summaries": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "A list of short summaries (a couple of words) of each detected weakness, "
                                           "like, or dislike (or an empty list if none)."
                        },
                        "categories": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "A list if the categories of each detected piece of information. Each "
                                           "category must be either 'weaknesses', 'likes', or 'dislikes' (or an empty "
                                           "list if none)."
                        },
                        "indices": {
                            "type": "array",
                            "items": {
                                "type": "integer"
                            },
                            "description": "A list of the indices (starting at 0) of each detected piece of "
                                           "information in its corresponding category list (or an empty list if none)."
                        }
                    },
                    "required": ["detected", "highlights", "summaries", "categories", "indices"],
                    "additionalProperties": False
                }
            }
        }
    )

    raw_reply = response.choices[0].message.content
    return raw_reply
