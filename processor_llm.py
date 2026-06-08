from dotenv import load_dotenv
import os
import re

load_dotenv()

# Try to use llama-cpp-python if available. If not installed or model
# path is not set, fall back to returning 'Unclassified' so the app
# continues to function without an LLM.
_LLAMA_MODEL = os.getenv("LLAMA_MODEL_PATH", "models/llama-model.bin")

try:
    from llama_cpp import Llama
except Exception:
    Llama = None

_llm = None
if Llama is not None and os.path.exists(_LLAMA_MODEL):
    try:
        _llm = Llama(model_path=_LLAMA_MODEL)
    except Exception:
        _llm = None


def classify_with_llm(log_msg):
    """Classify a log message using a local LLaMA model (llama-cpp-python).

    Returns a single category string or 'Unclassified' when the model
    is not available or fails.
    """
    if _llm is None:
        return "Unclassified"

    prompt = f'''Classify the log message into one of these categories:
    (1) Workflow Error, (2) Deprecation Warning.
    If you can't figure out a category, use "Unclassified".
    Put the category inside <category> </category> tags.
    Log message: {log_msg}'''

    try:
        resp = _llm.create(prompt=prompt, max_tokens=64, temperature=0.5)
        # llama-cpp-python returns text under choices[0]['text']
        content = resp.get("choices", [{}])[0].get("text", "")
        match = re.search(r'<category>(.*)</category>', content, flags=re.DOTALL)
        return match.group(1).strip() if match else "Unclassified"
    except Exception:
        return "Unclassified"


if __name__ == "__main__":
    print(classify_with_llm(
        "Case escalation for ticket ID 7324 failed because the assigned support agent is no longer active."))
    print(classify_with_llm(
        "The 'ReportGenerator' module will be retired in version 4.0. Please migrate to the 'AdvancedAnalyticsSuite' by Dec 2025"))
    print(classify_with_llm("System reboot initiated by user 12345."))