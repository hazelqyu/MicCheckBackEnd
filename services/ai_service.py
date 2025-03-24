from openai import OpenAI
import json
from data.config import OPENAI_API_KEY, OPENAI_MODEL
from services.prompt_service import get_combined_prompt, get_helper_prompt, get_scoring_prompt, get_gossip_prompt, \
    get_detect_prompt
from services.conversation_manager import conversation_manager

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_chat_response(request):
    npc_id = request.npc_id
    conversation_id = request.conversation_id
    user_input = request.user_input
    new_session = request.new_session

    conversation_history = conversation_manager.get_conversation_history(conversation_id)

    if new_session or not conversation_history:
        system_prompt = get_combined_prompt(npc_id, "chat")
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


def generate_fill_in_blank_response(request):
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
                        },
                        "npc_incomplete_bar": {
                            "description": "A string",
                            "type": "string"
                        },
                        "options": {
                            "description": "A list of options related to the task",
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        }
                    },
                    "required": ["npc_full_bar_1", "npc_full_bar_2", "npc_full_bar_3", "npc_full_bar_4",
                                 "npc_incomplete_bar", "options"],
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
    npc_id = request.npc_id
    conversation_id = request.conversation_id
    user_input = request.user_input
    new_session = request.new_session

    conversation_history = conversation_manager.get_conversation_history(conversation_id)

    if new_session or not conversation_history:
        system_prompt = get_helper_prompt()
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
                        "options": {
                            "description": "A list of options related to the task",
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        }
                    },
                    "required": ["incomplete_bars", "options"],
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
                            "description": "An integer",
                            "type": "integer"
                        },
                        "explanation_1": {
                            "description": "A string",
                            "type": "string"
                        },
                        "story_consistency_score": {
                            "description": "An integer",
                            "type": "integer"
                        },
                        "explanation_2": {
                            "description": "A string",
                            "type": "string"
                        },
                        "npc_weakness_score": {
                            "description": "An integer",
                            "type": "integer"
                        },
                        "explanation_3": {
                            "description": "A string",
                            "type": "string"
                        },
                        "audience_preference_score": {
                            "description": "An integer",
                            "type": "integer"
                        },
                        "explanation_4": {
                            "description": "A string",
                            "type": "string"
                        },
                        "prediction": {
                            "description": "An integer",
                            "type": "integer"
                        },
                        "prediction_reason": {
                            "description": "A string",
                            "type": "string"
                        },
                    },
                    "required": ["clarity_score", "story_consistency_score", "npc_weakness_score",
                                 "audience_preference_score", "prediction"],
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


def generate_gossip_response(request):
    conversation_id = request.conversation_id
    user_input = request.user_input
    new_session = request.new_session

    conversation_history = conversation_manager.get_conversation_history(conversation_id)

    if new_session or not conversation_history:
        system_prompt = get_gossip_prompt()
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
                            "description": "True if any weakness was detected in the message, else false."
                        },
                        "highlights": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "list of text fragments to highlight from the message (or empty if none)"
                        },
                        "weaknesses": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Short summary in a couple of words for each detected weaknesses."
                        },
                        "highlight_indices": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "start": {
                                        "type": "integer",
                                        "description": "Start index of the highlight"
                                    },
                                    "end": {
                                        "type": "integer",
                                        "description": "End index of the highlight"
                                    }
                                },
                                "required": ["start", "end"],
                                "additionalProperties": False
                            },
                            "description": "List of highlight ranges with start and end index"
                        }
                    },
                    "required": ["detected", "highlights", "weaknesses", "highlight_indices"],
                    "additionalProperties": False
                }
            }
        }
    )

    raw_reply = response.choices[0].message.content
    return raw_reply
