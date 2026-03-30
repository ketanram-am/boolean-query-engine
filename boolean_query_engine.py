# Boolean Query Engine with Nested Expressions
# Information Retrieval Assignment

# -----------------------------
# Document Collection (Manual)
# -----------------------------
# Each document is a short string of terms.
documents = {
    1: "data science machine learning",
    2: "physics chemistry science",
    3: "biology genetics evolution",
    4: "data mining big data",
    5: "science data analytics",
    6: "chemistry organic inorganic",
    7: "machine learning deep learning",
    8: "physics quantum mechanics",
    9: "statistics probability data",
    10: "genetics biology molecular",
    11: "information retrieval search engine",
    12: "data science visualization",
    13: "astronomy physics space",
    14: "neural networks machine learning",
    15: "data science machine learning statistics",
    16: "biology ecology environment",
    17: "chemistry physics materials",
    18: "data science artificial intelligence",
    19: "probability statistics mathematics",
    20: "information science data"
}

# ---------------------------------
# Inverted Index Creation (Manual)
# ---------------------------------
# Build a dictionary: term -> sorted list of document IDs.
inverted_index = {}
for doc_id, text in documents.items():
    terms = text.lower().split()
    for term in terms:
        if term not in inverted_index:
            inverted_index[term] = []
        inverted_index[term].append(doc_id)

# Ensure each posting list is sorted and unique
for term in inverted_index:
    inverted_index[term] = sorted(set(inverted_index[term]))

# -----------------
# Print the index
# -----------------
print("Inverted Index:")
for term in sorted(inverted_index.keys()):
    print(f"{term} -> {inverted_index[term]}")

# -------------------------------
# Boolean Operations (Linear Merge)
# -------------------------------
# AND: Intersection of two sorted lists

def intersect(list1, list2):
    result = []
    i = 0
    j = 0
    while i < len(list1) and j < len(list2):
        if list1[i] == list2[j]:
            result.append(list1[i])
            i += 1
            j += 1
        elif list1[i] < list2[j]:
            i += 1
        else:
            j += 1
    return result

# OR: Union of two sorted lists

def union(list1, list2):
    result = []
    i = 0
    j = 0
    while i < len(list1) and j < len(list2):
        if list1[i] == list2[j]:
            result.append(list1[i])
            i += 1
            j += 1
        elif list1[i] < list2[j]:
            result.append(list1[i])
            i += 1
        else:
            result.append(list2[j])
            j += 1
    # Append remaining elements
    while i < len(list1):
        result.append(list1[i])
        i += 1
    while j < len(list2):
        result.append(list2[j])
        j += 1
    return result

# NOT: Difference from universal set

def difference(universal, exclude_list):
    result = []
    i = 0
    j = 0
    while i < len(universal) and j < len(exclude_list):
        if universal[i] == exclude_list[j]:
            i += 1
            j += 1
        elif universal[i] < exclude_list[j]:
            result.append(universal[i])
            i += 1
        else:
            j += 1
    # Append remaining elements from universal
    while i < len(universal):
        result.append(universal[i])
        i += 1
    return result

# ---------------------
# Tokenizer for queries
# ---------------------

def tokenize(query):
    tokens = []
    current = ""
    for ch in query:
        if ch.isspace():
            if current:
                tokens.append(current)
                current = ""
        elif ch == '(' or ch == ')':
            if current:
                tokens.append(current)
                current = ""
            tokens.append(ch)
        else:
            current += ch
    if current:
        tokens.append(current)
    return tokens

# ------------------------
# Recursive Descent Parser
# ------------------------
# Grammar (with precedence):
# expr   -> or_expr
# or_expr -> and_expr (OR and_expr)*
# and_expr -> not_expr (AND not_expr)*
# not_expr -> NOT not_expr | term
# term -> WORD | '(' expr ')'

class Parser:
    def __init__(self, tokens, index, universal_set):
        self.tokens = tokens
        self.pos = 0
        self.index = index
        self.universal = universal_set

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self, expected=None):
        token = self.current_token()
        if expected is None or token == expected:
            self.pos += 1
            return token
        return None

    def parse(self):
        result = self.parse_or()
        if result is None:
            return None
        if self.current_token() is not None:
            return None
        return result

    # OR level
    def parse_or(self):
        left = self.parse_and()
        if left is None:
            return None
        while True:
            token = self.current_token()
            if token == "OR":
                self.consume("OR")
                right = self.parse_and()
                if right is None:
                    return None
                left = union(left, right)
            else:
                break
        return left

    # AND level
    def parse_and(self):
        left = self.parse_not()
        if left is None:
            return None
        while True:
            token = self.current_token()
            if token == "AND":
                self.consume("AND")
                right = self.parse_not()
                if right is None:
                    return None
                left = intersect(left, right)
            else:
                break
        return left

    # NOT level
    def parse_not(self):
        token = self.current_token()
        if token == "NOT":
            self.consume("NOT")
            operand = self.parse_not()
            if operand is None:
                return None
            return difference(self.universal, operand)
        return self.parse_term()

    # Term level
    def parse_term(self):
        token = self.current_token()
        if token is None:
            return None
        if token == '(':
            self.consume('(')
            inner = self.parse_or()
            if inner is None:
                return None
            if self.current_token() != ')':
                return None
            self.consume(')')
            return inner
        if token in ("AND", "OR", "NOT", ")"):
            return None

        # WORD term: fetch posting list, default to empty if not in index
        self.consume()
        word = token.lower()
        return self.index.get(word, [])

# -----------------------
# Query Processing Driver
# -----------------------

universal_set = sorted(documents.keys())

query = input("Enter Boolean Query: ")
print(f"Query: {query}")

raw_tokens = tokenize(query)
# Normalize operators to uppercase
normalized = []
for t in raw_tokens:
    if t.upper() in ("AND", "OR", "NOT"):
        normalized.append(t.upper())
    else:
        normalized.append(t)

parser = Parser(normalized, inverted_index, universal_set)
result = parser.parse()

if result is None:
    print("Invalid Query")
else:
    print(f"Matching Documents: {result}")
