# Boolean Query Engine with Nested Expressions

A simple Boolean Information Retrieval system implemented in Python. It builds a manual inverted index, supports AND/OR/NOT with linear merge, and evaluates nested Boolean queries using a precedence-aware parser.

DEMO LINK: https://1drv.ms/v/c/5e8c01ca57dca050/IQBjI_e-DPpkSYRmtAHOvTS6AfZzkSs35RxOtB5ryTGIAIw?e=PG2Bl3

## Features
- Manual document collection
- Inverted index (term -> sorted doc IDs)
- Boolean operators: AND, OR, NOT
- Parentheses and nested expressions
- Graceful handling of invalid queries

## Files
- `boolean_query_engine.py` – single-file Python implementation
- `boolean_query_engine.ipynb` / `boolean_query_engine_project.ipynb` – Jupyter notebooks

## Run
```bash
python boolean_query_engine.py
```

Then enter a query like:
```
(data AND science) NOT physics
```
