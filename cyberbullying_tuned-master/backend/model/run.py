import json
import sys
import os

# Add current directory to Python path to allow importing model module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from model import stage1_output, generate_peer_rationale, human_inthe_loop

# Read arguments
comment = sys.argv[1]
age = int(sys.argv[2])
ethnicity = sys.argv[3]

# Stage 1 classification
label, resources, message = stage1_output(comment)

if label == "not_cyberbullying":
    print(json.dumps({
        "flag": -1,
        "label": label,
        "response": None
    }))
    sys.exit(0)

# If bullying → generate rationale
peer_msg = generate_peer_rationale(comment, label, age)

# Call human_in_the_loop at the end of the process
feedback_prompt = human_inthe_loop()

print(json.dumps({
    "flag": 1,
    "label": label,
    "resources": resources,
    "response": message + "\n\n" + peer_msg,
    "feedback_prompt": feedback_prompt
}))
