from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
import joblib
import json

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

MODEL_PATH = Path(__file__).resolve().parents[1] / 'models' / 'content_classifier.joblib'


class ContentClassifier:
    def __init__(self, model: Optional[Pipeline] = None):
        self.model = model

    @staticmethod
    def _read_texts_from_dir(data_dir: Path) -> Tuple[List[str], List[str]]:
        texts: List[str] = []
        labels: List[str] = []
        for f in data_dir.iterdir():
            if f.is_file() and f.suffix in ('.txt',):
                label = f.stem
                content = f.read_text(encoding='utf-8')
                texts.append(content)
                labels.append(label)
        return texts, labels

    def train(self, data_dir: Path) -> None:
        texts, labels = self._read_texts_from_dir(data_dir)
        if not texts:
            raise ValueError('No training data found in dir: %s' % data_dir)

        pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
            ('clf', LogisticRegression(max_iter=1000))
        ])
        pipeline.fit(texts, labels)
        self.model = pipeline
        # Ensure model dir exists
        MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.model, MODEL_PATH)

    def predict(self, text: str) -> Dict[str, Any]:
        if self.model is None:
            raise RuntimeError('Model is not trained or loaded')
        pred = self.model.predict([text])[0]
        probs = self.model.predict_proba([text])[0]
        classes = list(self.model.classes_)
        score_map = {c: float(p) for c, p in zip(classes, probs)}
        # top features (approx) - get top tfidf features for the document
        # note: access vectorizer transform
        tfidf = self.model.named_steps['tfidf']
        x = tfidf.transform([text])
        # get top n features indices
        import numpy as np
        arr = x.toarray()[0]
        top_idx = np.argsort(arr)[::-1][:10]
        features = [tfidf.get_feature_names_out()[i] for i in top_idx if arr[i] > 0]

        return {
            'content_type': pred,
            'confidence': float(score_map.get(pred, 0.0)),
            'scores': score_map,
            'evidence': features,
        }

    @classmethod
    def load(cls) -> Optional['ContentClassifier']:
        if MODEL_PATH.exists():
            model = joblib.load(MODEL_PATH)
            return cls(model)
        return None
