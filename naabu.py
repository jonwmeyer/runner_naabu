#!/usr/bin/env python3

import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime

def main():
    """Entry point: Validate input, check dependencies, run wordlist generation, and handle results."""
    if len(sys.argv) < 2:
        print("[!] Error: Please provide a subdomain for wordlist generation")
        print("Usage: python3 alterx.py example.com")
        sys.exit(1)
    
    subdomain = sys.argv[1]

    if not check_alterx_installed():
        print("[!] Error: alterx is not installed or not in PATH")
        print("Please install alterx first: https://alterx.projectdiscovery.io/alterx/get-started/")
        sys.exit(1)
    
    activate_venv()
    
    print(f"[*] Starting alterx subdomain wordlist generation for: {subdomain}")
    exit_code = run_alterx_wordlist_generation_and_save(subdomain)
    
    if exit_code == 0:
        print("[+] wordlist generation completed successfully")
    else:
        print("[!] wordlist generation completed with errors or warnings")
    
    sys.exit(exit_code)

def check_alterx_installed():
    """Return True if alterx is installed and available in PATH."""
    try:
        result = subprocess.run(
            ["/go/bin/alterx", "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

def activate_venv():
    """Detect and note if a virtual environment exists."""
    venv_path = Path("venv")
    if venv_path.exists() and venv_path.is_dir():
        print("[*] Virtual environment found")
        venv_python = venv_path / "bin" / "python3"
        if venv_python.exists():
            print("[*] Using virtual environment Python")
        else:
            print("[*] Virtual environment found but Python not detected")

def run_alterx_wordlist_generation_and_save(subdomain):
    """Run alterx wordlist generation and save results to a timestamped file."""
    try:
        wordlist_generation_output = run_alterx_wordlist_generation(subdomain)
        if wordlist_generation_output is None:
            print("[!] alterx wordlist generation failed or returned no output")
            return 1
        
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
        filename = f"{timestamp}-wordlist generation.txt"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w") as f:
            f.write(wordlist_generation_output)
        print(f"[*] wordlist generation results saved as {filepath}")
        return 0

    except Exception as e:
        print(f"[!] Error running wordlist generation: {e}", file=sys.stderr)
        return 1 

def run_alterx_wordlist_generation(subdomain):
    """Run alterx wordlist generation on the given subdomain and return its output as a string, or None on error."""
    command = [
        "/go/bin/alterx",
        "-l", subdomain,
        "-silent"
    ]
    print(f"[*] Executing: {' '.join(command)}")
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=300,
            check=False
        )
        if result.returncode == -9:
            print("[!] Warning: alterx process was killed by SIGKILL (likely due to memory/resource limits)")
            if result.stdout.strip():
                return result.stdout
            return None
        if result.returncode != 0:
            print(f"[!] alterx exited with code {result.returncode}")
            if result.stderr:
                print("alterx error output:")
                print(result.stderr)
            return result.stdout if result.stdout.strip() else None
        return result.stdout
    except subprocess.TimeoutExpired:
        print("[!] alterx wordlist generation timed out")
        return None
    except FileNotFoundError:
        print("[!] Error: alterx command not found. Please ensure alterx is installed and in PATH")
        return None
    except Exception as e:
        print(f"[!] Unexpected error running alterx: {e}")
        return None

if __name__ == "__main__":
    main() 