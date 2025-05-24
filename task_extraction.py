import re


def extract_tasks_from_message(message):
    """Extract tasks from a message by checking if it starts with #"""
    # Split the message into lines to handle multiline messages
    lines = message.strip().split("\n")
    tasks = []

    # Check each line, if it starts with #, it's a task
    for line in lines:
        line = line.strip()
        if line.startswith("#"):
            # Remove the # and any leading whitespace
            task = line[1:].strip()
            if task:  # Make sure there's actual content after the #
                tasks.append(task)

    return tasks


def is_valid_task(text):
    """All tasks starting with # are considered valid"""
    return bool(text.strip())


def find_hidden_tasks(message):
    """
    No hidden tasks in the simplified approach
    All tasks must explicitly start with #
    """
    return []
