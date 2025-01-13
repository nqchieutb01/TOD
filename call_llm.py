from utils import get_completion, multi_process_task_dict
import random
TEMPLATE_QUESTION = """
**TASK**: You will be provided with an Wikipedia document, your mission is to generate 5 queries in Vietnamese.
**REQUIREMENT**:
1. The query should be {query_type}, {query_length}, {clarity}, and avoid copying the query verbatim.
2. A query MUST BE a question derived from the document.
3. The response must be solely in the following format without any additional explanation or unnecessary details:
BEGIN
[1]. Query 1
[2]. Query 2
...
[5]. Query 5
END
4. Always begin your response with "BEGIN" and end it with "END".
5. The queries must be written in Vietnamese.
6. The queries and documents require {difficulty} level education to understand. Be creative!
Now generate queries based on the following document:
{{context}}
""".strip()

TEMPLATE_STATEMENT = """
**TASK**: You will be provided with an Wikipedia document, your mission is to generate 5 queries in Vietnamese.
**REQUIREMENT**:
1. The query should be {query_type}, {query_length}, {clarity}, and avoid copying the query verbatim..
2. A query MUST BE a statement (not a question) derived from the document.
3. The response must be solely in the following format without any additional explanation or unnecessary details:
BEGIN
[1]. Query 1
[2]. Query 2
...
[5]. Query 5
END
4. Always begin your response with "BEGIN" and end it with "END".
5. The queries must be written in Vietnamese.
6. The queries and documents require {difficulty} level education to understand. Be creative!
Now generate queries based on the following document:
{{context}}
""".strip()
query_type = ["extremely long-tail", "long-tail", "common"]
query_length = ["less than 5 words", "5 to 15 words", "at least 10 words"]
clarity = ["clear", "understandable with some effort", "ambiguous"]
difficult = ["high school", "college", "PhD"]
def get_long_context():
    a = random.choice(random.choice(reloaded_encoded_dataset['train'])['chunks'])
    while len(a) < 400:
        a = random.choice(random.choice(reloaded_encoded_dataset['train'])['chunks'])
    a = reloaded_encoded_dataset['train'][1236]['chunks'][0]
    return a
context = get_long_context()
# print(context)
TEMPLATES = [TEMPLATE_QUESTION, TEMPLATE_STATEMENT]

def get_random_template():
    TEMPLATE = random.choice(TEMPLATES)
    qt = random.choice(query_type)
    ql = random.choice(query_length)
    cl = random.choice(clarity)
    di = random.choice(difficult)
    TEMPLATE = TEMPLATE.replace("{query_type}", qt)
    TEMPLATE = TEMPLATE.replace("{query_length}", ql)
    TEMPLATE = TEMPLATE.replace("{clarity}", cl)
    TEMPLATE = TEMPLATE.replace("{difficulty}", di)
    return TEMPLATE

TEMPLATE = TEMPLATES[random.choice([0,0,1,1])]
TEMPLATE = TEMPLATE_QUESTION
TEMPLATE = get_random_template()
prompt = TEMPLATE.replace("{{context}}", context)
print(prompt)
# prompt = TEMPLATE_QUESTION.replace("{{context}}", context)
print(get_completion(prompt))
