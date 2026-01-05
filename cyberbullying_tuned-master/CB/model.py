import json
from pathlib import Path
from openai import OpenAI
from resource import RESOURCES

# Read API key from api file
api_key_path = Path("api")
if api_key_path.exists():
    with open(api_key_path, "r") as f:
        api_key = f.read().strip()
    client = OpenAI(api_key=api_key)
else:
    # Fallback to environment variable if api file doesn't exist
    client = OpenAI()

FT_MODEL = "ft:gpt-4o-2024-08-06:personal:cb-final:Chlrmg79"  # your model
LABELS = ["age","ethnicity","not_cyberbullying"]

SYS = ("You classify online messages into one of the following categories: "
       "age, ethnicity, not_cyberbullying."
       "Respond using only the correct label.")

def classify_comment(comment: str) -> str:
    resp = client.chat.completions.create(
        model=FT_MODEL,
        messages=[
            {"role":"system","content":SYS},
            {"role":"user","content":f"Comment: {comment}"}
        ],
        # enforce a clean, single-field JSON response
        response_format={
          "type":"json_schema",
          "json_schema":{
            "name":"classification",
            "schema":{
              "type":"object",
              "properties":{"label":{"type":"string","enum": LABELS}},
              "required":["label"],
              "additionalProperties": False
            }
          }
        }
    )
    return json.loads(resp.choices[0].message.content)["label"]

def stage0_greeting():
    return "Hi, I am a cyberbullying detection agent. How can I help you today?"


def stage1_output(comment: str) -> tuple[str,str,str]:
    label = classify_comment(comment)
    resources = RESOURCES[label]

    message = (
        f'This is "{label}".\n'
        f'Here are articles that may help: {", ".join(resources)}.\n'
    )
    
    return label, resources, message

def generate_peer_rationale(comment: str, label: str, age: int) -> str:
    sys_prompt = (
        f"The user is {age} years old. Always assume the user may come from a diverse cultural background. Avoid cultural assumptions. Avoid references that only apply to one region. Respond in a universal, respectful, culturally-neutral tone. When discussing sensitive topics (gender, age, ethnicity, religion), use inclusive language and avoid stereotypes. If the user appears to be a minor, use simple, supportive, age-appropriate language. Avoid complex emotional vocabulary. Use short sentences and relatable examples. If the user appears older, adapt tone to be more mature and reflective.When generating a response, always begin by acknowledging the likely emotion of the user. Use non-judgmental language. Avoid moralizing. Encourage reflection and self-awareness. Validate emotions but do not validate harmful behavior."
    )

    user_prompt = (
        f"LABEL={label}\n"
        f"COMMENT={comment}\n"
        f"AGE={age}\n"
        f"Explain briefly why this comment is classified as {label}."
    )

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":sys_prompt},
            {"role":"user","content":user_prompt}
        ],
        response_format={
            "type":"json_schema",
            "json_schema":{
                "name": "rationale",
                "schema": {
                    "type":"object",
                    "properties": {
                        "peer_tone_message": {"type":"string"}
                    },
                    "required":["peer_tone_message"],
                    "additionalProperties": False
                }
            }
        }
    )

    return json.loads(resp.choices[0].message.content)["peer_tone_message"]

def human_inthe_loop() -> str:
    """Asks the user for feedback about their interaction with the model"""
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":"You are a friendly assistant asking for user feedback."},
            {"role":"user","content":"Ask the user how their interaction with the cyberbullying detection model was. Ask if you did a good job or if you need to improve in terms of language choice, empathy, etc."}
        ]
    )
    return resp.choices[0].message.content