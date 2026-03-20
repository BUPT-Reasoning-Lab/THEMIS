from .llm_xml_parser import LLMXMLParser, parse_llm_xml

__all__ = ["LLMXMLParser", "parse_llm_xml"]

import importlib.metadata

metadata = importlib.metadata.metadata(__package__ or __name__)

__version__ = metadata["Version"]
__author__ = metadata["Author"]
