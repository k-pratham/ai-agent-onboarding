from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
import logging

logger = logging.getLogger(__name__)

# Utilizing the larger gpt oss 20B localized node for robust drafting
llm = Ollama(model="gpt-oss-20b")

def generate_draft(candidate_name: str, missing_docs: list) -> str:
    """
    Takes the output of Gap Analysis and spins up an enterprise-grade draft email.
    """
    prompt = PromptTemplate.from_template(
        "You are an HR Onboarding representative. Generate an articulate and professional follow-up email directed to {candidate_name} requesting the submission of the remaining required documents: {missing_docs}.\nEnsure the tone is warm but emphasizes priority.\n\nDraft:"
    )
    chain = prompt | llm
    
    try:
        draft = chain.invoke({"candidate_name": candidate_name, "missing_docs": ", ".join(missing_docs)})
        return draft.strip()
    except Exception as e:
        logger.error(f"Draft generation crashed: {e}")
        return "[Error: System fallback draft] Please send the missing documents."
