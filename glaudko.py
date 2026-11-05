"""Мини-проверка кадров Glaudko: разбор и валидация одной строки.

Формат: ОТ>КОМУ|текст[|ключ=значение ...]
Запуск самопроверки: python glaudko.py
"""

SPECIAL = {"ALL", "HUMAN"}


def parse(line):
    """Возвращает dict(frm, to, text, fields) или бросает ValueError."""
    if "\n" in line.strip():
        raise ValueError("кадр должен быть одной строкой")
    parts = line.strip().split("|")
    if len(parts) < 2:
        raise ValueError("нет знака | между адресами и текстом")
    head, text, rest = parts[0], parts[1], parts[2:]
    if head.count(">") != 1:
        raise ValueError("в начале должно быть ОТ>КОМУ")
    frm, to = (x.strip() for x in head.split(">"))
    if not frm or not to:
        raise ValueError("пустое имя отправителя или адресата")
    if frm in SPECIAL:
        raise ValueError("ALL и HUMAN не могут быть отправителем")
    if not text.strip():
        raise ValueError("пустой текст")
    fields = {}
    for p in rest:
        if "=" not in p:
            raise ValueError("поле должно быть ключ=значение: " + repr(p))
        k, v = p.split("=", 1)
        fields[k.strip()] = v.strip()
    return {"frm": frm, "to": to, "text": text.strip(), "fields": fields}


if __name__ == "__main__":
    good = [
        "GROQ>GEMINI|wall ahead; go west",
        "GEMINI>ALL|north blocked; need alt route|x=3|y=5",
        "OR>GROQ|ok",
        "GROQ>HUMAN|Впереди стена, поэтому поворачиваю на запад.",
    ]
    bad = ["hello", "GROQ>GEMINI", "GROQ>GEMINI|a|b", "ALL>GROQ|hi", "GROQ>|x"]
    for g in good:
        parse(g)
    for b in bad:
        try:
            parse(b)
        except ValueError:
            continue
        raise SystemExit("ошибка: должен был отклониться " + repr(b))
    print("ok: %d верных кадров принято, %d неверных отклонено" % (len(good), len(bad)))
