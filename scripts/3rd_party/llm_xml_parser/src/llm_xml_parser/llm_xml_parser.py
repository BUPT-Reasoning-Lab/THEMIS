import re
from typing import Union, Dict, List, Any, Optional

class LLMXMLParser:
    """
    专门为 THEMIS 评测设计的健壮解析器。
    升级特性：支持提取 LLM 自我纠错后的最后一个有效标签，增强了对 MASK 和 CHOICE 变体的处理。
    """

    @staticmethod
    def parse(text: str) -> Dict[str, Any]:
        if not text:
            return {"choice": None, "mask": [], "tampered_parts": [], "tampered_sentences": [], "explanation": ""}

        # 1. 预处理：标准化空值描述
        text = LLMXMLParser._standardize_empty(text)
        # 2. 提取 Choice (支持 CHOICE 或 CHOICES 变体)
        # 逻辑：获取所有匹配项，取最后一个
        choices_tags = LLMXMLParser._extract_all_tags(text, r"CHOICES?")
        final_choice_raw = choices_tags[-1] if choices_tags else ""
        final_choices = LLMXMLParser._process_choice_data(final_choice_raw)

        # 3. 提取 Mask
        masks_list = LLMXMLParser._extract_all_tags(text, r"MASK")
        final_mask_raw = masks_list[-1] if masks_list else ""
        final_mask = LLMXMLParser._process_mask_data(final_mask_raw)

        # 3. 提取 PARTS (类别标签提取)
        parts_tags = LLMXMLParser._extract_all_tags(text, r"PARTS")
        final_parts = LLMXMLParser._process_parts_data(parts_tags[-1] if parts_tags else "")

        # 4. 提取 SENTENCES (多行文本清理)
        sentences_tags = LLMXMLParser._extract_all_tags(text, r"SENTENCES")
        final_sentences = LLMXMLParser._process_sentences_data(sentences_tags[-1] if sentences_tags else "")


        # 4. 提取 Explanation
        explanations = LLMXMLParser._extract_all_tags(text, r"EXPLANATION")
        final_explanation = explanations[-1] if explanations else ""

        res =  {
            "choice": final_choices,
            "mask": final_mask,
            "tampered_parts": final_parts,
            "tampered_sentences": final_sentences,
            "explanation": final_explanation,
            "raw_response": text
        }

        if not res["choice"] or (not res["explanation"] and len(text) > 100):
            fallback = LLMXMLParser._fallback_parse(text)
            if not res["choice"]:
                res["choice"] = fallback["choice"]
            if not res["explanation"]:
                res["explanation"] = fallback["explanation"]
        
        return res
    
    @staticmethod
    def _fallback_parse(text: str) -> Dict[str, Any]:
        """
        当标签提取失败时，尝试从原始文本中匹配结论。
        针对：'Therefore, the most appropriate choice is D' 或 'Final Answer: D'
        """
        res = {"choice": [], "explanation": ""}
        
        # 1. 匹配选项：通常在结论句中
        # 匹配模式如：choice is D, answer is A, 或者是 D) no forgery
        choice_patterns = [
            r"(?:choice|answer|result)\s*(?:is|:)\s*([A-G])", # choice is D
            r"\b([A-G])\)\s*(?:no forgery|splicing|copy-move|aigc)", # D) no forgery
            r"Final\s*Answer\s*[:：]\s*([A-G])" # Final Answer: D
        ]
        
        for p in choice_patterns:
            matches = re.findall(p, text, re.I)
            if matches:
                # 取最后一个匹配到的字母（符合 Last-is-Best 原则）
                res["choice"] = [matches[-1].upper()]
                break
        
        # 2. 匹配解释：如果没标签，就把最后一段话当作解释
        if not res["explanation"]:
            paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
            if paragraphs:
                res["explanation"] = paragraphs[-1]
                
        return res
    
    @staticmethod
    def _process_choice_data(raw: str) -> List[str]:
        """
        处理多选逻辑：提取所有 A-G 字母，去重并按字母顺序排序。
        """
        if not raw:
            return []
        # 匹配 A-G 的所有字母
        letters = re.findall(r"[A-G]", raw.upper())
        # 去重并排序，确保结果一致性 (例如 "B, A" 统一为 ["A", "B"])
        return sorted(list(set(letters)))
    
    @staticmethod
    def _extract_all_tags(text: str, tag_pattern: str) -> List[str]:
        """
        通用提取函数：返回所有匹配该标签的内容列表。
        支持闭合标签 <TAG>内容</TAG> 和残缺标签 <TAG>内容
        """
        contents = []
        
        # 模式1：匹配闭合标签
        full_pattern = f"<{tag_pattern}>(.*?)</{tag_pattern}>"
        full_matches = re.findall(full_pattern, text, re.DOTALL | re.IGNORECASE)
        
        # 模式2：匹配未闭合标签（直到下一个 < 或结束）
        # 这种模式常用于捕获 LLM 还没写完或格式破损的情况
        partial_pattern = f"<{tag_pattern}>(.*?)(?=<|$)"
        partial_matches = re.findall(partial_pattern, text, re.DOTALL | re.IGNORECASE)
        
        # 合并并去重（保留顺序），主要为了应对既有闭合又有残缺的复杂情况
        # 这里直接取 partial_matches 通常更稳健，因为它包含了 full_matches 的内容
        return [m.strip() for m in partial_matches if m.strip()]

    @staticmethod
    def _process_mask_data(raw: str) -> List[int]:
        """
        清洗 Mask 数据：转整数、去重、排序。
        """
        raw = raw.upper()
        if not raw or "EMPTY" in raw.upper():
            return []
        
        nums = re.findall(r"\d+", raw)
        try:
            return sorted(list(set(int(n) for n in nums)))
        except ValueError:
            return []
        
    @staticmethod
    def _process_parts_data(raw: str) -> List[str]:
        """
        处理 PARTS：将 'caption, related' 转换为 ['caption', 'related']
        并进行标准化处理（去除空格、转小写）
        """
        if not raw or "EMPTY" in raw.upper():
            return []
        # 按逗号或分号分割，并清理每个元素
        parts = [p.strip().lower() for p in re.split(r"[,;，；]", raw)]
        # 过滤掉空字符串和无效描述
        return [p for p in parts if p and p not in ["none", "null"]]
    
    staticmethod
    def _process_sentences_data(raw: str) -> List[str]:
        """
        处理 SENTENCES：将多行文本拆分为列表，移除行首序号（如 '1)' 或 '1.'）
        """
        if not raw or "EMPTY" in raw.upper():
            return []
        
        # 按换行符分割
        lines = raw.split('\n')
        processed_lines = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            # 移除行首的序号，例如 "1) ", "2. ", "- "
            clean_line = re.sub(r"^(\d+[\.\)\s]|-|\*)\s*", "", line).strip()
            if clean_line:
                processed_lines.append(clean_line)
        return processed_lines
    
    @staticmethod
    def _standardize_empty(text: str) -> str:
        """
        统一各种 '空' 的表达方式。
        """
        empty_keywords = ["none", "null", "0", r"\[\s*\]", "empty"]
        new_text = text
        for kw in empty_keywords:
            # 匹配 >none< 这种标签内的内容
            pattern = f">\\s*{kw}\\s*<"
            new_text = re.sub(pattern, ">EMPTY<", new_text, flags=re.IGNORECASE)
        
        # 处理完全空白的标签
        new_text = re.sub(r"<MASK>\s*</MASK>", "<MASK>EMPTY</MASK>", new_text, flags=re.IGNORECASE)
        new_text = re.sub(r"<PARTS>\s*</PARTS>", "<PARTS>EMPTY</PARTS>", new_text, flags=re.IGNORECASE)
        new_text = re.sub(r"<SENTENCES>\s*</SENTENCES>", "<PARTS>EMPTY</PARTS>", new_text, flags=re.IGNORECASE)
        return new_text

def parse_llm_xml(text: str) -> Union[dict, list]:
    """
    便捷函数：解析 LLM 输出的 JSON

    Args:
        text: 待解析的文本

    Returns:
        解析后的 Python 对象（dict 或 list）

    Raises:
        ValueError: 当无法解析 JSON 时抛出
    """
    return LLMXMLParser.parse(text)

