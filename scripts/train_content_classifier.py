"""Train and save a content classifier using data in `test_data/` or provided folder.

Example:
  python scripts/train_content_classifier.py --data-dir test_data
"""
from pathlib import Path
import argparse
from src.core.content_classifier import ContentClassifier


def main(data_dir: Path):
    cc = ContentClassifier()
    cc.train(data_dir)
    print('Model trained and saved')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--data-dir', type=Path, default=Path('test_data'))
    args = p.parse_args()
    main(args.data_dir)
