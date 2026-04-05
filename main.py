import os
import time
from datetime import datetime
from urllib.parse import urlparse
from scraper.engine import FirecrawlEngine
from janitor import run_content_audit

def main():
    # 1. Get User Input
    print("--- Webscraper CLI ---")
    target_url = input("Enter the URL to crawl (e.g., https://wiki.com): ").strip()
    
    if not target_url.startswith("http"):
        print("Error: Please enter a valid URL starting with http/https")
        return

    # 2. Setup Paths
    project_root = os.path.dirname(os.path.abspath(__file__))
    domain = urlparse(target_url).netloc.replace(".", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    save_path = os.path.join(project_root, "data", domain, timestamp)
    os.makedirs(save_path, exist_ok=True)

    # 3. Start Crawl
    engine = FirecrawlEngine()
    try:
        job_id = engine.run_crawl(target_url)
        print(f"🚀 Job started! ID: {job_id}")
        
        while True:
            data = engine.get_status(job_id)
            status = data.get("status")
            done = data.get("completed", 0)
            total = data.get("total", 0)

            print(f"[{status.upper()}] Progress: {done}/{total} pages", end="\r")

            if status == "completed":
                print(f"\n✅ Crawl Finished. Saving files to {save_path}...")
                for page in data.get("data", []):
                    # Save logic
                    path = urlparse(page['metadata']['sourceURL']).path.strip("/")
                    name = path.replace("/", "_") or "index"
                    with open(os.path.join(save_path, f"{name}.md"), "w", encoding="utf-8") as f:
                        f.write(page.get("markdown", ""))
                
                # --- JANITOR FUNCTIONALITY ---
                print("\n🧹 Initializing Janitor: Content-Aware English Audit...")
                run_content_audit(save_path)
                break
            
            time.sleep(5)
            
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()