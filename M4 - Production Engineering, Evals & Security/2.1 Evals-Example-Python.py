import json ### Used for handling JSON data

from anthropic import Anthropic ### Used for interacting with the Anthropic API
from statistics import mean #### Used for calculating the average score of the evaluation results
import re ### Used for validating Regex syntax
import ast ### Used for validating Python syntax

client = Anthropic()
model = "claude-sonnet-4-6"

messages = []

def generate_dataset():
    prompt = """
Generate a evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts
that generate Python, JSON, or Regex specifically for AWS-related tasks. Generate an array of JSON objects,
each representing task that requires Python, JSON, or a Regex to complete.

Example output:
```json
[
    {
        "task": "Description of task",
        "format": "json" or "python" or "regex",
        "solution_criteria": "Key criteria for evaluating the solution"
    },
    ...additional
]
```

* Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a regular expression.
* Focus on tasks that do not require writing much code

Please generate 3 objects.
Return only a valid JSON array. Do not use Markdown code fences or include any other text.
"""
    messages = []
    add_user_message(messages, prompt)
    text = chat(messages)
    return json.loads(text)


def validate_json(text):
    try:
        json.loads(text.strip())
        return 10
    except json.JSONDecodeError:
        return 0

def validate_python(text):
    try:
        ast.parse(text.strip())
        return 10
    except SyntaxError:
        return 0

def validate_regex(text):
    try:
        re.compile(text.strip())
        return 10
    except re.error:
        return 0

def grade_syntax(response, test_case):
    format = test_case["format"]
    if format == "json":
        return validate_json(response)
    elif format == "python":
        return validate_python(response)
    else:
        return validate_regex(response)


def add_user_message(messages, content):
    userMessage = {"role": "user", "content": content}
    messages.append(userMessage)
    return messages

def add_assistant_message(messages, content):
    assistantMessage = {"role": "assistant", "content": content}
    messages.append(assistantMessage)
    return messages

def chat(messages, system=None, temperature=1.0, stop_sequences=None):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
       # "temperature": temperature,
        "stop_sequences": stop_sequences or [],
    }

    if system:
        params["system"] = system

    message = client.messages.create(**params)
    return message.content[0].text

def run_prompt(test_case):
    """Merges the prompt and test case input, then returns the result"""
    prompt = f"""
    Please solve the following task:

    {test_case["task"]}
    * Respond only with Python, JSON, or a plain Regex
    * Do not add any comments or commentary or explanation
    * Do not use Markdown code fences
    """
    messages = []
    add_user_message(messages, prompt)
    output = chat(messages)
    return output

def run_test_case(test_case):
    output = run_prompt(test_case)
    
    # Grade the output
    model_grade = grade_by_model(test_case, output)
    model_score = model_grade["score"]
    reasoning = model_grade["reasoning"]
    syntax_score = grade_syntax(output, test_case)
    score = (model_score + syntax_score) / 2

    
    return {
        "output": output, 
        "test_case": test_case, 
        "score": score,
        "reasoning": reasoning
    }

def run_eval(dataset):
    """Loads the dataset and calls run_test_case with each case"""
    results = []
    
    for test_case in dataset:
        result = run_test_case(test_case)
        results.append(result)
    
    average_score = mean([result["score"] for result in results])
    print(f"Average score: {average_score}")

    return results


# Function to grade a test case + output using a model
def grade_by_model(test_case, output):
    eval_prompt = f"""
        You are an expert AWS code reviewer. Your task is to evaluate the following AI-generated solution.

        Original Task:
        <task>
        {test_case["task"]}
        </task>

        Solution to Evaluate:
        <solution>
        {output}
        </solution>

        Criteria you should use to evaluate the solution:
        <criteria>
        {test_case["solution_criteria"]}
        </criteria>

        Output Format
        Provide your evaluation as a structured JSON object with the following fields, in this specific order:
        - "strengths": An array of 1-3 key strengths
        - "weaknesses": An array of 1-3 key areas for improvement
        - "reasoning": A concise explanation of your overall assessment
        - "score": A number between 1-10

        Return only a valid JSON object. Do not use Markdown code fences or include any other text.
        Keep your response concise and direct.
        Example response shape:
        {{
            "strengths": string[],
            "weaknesses": string[],
            "reasoning": string,
            "score": number
        }}
    """

    messages = []
    add_user_message(messages, eval_prompt)
    eval_text = chat(messages)
    return json.loads(eval_text)

## end of methods. 

### Generate the evaluation dataset
dataset =   generate_dataset();
print(json.dumps(dataset, indent=4))
with open("prompt_eval_dataset.json", "w") as f:
    json.dump(dataset, f, indent=2)

### Load the evaluation dataset
with open("prompt_eval_dataset.json", "r") as f:
    dataset = json.load(f)
### Run the evaluation
results = run_eval(dataset)
print(json.dumps(results, indent=4))
### Save the evaluation results
with open("prompt_eval_dataset_result.json", "w") as f:
    json.dump(results, f, indent=2)
