import json
import threading
from datetime import datetime
from pathlib import Path

class SecureChatHistory:
    def __init__(self):
        self.chat_history_path = Path("chat_data/chat_history.txt")
        self._ensure_directories()

    def _ensure_directories(self):
        """Create necessary directories and files"""
        self.chat_history_path.parent.mkdir(exist_ok=True)
        if not self.chat_history_path.exists():
            self.chat_history_path.write_text("")

    def initialize_encryption(self, password, max_retries=5):
        """Kept for compatibility"""
        pass

    def save_chat_entry(self, entry_data):
        """Save chat entry asynchronously"""
        try:
            entry = {
                'timestamp': datetime.now().isoformat(),
                'data': entry_data,
                'type': 'chat_entry'
            }
            
            # Write to file in background
            def write_to_file():
                try:
                    with open(self.chat_history_path, 'a', encoding='utf-8') as f:
                        f.write(json.dumps(entry) + '\n')
                except Exception as e:
                    print(f"Failed to write chat entry: {str(e)}")
            
            threading.Thread(target=write_to_file, daemon=True).start()
                
        except Exception as e:
            print(f"Failed to save chat entry: {str(e)}")

    def load_chat_history(self, limit=None):
        """Load chat history with buffered reading"""
        entries = []
        BUFFER_SIZE = 8192  # 8KB buffer
        
        try:
            with open(self.chat_history_path, 'r', 
                     encoding='utf-8', 
                     buffering=BUFFER_SIZE) as f:
                
                # Read lines in reverse if limit is set
                if limit:
                    lines = f.readlines()
                    for line in reversed(lines[-limit:]):
                        if line.strip():
                            try:
                                entry = json.loads(line.strip())
                                if entry['type'] == 'chat_entry':
                                    entries.insert(0, entry)
                            except json.JSONDecodeError:
                                continue
                else:
                    for line in f:
                        if line.strip():
                            try:
                                entry = json.loads(line.strip())
                                if entry['type'] == 'chat_entry':
                                    entries.append(entry)
                            except json.JSONDecodeError:
                                continue
                                
            return entries
            
        except Exception as e:
            print(f"Failed to load chat history: {str(e)}")
            return []