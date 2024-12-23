# Exam Generator Script

## Overview

This Python script generates quizzes based on a given template and a set of questions. It allows for the random selection of questions and options, as well as the export of quizzes in LaTeX format. The script can also generate solutions for the quizzes.

## Features

- Generates tests from a structured template and a set of questions.
- Supports shuffling of questions and answer options.
- Exports tests and their solutions to LaTeX files.
- Configurable through JSON files for questions, configuration, and templates.

## Requirements

- Python 3.x
- Required libraries: `random`, `os`, `getopt`, `string`, `sys`, `json`

## Files

- **questions.json**: A JSON file containing the questions categorized by topics.
- **config.json**: A JSON configuration file that defines the structure of the quiz and other settings.
- **template.tex**: A LaTeX template file for formatting the output document.
- **generator.py**: The main Python script that generates quizzes.

## Usage

1. **Prepare Your Files**:

   - Create a `questions.json` file with your questions structured by topics. Each question can have options or subquestions.
   - Create a `config.json` file to specify how many questions to select from each topic and other configurations.
   - Create a `template.tex` file that defines how the output should be formatted in LaTeX.
2. **Run the Script**:
   Open your terminal and navigate to the directory containing the script. Use the following command to run it:

```bash
python script.py -q <path_to_questions.json> -o <output_folder> -c <path_to_config.json> -t <path_to_template.tex> [-s]
```

Replace `<path_to_questions.json>`, `<output_folder>`, `<path_to_config.json>`, and `<path_to_template.tex>` with your actual file paths. The `-s` flag is optional; if included, it will shuffle the questions in the quizzes.

3. **Output**:
   The script will create an output folder (if it doesn't already exist) containing:

- `exams.tex`: The generated quiz in LaTeX format.
- `exam_solutions.tex`: The generated solutions for the quiz in LaTeX format.

## Configuration File Structure

The `config.json` file must contain the following structure:

```json
{
    "seed": 1234,
    "structure": {
        "topic1": number_of_questions,
        "topic2": number_of_questions,
        ...
    },
    "number": number_of_quizzes
}
```

- **seed**: An integer used for randomization (optional).
- **structure**: A dictionary where keys are topic names and values are the number of questions to select from each topic.
- **number**: The total number of quizzes to generate.

## Questions File Structure

The `questions.json` file should be structured as follows:

```json
{
    "topic1": [
        {
            "question": "What is question 1?",
            "options": ["Option A", "Option B", "Option C"],
            "answer": index_of_correct_option
        },
        ...
    ],
    "topic2": [
        {
            "question": "What is question 2?",
            "subquestions": ["Subquestion 1", "Subquestion 2"],
            "answer": "correct_answer"
        },
        ...
    ]
}
```

- Each topic contains a list of questions.
- Questions can have either options (for multiple-choice) or subquestions (for open-ended questions).

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

This script was developed to facilitate test generation for educational purposes. Contributions and suggestions are welcome!
