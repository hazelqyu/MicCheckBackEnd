from openai import OpenAI
import json
from data.config import OPENAI_API_KEY, OPENAI_MODEL
from services.prompt_service import get_combined_prompt, get_helper_prompt
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
        response_format={"type": "json_object"}
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
