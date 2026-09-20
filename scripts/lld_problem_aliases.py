"""How the LLD survey agents' names fold into one problem each, and what is out of scope.
Read by design_problem_survey.py --domain low-level-design. BUILD.md explains the judgements."""

import re


def normalise(name: str) -> str:
    """Strip the annotations agents added around a name."""
    m = re.search(r"\*\*(.+?)\*\*", name)                       # (invented: **Chat room**)
    if m:
        name = m.group(1)
    name = re.sub(r"^\((?:new|no fit)[^)]*\)\s*", "", name)      # (new) Kanban board
    name = re.sub(r"\s*\((?:new|concert|dynamic|cloud|Snake-only|collaborative|P2P|billing|payment|Trello)[^)]*\)\s*$", "", name)
    return name.strip()


ALIASES = {
    "Elevator": "Elevator system",
    "Online auction system": "Online auction",
    "Chat application": "Chat room", "Online chat system": "Chat room",
    "Social network-like chat": "Chat room",
    "Order management system": "Online shopping (Amazon)",
    "E-commerce cart and checkout": "Online shopping (Amazon)",
    "Inventory management": "Online shopping (Amazon)",
    "Warehouse management": "Online shopping (Amazon)",
    "Kanban board": "Task management (Trello/Jira)",
    "Kanban board (Trello-like)": "Task management (Trello/Jira)",
    "Task scheduler (Trello/kanban-board variant)": "Task management (Trello/Jira)",
    "Ticketing / issue queue": "Task management (Trello/Jira)",
    "Support-ticket triage": "Task management (Trello/Jira)",
    "Job scheduler": "Task scheduler",
    "LFU cache": "LRU cache",
    "Payment gateway system": "Payment gateway",
    "Thread pool / synchronization primitive": "Thread pool",
    "Event bus": "Pub-sub / message broker",
    "Kafka": "Pub-sub / message broker",
    "Ledger / accounting system": "Bank account system",
    "Multi-player card game framework": "Deck of cards / blackjack",
    "Simplified Twitter feed": "Social network",
    "Coding-judge platform": "Online judge",
    "Online shopping-like judge platform": "Online judge",
    "Property listing site": "Online shopping (Amazon)",
    "Online shopping (Amazon)-like listing site": "Online shopping (Amazon)",
    "Coupon and discount system": "Billing / discount engine",
    "Voting booth system": "Voting system",
    "Snake and ladder (Snake-only variant)": "Snake game",
}

# Prefixes. Another round, or not a design problem.
OUT_OF_SCOPE = (
    "Hash table / dictionary implementation", "Stack and queue", "Shape calculator",   # data-structure exercises
    "Compiler lexer", "Game physics engine", "Entity-component system",                # specialist domains
    "Video conferencing", "Video streaming platform",                                  # system design, not LLD
)
