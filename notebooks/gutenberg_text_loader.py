# gutenberg_text_loader.py
# Minimal Gutenberg text downloader and cache manager

import requests
import pathlib
import os
import re


class GutenbergSource:
    """
    Downloads and caches Project Gutenberg texts.
    Usage: gs = GutenbergSource(); gs.load_from_url(url)
    """
    
    def __init__(self, cache_dir: str = "./.cache"):
        self.cache_dir = pathlib.Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def load_from_url(self, url: str) -> str:
        """
        Download Gutenberg text from URL and cache it.
        Returns the file path to the cached text.
        """
        # Extract Gutenberg ID from URL
        match = re.search(r'pg(\d+)', url)
        if not match:
            raise ValueError(f"Could not extract Gutenberg ID from URL: {url}")
        
        gutenberg_id = match.group(1)
        filename = f"pg{gutenberg_id}.txt"
        outfile = self.cache_dir / filename
        
        # Return cached file if it exists
        if outfile.exists():
            print(f"   📂 Using cached: {outfile}")
            return str(outfile)
        
        # Download and save
        print(f"   ⬇️  Downloading from Gutenberg: {url}")
        try:
            response = requests.get(url, timeout=60, headers={
                'User-Agent': 'Mozilla/5.0 (compatible; RAG-Lab/1.0)'
            })
            response.raise_for_status()
            
            # Save to cache
            outfile.write_text(response.text, encoding='utf-8')
            print(f"   ✅ Saved: {outfile}")
            
            return str(outfile)
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to download {url}: {e}")
    
    def get_cached_text(self, gutenberg_id: str) -> str:
        """Retrieve cached text by Gutenberg ID."""
        filename = f"pg{gutenberg_id}.txt"
        filepath = self.cache_dir / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"No cached text for pg{gutenberg_id}")
        
        return filepath.read_text(encoding='utf-8')
    
    def list_cached_files(self):
        """List all cached Gutenberg texts."""
        files = list(self.cache_dir.glob("pg*.txt"))
        return [f.name for f in files]
    
    def clear_cache(self):
        """Clear all cached files."""
        files = self.cache_dir.glob("pg*.txt")
        for f in files:
            f.unlink()
        print(f"   🗑️  Cleared {len(list(files))} cached files")
