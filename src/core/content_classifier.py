from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
import joblib
import json

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

MODEL_PATH = Path(__file__).resolve().parents[1] / 'models' / 'content_classifier.joblib'
EMBED_MODEL_PATH = Path(__file__).resolve().parents[1] / 'models' / 'content_classifier_embeddings.joblib'


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


# New embeddings-based classifier
class EmbeddingContentClassifier:
    """Classifier using sentence-transformers embeddings + calibrated logistic regression."""

    def __init__(self, clf: Optional[object] = None, embed_model_name: str = "all-MiniLM-L6-v2"):
        self.clf = clf
        self.embed_model_name = embed_model_name

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

    def train(self, data_dir: Path, embed_model_name: Optional[str] = None) -> None:
        try:
            from sentence_transformers import SentenceTransformer
            from sklearn.calibration import CalibratedClassifierCV
            from sklearn.linear_model import LogisticRegression
            from sklearn.model_selection import StratifiedKFold, cross_val_score
            from sklearn.metrics import f1_score, precision_recall_fscore_support
        except Exception as e:
            raise RuntimeError("Missing training dependencies: sentence-transformers or sklearn not available") from e

        texts, labels = self._read_texts_from_dir(data_dir)
        if not texts:
            raise ValueError('No training data found in dir: %s' % data_dir)

        embed_model_name = embed_model_name or self.embed_model_name
        embedder = SentenceTransformer(embed_model_name)
        X = embedder.encode(texts, show_progress_bar=True)

        from collections import Counter
        class_counts = Counter(labels)
        min_count = min(class_counts.values())

        if min_count >= 3:
            base_clf = LogisticRegression(max_iter=2000)
            clf = CalibratedClassifierCV(base_clf, cv=3)
            clf.fit(X, labels)
            trained_clf = clf
            used_calibration = True
        else:
            # Not enough examples per class for calibration; train base classifier
            base_clf = LogisticRegression(max_iter=2000)
            base_clf.fit(X, labels)
            trained_clf = base_clf
            used_calibration = False

        # Save with metadata and training examples/embeddings for nearest-example evidence
        MODEL_DIR = EMBED_MODEL_PATH.parent
        MODEL_DIR.mkdir(parents=True, exist_ok=True)
        joblib.dump({
            "clf": trained_clf,
            "embed_model_name": embed_model_name,
            "train_texts": texts,
            "train_embeddings": X,
            "used_calibration": used_calibration,
        }, EMBED_MODEL_PATH)
        self.clf = trained_clf
        self.embed_model_name = embed_model_name
        self.train_texts = texts
        self.train_embeddings = X

    def predict(self, text: str) -> Dict[str, Any]:
        if self.clf is None:
            raise RuntimeError('Embedding classifier not trained or loaded')
        try:
            from sentence_transformers import SentenceTransformer
            import numpy as np
        except Exception as e:
            raise RuntimeError("Missing runtime dependency: sentence-transformers") from e

        embedder = SentenceTransformer(self.embed_model_name)
        x = embedder.encode([text])
        probs = self.clf.predict_proba(x)[0]
        classes = list(self.clf.classes_)
        score_map = {c: float(p) for c, p in zip(classes, probs)}
        pred = classes[int(np.argmax(probs))]

        # evidence: nearest training examples by cosine similarity
        evidence = []
        if hasattr(self, 'train_embeddings') and getattr(self, 'train_embeddings') is not None:
            import numpy as _np
            from sklearn.metrics.pairwise import cosine_similarity
            sims = cosine_similarity(_np.asarray(x), _np.asarray(self.train_embeddings))[0]
            top_idx = _np.argsort(sims)[::-1][:3]
            evidence = [self.train_texts[i] for i in top_idx]
        else:
            # fallback: provide top classes as evidence
            top_sorted = sorted(score_map.items(), key=lambda kv: kv[1], reverse=True)
            evidence = [k for k, _ in top_sorted[:3]]

        return {
            'content_type': pred,
            'confidence': float(score_map.get(pred, 0.0)),
            'scores': score_map,
            'evidence': evidence,
        }

    @classmethod
    def load(cls) -> Optional['EmbeddingContentClassifier']:
        if EMBED_MODEL_PATH.exists():
            data = joblib.load(EMBED_MODEL_PATH)
            clf = data.get('clf')
            embed_model_name = data.get('embed_model_name')
            inst = cls(clf=clf, embed_model_name=embed_model_name)
            inst.train_texts = data.get('train_texts')
            inst.train_embeddings = data.get('train_embeddings')
            return inst
        return None
