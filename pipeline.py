import re

class IndicDataPipeline:
    """
    Backend data processing layer for the IIT Kanpur Git Supersite.
    Parses unstructured text records and outputs schema-validated JSON formats.
    """
    def __init__(self, raw_input_text):
        self.raw_input = raw_input_text
        self.structured_db = {
            "metadata": {
                "processor_name": "Appala Srinivas Tanakala", 
                "status": "Cleaned"
            }, 
            "verses": []
        }

    def advanced_indic_tokenization(self, text):
        """Cleans traditional verse markers and splits into clean tokens."""
        cleaned_text = re.sub(r'[।॥\s]+', ' ', text).strip()
        tokens = [token for token in cleaned_text.split(' ') if token]
        return tokens, len(tokens)

    def run_parser_pipeline(self):
        """Iterates through headers and safely extracts multi-line blocks."""
        matches = list(re.finditer(r'\[CHAPTER:\s*(\d+),\s*VERSE:\s*(\d+)\]', self.raw_input))
        
        for i, match in enumerate(matches):
            ch, vr = match.groups()
            
            # Map boundaries safely between individual blocks
            start_pos = match.end()
            end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(self.raw_input)
            verse_text = self.raw_input[start_pos:end_pos].strip()
            
            # DOTALL lookaheads prevent breaking on multiline returns
            sanskrit = re.search(r'SANSKRIT:\s*(.*?)(?=\n[A-Z]+:|$)', verse_text, re.DOTALL)
            telugu = re.search(r'TELUGU:\s*(.*?)(?=\n[A-Z]+:|$)', verse_text, re.DOTALL)
            english = re.search(r'ENGLISH:\s*(.*?)(?=\n[A-Z]+:|$)', verse_text, re.DOTALL)
            
            sanskrit_txt = re.sub(r'\s+', ' ', sanskrit.group(1)).strip() if sanskrit else ""
            telugu_txt = re.sub(r'\s+', ' ', telugu.group(1)).strip() if telugu else ""
            english_txt = re.sub(r'\s+', ' ', english.group(1)).strip() if english else ""
            
            # Process token analytics using the advanced method
            _, s_word_count = self.advanced_indic_tokenization(sanskrit_txt)
            
            # Integrity Check Validation Flags
            issues = []
            if not sanskrit_txt: issues.append("Missing Sanskrit Text")
            if not telugu_txt: issues.append("Missing Telugu Script Translation")
            if not english_txt: issues.append("Missing English Translation Mapping")

            verse_record = {
                "verse_id": f"BG_{int(ch):02d}_{int(vr):02d}",
                "chapter": int(ch),
                "verse_number": int(vr),
                "linguistic_layers": {
                    "devanagari_sanskrit": sanskrit_txt,
                    "telugu_script": telugu_txt
                },
                "translations": {
                    "english_translation": english_txt
                },
                "analytics": {
                    "word_count": s_word_count
                },
                "validation": {
                    "is_valid": len(issues) == 0,
                    "flagged_issues": issues
                }
            }
            self.structured_db["verses"].append(verse_record)
            
        return self.structured_db
