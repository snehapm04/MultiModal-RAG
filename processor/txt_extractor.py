def extract_text(doc):
    pages = []
    for i, page in enumerate(doc):
        pages.append((i, page.get_text()))
    return pages
