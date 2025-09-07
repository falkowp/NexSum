import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.summarizer import TextSummarizer
import time

def test_cpu_summarizer():
    print("🧪 TESTING CPU SUMMARIZER")
    print("=" * 50)
    
    summarizer = TextSummarizer()
    
    test_text = """
    Artificial intelligence is transforming many industries across the world. 
    Machine learning algorithms can now recognize complex patterns in data that 
    humans might miss. Deep learning has revolutionized fields like image recognition 
    and natural language processing. Companies are using AI to improve efficiency, 
    reduce costs, and create new products and services. The future of AI looks 
    promising with continued advancements in technology.
    """
    
    print("⏳ Generating summary (this may take 10-30 seconds on CPU)...")
    start_time = time.time()
    summary = summarizer.summarize(test_text)
    end_time = time.time()
    
    print(f"✅ Summary generated in {end_time - start_time:.1f} seconds")
    print(f"📝 Original length: {len(test_text)} characters")
    print(f"📊 Summary length: {len(summary)} characters")
    print(f"🎯 Summary: {summary}")
    print(f"🔧 Using real model: {summarizer._dependencies_available}")
    
    return summary

if __name__ == "__main__":
    test_cpu_summarizer()