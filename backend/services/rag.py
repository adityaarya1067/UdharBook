def build_context(transactions, notes):
    context = "TRANSACTIONS:\n"

    if transactions:
        for t in transactions:
            context += (
                f"- Name: {t['name']}, "
                f"Type: {t['type']}, "
                f"Amount: ₹{t['amount']}, "
                f"Relation: {t['relation']}, "
                f"Date: {t['date']}\n"
            )
    else:
        context += "No transactions found.\n"

    context += "\nNOTES:\n"

    if notes:
        for n in notes:
            context += f"- Title: {n['title']}, Content: {n['content']}\n"
    else:
        context += "No notes found.\n"

    return context
