from typing import Dict, List, Tuple

# Example data structure:
# Each translation is a dictionary where keys are references like 'Book Chapter:Verse'
# and values are the corresponding text in Japanese.
japan_bibles = {
    "meiji": {
        "John 3:16": "神は、そのひとり子を賜うほどにこの世を愛し給えり...",
        "Psalm 23:1": "主はわが牧者なり...",
        # ...
    },
    "shinkai": {
        "John 3:16": "神は実に、そのひとり子をお与えになったほどに世を愛された...",
        "Psalm 23:1": "主は私の羊飼い。私は乏しいことがありません...",
        # ...
    },
}


def parse_reference(ref: str) -> List[Tuple[str, int]]:
    """
    Parse a reference string into a list of (book_chapter, verse) tuples.
    Supports single verses ('John 3:16'), ranges ('John 3:16-18'),
    and multiple references separated by commas ('John 3:16-18, Psalm 23:1-3').
    """
    results = []
    for part in ref.split(","):
        part = part.strip()
        if "-" in part:  # range
            book_chapter, verse_range = part.split(":")
            start, end = map(int, verse_range.split("-"))
            for verse in range(start, end + 1):
                results.append((book_chapter, verse))
        else:  # single verse
            book_chapter, verse = part.split(":")
            results.append((book_chapter, int(verse)))
    return results


def compare_translations(reference: str, translations: Dict[str, Dict[str, str]]) -> Dict[str, List[str]]:
    """
    Compare a verse or verse range across translations.

    :param reference: e.g. "John 3:16" or "Psalm 23:1-3"
    :param translations: dict like {"meiji": {...}, "shinkai": {...}}
    :return: dict mapping translation name to list of verse texts
    """
    verses = parse_reference(reference)
    results = {}
    for name, bible in translations.items():
        texts = []
        for book_chapter, verse in verses:
            key = f"{book_chapter}:{verse}"
            texts.append(bible.get(key, "[未翻訳]"))
        results[name] = texts
    return results


if __name__ == "__main__":
    reference = "John 3:16, Psalm 23:1-3"  # Example mixed reference
    comparison = compare_translations(reference, japan_bibles)

    for translation, texts in comparison.items():
        print(f"\n--- {translation.upper()} ---")
        for verse_text in texts:
            print(verse_text)
