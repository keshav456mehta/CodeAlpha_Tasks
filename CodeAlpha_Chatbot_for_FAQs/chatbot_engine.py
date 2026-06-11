"""
chatbot_engine.py
NLP engine: TF-IDF + cosine similarity over FAQ dataset
"""

import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# silent NLTK downloads
for pkg in ["punkt", "punkt_tab", "stopwords", "wordnet", "omw-1.4"]:
    try:
        nltk.download(pkg, quiet=True)
    except Exception:
        pass

from faq_data import FAQS


class FAQChatbot:
    THRESHOLD = 0.18   # minimum cosine similarity to return a match

    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words  = set(stopwords.words("english"))
        self.questions   = [q for q, _ in FAQS]
        self.answers     = [a for _, a in FAQS]
        self.vectorizer  = TfidfVectorizer(
            preprocessor=self._preprocess,
            ngram_range=(1, 2),
            min_df=1,
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(self.questions)

    # ── NLP pipeline ──────────────────────────────────────────────────────────
    def _preprocess(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        tokens = word_tokenize(text)
        tokens = [
            self.lemmatizer.lemmatize(t)
            for t in tokens
            if t not in self.stop_words and len(t) > 1
        ]
        return " ".join(tokens)

    # ── Query ─────────────────────────────────────────────────────────────────
    def get_answer(self, user_input: str):
        vec = self.vectorizer.transform([user_input])
        sims = cosine_similarity(vec, self.tfidf_matrix).flatten()
        best_idx = int(np.argmax(sims))
        best_score = float(sims[best_idx])

        if best_score < self.THRESHOLD:
            return (
                "I don't have a specific answer for that in my knowledge base. "
                "Try rephrasing, or pick a topic from the sidebar. "
                "I'm specialised in Generative AI & LLMs.",
                None
            )
        return self.answers[best_idx], best_score


# ── Quick CLI test ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    bot = FAQChatbot()
    tests = [
        "What is a large language model?",
        "explain hallucination in AI",
        "what is RAG",
        "attention mechanism transformer",
        "difference between GPT and BERT",
        "how does fine-tuning work",
        "random nonsense xyz abc",
    ]
    for q in tests:
        ans, score = bot.get_answer(q)
        pct = f"{score*100:.0f}%" if score else "—"
        print(f"\nQ: {q}\nA ({pct}): {ans[:80]}...")
