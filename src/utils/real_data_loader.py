import requests
from datasets import load_dataset
from typing import List, Tuple

def load_real_business_data() -> List[Tuple[str, str]]:
    try:
        print("Loading real business news dataset...")
        dataset = load_dataset("cnn_dailymail", "3.0.0", split="train[:200]")  
        data_pairs = []
        
        for i, example in enumerate(dataset):
            article = example['article'].replace("\n", " ").replace("  ", " ").strip()
            summary = example['highlights'].replace("\n", " ").replace("  ", " ").strip()
            
            article = article[:800]  
            summary = summary[:200] 
            
            if len(article) > 200 and len(summary) > 30:
                data_pairs.append((article, summary))
            
            if len(data_pairs) >= 100:  
                break
        
        print(f"Successfully loaded {len(data_pairs)} real business articles")
        return data_pairs
        
    except Exception as e:
        print(f"Could not load CNN/DailyMail dataset: {e}")
        print("Using fallback business data...")
        return load_fallback_business_data()

def load_fallback_business_data() -> List[Tuple[str, str]]:
    return [
        ("Apple Inc. reported quarterly revenue of $89.5 billion, exceeding analyst expectations and showing 8% year-over-year growth driven by strong iPhone sales and services revenue.", "Apple revenue $89.5B, beat expectations with 8% growth on iPhone and services"),
        ("Tesla's Q4 earnings showed record deliveries of 405,000 vehicles, representing 40% growth compared to the same quarter last year, though profit margins narrowed due to price cuts.", "Tesla delivered 405K vehicles in Q4, 40% growth but margins narrowed"),
        
        ("Microsoft completed its $69 billion acquisition of Activision Blizzard, creating the world's third-largest gaming company and significantly expanding its Xbox game portfolio.", "Microsoft acquired Activision Blizzard for $69B, now third-largest gaming company"),
        ("Amazon announced it will acquire primary care provider One Medical for $3.9 billion, expanding its healthcare footprint and integrating telehealth with its other services.", "Amazon buying One Medical for $3.9B to expand healthcare services"),
        
        ("The Federal Reserve raised interest rates by 0.25 percentage points, bringing the benchmark rate to 4.5-4.75% in its continued effort to combat inflation while acknowledging easing price pressures.", "Fed raised rates 0.25% to 4.5-4.75% to combat inflation"),
        ("Oil prices fell 3% to $75 per barrel as concerns about global economic growth outweighed supply constraints from OPEC+ production cuts and Russian sanctions.", "Oil prices dropped 3% to $75 on economic growth concerns"),
    ]

def load_sample_data() -> List[Tuple[str, str]]:
    """Load sample data for training"""
    return load_real_business_data()

def load_validation_data() -> List[Tuple[str, str]]:
    """Load validation data"""
    try:
        print("Loading validation data...")
        dataset = load_dataset("cnn_dailymail", "3.0.0", split="validation[:50]")  
        data_pairs = []
        
        for i, example in enumerate(dataset):
            article = example['article'].replace("\n", " ").replace("  ", " ").strip()
            summary = example['highlights'].replace("\n", " ").replace("  ", " ").strip()
            
            article = article[:800]  
            summary = summary[:200] 
            
            if len(article) > 200 and len(summary) > 30:
                data_pairs.append((article, summary))
            
            if len(data_pairs) >= 20:  
                break
        
        print(f"Successfully loaded {len(data_pairs)} validation articles")
        return data_pairs
        
    except Exception as e:
        print(f"Could not load validation dataset: {e}")
        print("Using fallback validation data...")
        return [
            ("Google's parent company Alphabet reported strong earnings with revenue growth of 7% in the latest quarter, driven by increased cloud computing adoption and steady advertising revenue.", "Alphabet revenue grew 7% on cloud and advertising strength"),
            ("Meta Platforms announced plans to invest an additional $10 billion in artificial intelligence research and development, focusing on generative AI technologies and large language models.", "Meta investing $10B more in AI research and development")
        ]