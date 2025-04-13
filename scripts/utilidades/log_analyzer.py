#!/usr/bin/env python3
import re
import sys
from collections import Counter
from datetime import datetime

def analyze_logs(log_file):
    print(f"\nAnalyzing file: {log_file}")
    print("-" * 50)
    
    ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    error_pattern = r'ERROR|error|Error'
    
    ip_addresses = []
    errors = []
    
    try:
        with open(log_file, 'r') as f:
            for line in f:
                # Search for IP addresses
                ips = re.findall(ip_pattern, line)
                ip_addresses.extend(ips)
                
                # Search for errors
                if re.search(error_pattern, line):
                    errors.append(line.strip())
    
        # IP analysis
        ip_counter = Counter(ip_addresses)
        print("\nTop 10 most frequent IPs:")
        for ip, count in ip_counter.most_common(10):
            print(f"{ip}: {count} occurrences")
            
        # Error analysis
        print("\nErrors found:")
        for error in errors[:10]:  # Show only the first 10 errors
            print(f"- {error}")
            
    except FileNotFoundError:
        print(f"Error: Could not find file {log_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python log_analyzer.py <log_file>")
        print("Example: python log_analyzer.py access.log")
        sys.exit(1)
        
    log_file = sys.argv[1]
    analyze_logs(log_file) 