#!/usr/bin/env python3
import base64
import email
import os
from email import policy
from cortexutils.analyzer import Analyzer
from transformers import pipeline

class NLPPhishingAnalyzer(Analyzer):
    """
    Analyzes email content to classify it as phishing or legitimate.
    Accepts 'file', 'mail' (Base64), and 'text' data types.
    """
    def __init__(self):
        super().__init__()
        # Initialize the HuggingFace pipeline for text classification
        self.classifier = pipeline(
            "text-classification",
            model="mrm8488/bert-tiny-finetuned-enron-spam-detection"
        )

    def _extract_text_from_msg(self, msg):
        """Extracts the plain text body from an email.message object."""
        body = ""
        if msg.is_multipart():
            # Walk through all parts of the email
            for part in msg.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get('Content-Disposition'))
                # Find the plain text part that is not an attachment
                if ctype == "text/plain" and 'attachment' not in cdispo:
                    payload = part.get_payload(decode=True)
                    if payload:
                        body += payload.decode(part.get_content_charset() or 'utf-8', errors='ignore')
        else:
            # Handle non-multipart emails
            if msg.get_content_type() == 'text/plain':
                payload = msg.get_payload(decode=True)
                if payload:
                    body = payload.decode(msg.get_content_charset() or 'utf-8', errors='ignore')
        return body.strip()

    def run(self):
        super().run()
        try:
            content_to_analyze = ""

            if self.data_type == "file":
                filepath = self.get_data()
                if not os.path.isfile(filepath):
                    return self.error(f"File not found at: {filepath}")
                # Read file as bytes for robust parsing
                with open(filepath, "rb") as f:
                    eml_bytes = f.read()
                msg = email.message_from_bytes(eml_bytes, policy=policy.default)
                content_to_analyze = self._extract_text_from_msg(msg)

            elif self.data_type == "mail":
                # Expect data to be a Base64 encoded EML string
                b64_content = self.get_data()
                if not b64_content:
                    return self.error("Mail data is empty.")
                # Decode from Base64 to bytes
                eml_bytes = base64.b64decode(b64_content)
                msg = email.message_from_bytes(eml_bytes, policy=policy.default)
                content_to_analyze = self._extract_text_from_msg(msg)

            elif self.data_type == "text":
                content_to_analyze = self.get_data()

            else:
                return self.error(f"Unsupported data type: {self.data_type}")

            if not content_to_analyze or not content_to_analyze.strip():
                return self.error("No text content found to analyze.")

            # Classify a snippet of the text (up to 512 tokens for BERT models)
            snippet = content_to_analyze[:512]
            result = self.classifier(snippet)[0]
            label = result["label"]
            score = float(result["score"])

            self.report({
                "success": True,
                "summary": {"label": label, "score": round(score, 4)},
                "full": result
            })

        except Exception as e:
            self.error(f"Analyzer failed with exception: {e}")

if __name__ == "__main__":
    NLPPhishingAnalyzer().run()
