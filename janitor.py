import os
from langdetect import detect, DetectorFactory, lang_detect_exception

# Ensures the 9950X3D gives the same deterministic result every time
DetectorFactory.seed = 0

def run_content_audit(session_path):
    """
    Opens every file in the session, detects language, and purges non-English.
    """
    if not os.path.exists(session_path):
        print(f"❌ Session path not found: {session_path}")
        return

    print(f"🕵️ Deep-Scanning content for English integrity...")
    deleted = 0
    kept = 0

    for filename in os.listdir(session_path):
        if not filename.endswith(".md"):
            continue
            
        file_path = os.path.join(session_path, filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                # We only need the first 1000 chars to be 99.9% sure of the language
                content_sample = f.read(1000)
            
            if not content_sample.strip():
                os.remove(file_path)
                deleted += 1
                continue

            # Perform the language check
            detected_lang = detect(content_sample)
            
            if detected_lang != 'en':
                print(f"🗑️ Purging {detected_lang.upper()}: {filename}")
                os.remove(file_path)
                deleted += 1
            else:
                kept += 1
                
        except lang_detect_exception.LangDetectException:
            # Usually happens if the file is mostly code/numbers/emojis
            print(f"⚠️ Could not determine language for {filename}. Keeping for safety.")
            kept += 1
        except Exception as e:
            print(f"❌ Critical error processing {filename}: {e}")

    print(f"--- Audit Results ---")
    print(f"✅ English Files Kept: {kept}")
    print(f"🧹 Non-English Purged: {deleted}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        run_content_audit(sys.argv[1])