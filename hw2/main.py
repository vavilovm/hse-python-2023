from datetime import date
from typing import List

from ast_visualizer.main import create_fib_ast_image


def document_start(title: str, author: str, doc_date: str) -> str:
    return '\n'.join((
        '\\documentclass[12pt]{article}',
        '\\usepackage[utf8]{inputenc}',
        '\\usepackage[english,russian]{babel}',
        '\\usepackage{graphicx}',
        '\\usepackage{amsmath}',
        '\\usepackage[a4paper,left=5mm,right=10mm,top=5mm,bottom=5mm]{geometry}',
        '',
        '\\DeclareMathSymbol{*}{\\mathbin}{symbols}{"01}',
        '',
        f'\\title{{{title}}}',
        f'\\author{{{author}}}',
        f'\\date{{{doc_date}}}',
        '',
        '\\begin{document}',
        '',
        '\\maketitle',
        ''
    ))


def document_end() -> str:
    return '\n\\end{document}'


def latex_table(table: List[list]) -> str:
    def table_format(column_number: int) -> str:
        return 'c | ' * (column_number - 1) + 'c'

    def max_len(t: List[list]) -> int:
        return max(len(x) for x in t)

    cols = max_len(table)
    double_slash = ' \\\\'
    return '\n'.join((
        '\\begin{tabular} ' + f'{{ {table_format(cols)} }}',
        ' \n\\hline\n'.join(map(
            lambda row: ' & '.join(map(str, row)) + ' & ' * (cols - len(row)) + double_slash, table
        )),
        '\\end{tabular}',
    ))


def image(path: str, scale: float = 1) -> str:
    return f'\\includegraphics[scale={scale}]{{{path}}}\\\\'


data = [
    [1, 2, 3, 4, 5, 6],
    ['а', 'б', 'в'],
    ['a', 'b', 'c'],
    ['$x=40$', '$\\implies $', '$\\sqrt{\\dfrac{(3.9*10^5)^2}{2*3.9*10^5}}$']
]


def generate_latex_text():
    return '\n'.join((
        document_start("Title", "Марк Вавилов", date.today().strftime("%B %d %Y")),
        latex_table(data),
        '',
        image('../artifacts/graph.png', scale=0.2),
        document_end()
    ))


if __name__ == "__main__":
    create_fib_ast_image()

    with open('artifacts/file.tex', 'w') as f:
        f.write(generate_latex_text())
