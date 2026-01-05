# test_once.py
from model import stage0_greeting, stage1_output, generate_peer_rationale

if __name__ == "__main__":
    # Stage 0: Greeting
    print("=== Stage 0: Greeting ===")
    print(stage0_greeting())

    # 테스트용 comment 한 개
    comment = "go back to your country"
    age = 13

    # Stage 1: Classification + Resources
    print("\n=== Stage 1: Classification ===")
    label, resources, message = stage1_output(comment)
    print("Comment:", comment)
    print("Predicted label:", label)
    print("Resources:", resources)
    print("Message:\n", message)

    # Stage 2: Peer-tone rationale
    print("\n=== Stage 2: Peer Rationale ===")
    rationale = generate_peer_rationale(comment, label, age)
    print("Age:", age)
    print("Rationale:\n", rationale)
