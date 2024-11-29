from langchain_experimental.data_anonymizer import PresidioAnonymizer
import difflib
import re
import ruamel.yaml
import sys

def capture_pii(original_text, anon_text):
    d = difflib.Differ()
    diff = list(d.compare(original_text.split(), anon_text.split()))
    pii_dict = {}
    counter = 1
    for item in diff:
        code, text = item[:1], item[2:].strip()
        if code == '-':
            if text.isdigit():
                category = f'pii_{counter}'
                pii_dict[category] = text
            elif re.match(r"[^@]+@[^@]+\.[^@]+", text):  # Check for email format
                category = f'pii_{counter}'
                pii_dict[category] = text
            else:
                category = f'pii_{counter}'
                pii_dict[category] = text
            counter += 1

    yaml = ruamel.yaml.YAML()
    yaml.dump(pii_dict, sys.stdout)

if __name__ == "__main__":
    anonymizer = PresidioAnonymizer()
    original_text = input("Enter the original text: ")
    anon_text = anonymizer.anonymize(original_text)
    print("\nCaptured PII:")
    capture_pii(original_text, anon_text)