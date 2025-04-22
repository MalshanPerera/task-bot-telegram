import re
from config import nlp


def extract_tasks_from_message(message):
    """Extract tasks from a message using NLP"""
    doc = nlp(message)
    tasks = []

    # Task keywords
    task_keywords = [
        "please",
        "need to",
        "should",
        "must",
        "have to",
        "take",
        "get",
        "make",
        "prepare",
        "create",
        "update",
        "review",
        "check",
        "follow up",
        "send",
        "call",
        "email",
        "contact",
        "schedule",
        "arrange",
        "organize",
        "provide",
        "approve",
        "approval",
        "submit",
        "compile",
        "gather",
        "collect",
        "finish",
    ]

    # Question indicators
    question_task_indicators = [
        "can you",
        "could you",
        "would you",
        "will you",
        "are you able to",
        "would it be possible",
        "is it possible",
        "can u",
        "could u",
    ]

    # Date indicators
    date_indicators = [
        "today",
        "tomorrow",
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "next week",
        "this week",
        "by the end of",
    ]

    for sent in doc.sents:
        sent_text = sent.text.strip()
        if not sent_text:
            continue

        # Convert to lowercase for better matching
        sent_lower = sent_text.lower()

        # Check for tasks using various indicators
        is_task = any(indicator in sent_lower for indicator in question_task_indicators)

        if not is_task:
            is_task = any(keyword in sent_lower for keyword in task_keywords)

        if not is_task:
            tokens = [token for token in sent]
            is_task = (tokens and tokens[0].pos_ == "VERB") or (
                len(tokens) > 1
                and tokens[0].text.lower() in ["i", "we", "you"]
                and tokens[1].pos_ == "VERB"
            )

        if not is_task:
            is_task = any(indicator in sent_lower for indicator in date_indicators)

        if is_task and is_valid_task(sent_text):
            tasks.append(sent_text)

    return tasks


def is_valid_task(text):
    """Check if a text is likely a real task and not just an acknowledgment"""
    # List of common acknowledgments that shouldn't be treated as tasks
    acknowledgments = [
        "noted",
        "ok",
        "okay",
        "got it",
        "thanks",
        "thank you",
        "understood",
        "sure",
        "alright",
        "cool",
        "great",
        "perfect",
        "sounds good",
        "good",
        "fine",
        "agreed",
        "done",
        "yes",
        "yeah",
        "👍",
        "👌",
        "✅",
        "good job",
        "nice",
        "well done",
    ]

    # Clean the text for comparison
    text_lower = text.lower().strip()

    # Check if it's just an acknowledgment
    for ack in acknowledgments:
        if text_lower == ack or text_lower == f"{ack}." or text_lower == f"{ack}!":
            return False

    # Check if it's too short to be a meaningful task (less than 4 words)
    words = [w for w in text_lower.split() if w]
    if len(words) < 4:
        # Short messages are often not tasks unless they contain task indicators
        task_indicators = [
            "please",
            "need",
            "must",
            "should",
            "review",
            "check",
            "do",
            "make",
            "get",
            "prepare",
        ]
        has_indicator = any(indicator in text_lower for indicator in task_indicators)
        if not has_indicator:
            return False

    return True


def find_hidden_tasks(message):
    """Find tasks that span multiple sentences or are otherwise hidden"""
    hidden_tasks = []
    task_sections = re.findall(
        r"(?i)(?:i need you to|please|could you).*?(?:\.|\n|$)", message
    )

    for section in task_sections:
        if section not in hidden_tasks:
            hidden_tasks.append(section.strip())

    return [task for task in hidden_tasks if is_valid_task(task)]
