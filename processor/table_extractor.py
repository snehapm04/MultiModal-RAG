import camelot
import os

def extract_tables(pdf_path, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    tables = camelot.read_pdf(pdf_path, pages="all")

    results = []
    for i, t in enumerate(tables):
        path = f"{out_dir}/table{i}.csv"
        t.df.to_csv(path, index=False)
        results.append(path)

    return results
