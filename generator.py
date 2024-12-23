import random
import os
import getopt
import string
import sys
import json


def genera_test(template: dict, questions: dict, use_shuffle: bool = False) -> list:

    quiz = []
    topics = list(template.keys())

    for topic in topics:
        count: int = template[topic]

        available_q = questions[topic]
        indices = list(range(len(available_q)))
        random.shuffle(indices)
        indices = indices[0:count]

        for i in indices:
            q: dict = available_q[i]

            if "options" in q:
                order_options = list(range(len(q["options"])))
                random.shuffle(order_options)

                new_answer = order_options[q["answer"]]
                new_options = [q["options"][j] for j in order_options]

                quiz.append({
                    "question": q["question"],
                    "options": new_options,
                    "answer": new_answer
                })
            elif "subquestions" in q:
                quiz.append({
                    "question": q["question"],
                    "subquestions": q["subquestions"],
                    "answer": q["answer"]
                })
            else:
                quiz.append({
                    "question": q["question"],
                    "answer": q["answer"]
                })
    if (use_shuffle):
        random.shuffle(quiz)
    return quiz


def export_quiz(quiz_list: list[list[dict]], output_file: str, doc_template: str, content_template: str, add_solution: bool = False):

    alph_vect = string.ascii_uppercase

    quiz_content_list = []
    for i, quiz in enumerate(quiz_list):

        quiz_text = "\n"
        for item in quiz:
            if add_solution:
                answer = item['answer']
                if isinstance(answer, int):
                    quiz_text += f"\\item {item['question']} - \\textbf{ {alph_vect[answer]} }\n"
                else:
                    quiz_text += f"\\item {item['question']} - \\textbf{ {answer} }\n"
            else:
                quiz_text += f"\\item {item['question']}\n"
                if "options" in item.keys():
                    quiz_text += "\\begin{enumerate}[label=\\Alph*.]\n"
                    quiz_text += '\n'.join([
                        f"\item {x}" for x in item["options"]
                    ])
                    quiz_text += "\n\\end{enumerate}\n"
                elif "subquestions" in item.keys():
                    quiz_text += "\\begin{enumerate}\n"
                    quiz_text += '\n'.join([
                        f"\item {x}" for x in item["subquestions"]
                    ])
                    quiz_text += "\n\\end{enumerate}\n"
                    pass

        quiz_content = replace_template(content_template, {
            "%--CODE--": integer_to_roman(i+1),
            "%--QUESTIONS--": quiz_text
        })
        quiz_content_list.append(quiz_content)

    quiz_content = '\n'.join(quiz_content_list)

    doc = replace_template(doc_template, {
        "%--CONTENT--": quiz_content
    })

    with open(output_file, "w") as fp:
        fp.write(doc)


def replace_template(template: str, data: dict):
    text = template
    for v in data:
        text = text.replace(v, data[v])
    return text


def get_template(template: str):
    start_code = "%%REPEAT-START%%"
    end_code = "%%REPEAT-END%%"

    s_index = template.index(start_code)
    e_index = template.index(end_code)
    item_template = template[s_index:e_index]
    document_template = template.replace(item_template, "%--CONTENT--")
    return document_template, item_template


def integer_to_roman(num):
    # Define the mapping of integers to Roman numerals
    lookup = [
        (1000, 'M'),
        (900, 'CM'),
        (500, 'D'),
        (400, 'CD'),
        (100, 'C'),
        (90, 'XC'),
        (50, 'L'),
        (40, 'XL'),
        (10, 'X'),
        (9, 'IX'),
        (5, 'V'),
        (4, 'IV'),
        (1, 'I')
    ]

    roman = ''
    for value, symbol in lookup:
        while num >= value:
            roman += symbol
            num -= value

    return roman


def main(argc: int, argv: list[str]):

    questions_file: str = None
    output_folder: str = None
    config_file: str = None
    template_file: str = None
    use_shuffle: bool = False

    opts, args = getopt.getopt(
        argv, "q:o:c:t:s", ["questions=", "output=", "configuration=", "template=", "use_shuffle"])

    for opt, arg in opts:
        if opt in ("-q", "--questions"):
            questions_file = arg
        elif opt in ("-o", "--output"):
            output_folder = arg
        elif opt in ("-c", "--configuration"):
            config_file = arg
        elif opt in ("-t", "--template"):
            template_file = arg
        elif opt in ("-s", "--use_shuffle"):
            use_shuffle = True

    assert os.path.exists(questions_file), "Questions file does not exists"
    assert not os.path.exists(output_folder), "Output folder already exists"
    assert os.path.exists(config_file), "Config file does not exists"
    assert os.path.exists(template_file), "Template file does not exists"

    os.mkdir(output_folder)

    with open(config_file, "r") as fp:
        config: dict = json.load(fp)

    with open(template_file, "r") as fp:
        doc_template, content_template = get_template(fp.read())

    with open(questions_file, "r") as fp:
        questions: dict = json.load(fp)

    seed: int = config.get("seed", 1234)
    random.seed(seed)

    structure: dict = config.get("structure", None)
    assert structure is not None and isinstance(
        structure, dict), "Structure is not valid"

    number: int = config.get("number", 1)

    quiz_list = [
        genera_test(structure, questions, use_shuffle)
        for i in range(number)
    ]

    output_file = os.path.join(output_folder, "exams.tex")
    export_quiz(
        quiz_list,
        output_file,
        doc_template,
        content_template,
        False
    )

    output_sol_file = os.path.join(output_folder, "exam_solutions.tex")
    export_quiz(
        quiz_list,
        output_sol_file,
        doc_template,
        content_template,
        True
    )

    pass


if __name__ == "__main__":
    main(len(sys.argv)-1, sys.argv[1:])
