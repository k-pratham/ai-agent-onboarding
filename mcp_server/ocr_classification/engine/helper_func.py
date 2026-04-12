from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
import logging

logger = logging.getLogger(__name__)

# Targeting numarkdown-8B-Thinking per requirement schema, expected to run via Ollama or similar local protocol on default ports
llm = Ollama(model="numarkdown-8b-thinking")

def classify_document_type(ocr_text: str) -> str:
    """
    Validates whether received documents match expected types using the local thinking model.
    """
    prompt = PromptTemplate.from_template(
        "Analyze the following OCR payload and classify the identity of the document strictly as one of: [AADHAAR, PAN, MARKSHEET, UNKNOWN].\n\nOCR TEXT: {text}\n\nCategory:"
    )
    
    chain = prompt | llm
    
    try:
        category = chain.invoke({"text": ocr_text}).strip().upper()
        logger.info(f"Classified document as {category}")
        return category
    except Exception as e:
        logger.error(f"Classification inference failed: {str(e)}")
        return "UNKNOWN"
