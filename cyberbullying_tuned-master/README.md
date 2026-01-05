# Cyberbullying Detection System

This project provides a cyberbullying detection system that classifies online comments and provides age-appropriate explanations and resources.

## Files Overview

### `model.py`
The core module containing the cyberbullying detection logic. It provides three main functions:

1. **`classify_comment(comment: str) -> str`**
   - Classifies a comment into one of three categories: `age`, `ethnicity`, or `not_cyberbullying`
   - Uses a fine-tuned GPT-4o model (`ft:gpt-4o-2024-08-06:personal:cb-final:Chlrmg79`)
   - Returns the classification label as a string

2. **`stage1_output(comment: str) -> tuple[str, str, str]`**
   - Performs classification and returns a formatted response
   - Returns: `(label, resources, message)`
     - `label`: The classification label
     - `resources`: List of helpful resources/links for the detected category
     - `message`: A user-friendly message explaining the classification and next steps

3. **`generate_peer_rationale(comment: str, label: str, age: int) -> str`**
   - Generates an age-appropriate explanation for why a comment was classified as cyberbullying
   - Takes the user's age into account to provide appropriate language and tone
   - Uses GPT-4o-mini to generate peer-tone explanations
   - Returns a rationale message explaining the classification

4. **`stage0_greeting() -> str`**
   - Returns the initial greeting message for the chatbot

**API Key Configuration:**
- The module reads the OpenAI API key from an `api` file in the project root
- If the `api` file doesn't exist, it falls back to the `OPENAI_API_KEY` environment variable

### `testing.py`
A test script that demonstrates how to use the functions in `model.py`. It runs through all three stages:

1. **Stage 0**: Displays the greeting message
2. **Stage 1**: Tests comment classification with a sample comment ("go back to your country")
   - Shows the predicted label, resources, and formatted message
3. **Stage 2**: Tests rationale generation with a sample age (13)
   - Shows the age-appropriate explanation

**Usage:**
```bash
python testing.py
```

## Setup Instructions

### 1. Install Dependencies

Install the required Python packages using `requirements.txt`:

```bash
pip install -r requirements.txt
```

**For Windows PowerShell:**
```powershell
pip install -r requirements.txt
```

**For macOS/Linux:**
```bash
pip install -r requirements.txt
```

If you're using a virtual environment (recommended):

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
.\venv\Scripts\activate.bat
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Key

Create an `api` file in the project root containing your OpenAI API key:

```
sk-proj-your-api-key-here
```

Alternatively, you can set the `OPENAI_API_KEY` environment variable:

**Windows PowerShell:**
```powershell
$env:OPENAI_API_KEY = "sk-proj-your-api-key-here"
```

**macOS/Linux:**
```bash
export OPENAI_API_KEY="sk-proj-your-api-key-here"
```

### 3. Required Files

Ensure you have the following files in your project:
- `model.py` - Core detection logic
- `testing.py` - Test script
- `resource.py` - Resource mappings (imported by model.py)
- `api` - Your OpenAI API key file

## Running the Code

### Test the Model

Run the test script to see the system in action:

```bash
python testing.py
```

This will:
1. Display the greeting message
2. Classify a sample comment
3. Generate an age-appropriate explanation

### Use in Your Code

```python
from model import stage1_output, generate_peer_rationale

# Classify a comment
label, resources, message = stage1_output("your comment here")
print(f"Label: {label}")
print(f"Resources: {resources}")
print(f"Message: {message}")

# Generate explanation
rationale = generate_peer_rationale("your comment", label, age=13)
print(f"Explanation: {rationale}")
```

## Dependencies

- **openai** (>=1.0.0): OpenAI Python client for API calls
- **fastapi** (0.104.1): Web framework for API server (optional, for `api_server.py`)
- **uvicorn** (0.24.0): ASGI server for FastAPI (optional, for `api_server.py`)
- **pydantic** (2.5.0): Data validation (optional, for `api_server.py`)

## Notes

- The fine-tuned model is configured for three labels: `age`, `ethnicity`, and `not_cyberbullying`
- The system uses structured JSON responses to ensure consistent output
- Age-appropriate explanations adapt language complexity based on the user's age

