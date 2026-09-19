"""Provide the shared five-label instruction and JSON validation for annotation scripts."""

import json


LABEL_DEFINITIONS = {
    "Conspiracy": "Attributes complex events to secret plots, rejects mainstream information, or frames events as elite deception.",
    "Sensationalism": "Uses exaggerated or dramatic language, shock or fear appeals, oversimplification, or clickbait-style framing.",
    "Hate_Speech": "Incites discrimination, defamation, hostility, or violence based on identity, or makes false reputation-damaging claims.",
    "Speculation": "Circulates unverified political claims, often amplified through partisan or ideological framing.",
    "Satire": "Uses humor, political satire, or internet memes to comment on politics.",
}


def annotation_messages(post_text: str) -> list[dict[str, str]]:
    LLM_prompt = f"""
    Your task is to accurately classify social media posts related to the U.S. Presidential Election.
    Determine whether the given post falls into one or more of the following categories: Conspiracy, Sensationalism, Hate Speech, Speculation, and Satire.
    Use the detailed definitions provided for each category and respond with **True** or **False** for each category only.

    Categories:  
    "Conspiracy": "Simplifies complex events by attributing them to secret plots, rejects mainstream information, forms closed belief communities, replaces science with alternative explanations, or frames events as elite deception.",
    "Sensationalism": "Uses exaggerated or dramatic language, shock and fear appeal, oversimplifies issues, or employs clickbait-style framing to increase engagement.",
    "Hate Speech": "Contains incitement of discrimination, defamation, hostility, or violence based on identity, or makes false statements that damage a person’s reputation (libel/slander).",
    "Speculation": "Speculative ClaimsCirculates unverified claims for political advantage, driven by partisan interests, amplified in ideological echo chambers, and sustains political controversy.",
    "Satire": "Uses humor, political stsatire, and internet memes to criticize or comment on politics, often spreading through viral online platforms."
    
    Post: 
    "{post_text}"     
    """
    return [
        {"role": "user", "content": LLM_prompt},
    ]


def annotation_prompt(post_text: str) -> str:
    return "\n\n".join(message["content"] for message in annotation_messages(post_text))


def annotation_row(identifier: object, response_text: str) -> dict[str, object]:
    response = json.loads(response_text)
    row: dict[str, object] = {"id": identifier}
    for label in LABEL_DEFINITIONS:
        value = response.get(label, response.get(label.replace("_", " "), False))
        row[label] = int(bool(value))
    return row
