#!/usr/bin/env python
"""
Script to compare generated dummy data with exported database data.
"""

import os
import csv
import sys
from collections import Counter

def read_csv_file(filepath):
    """Read a CSV file and return list of dictionaries"""
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        return []
    
    with open(filepath, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

def compare_files(generated_file, exported_file, key_fields=None):
    """Compare two CSV files and report differences"""
    print(f"\nComparing:\n  Generated: {generated_file}\n  Exported:  {exported_file}")
    print("-" * 60)
    
    generated_data = read_csv_file(generated_file)
    exported_data = read_csv_file(exported_file)
    
    if not generated_data or not exported_data:
        print("One or both files are empty or not found.")
        return
    
    # Compare counts
    print(f"Generated records: {len(generated_data)}")
    print(f"Exported records:  {len(exported_data)}")
    
    if len(generated_data) != len(exported_data):
        print(f"⚠️  COUNT MISMATCH: Difference of {abs(len(generated_data) - len(exported_data))} records")
    else:
        print("✓ Record counts match")
    
    # Compare field names
    generated_fields = set(generated_data[0].keys()) if generated_data else set()
    exported_fields = set(exported_data[0].keys()) if exported_data else set()
    
    if generated_fields != exported_fields:
        print(f"⚠️  FIELD MISMATCH:")
        missing_in_exported = generated_fields - exported_fields
        missing_in_generated = exported_fields - generated_fields
        
        if missing_in_exported:
            print(f"  Fields in generated but not in exported: {missing_in_exported}")
        if missing_in_generated:
            print(f"  Fields in exported but not in generated: {missing_in_generated}")
    else:
        print("✓ Field names match")
    
    # Compare sample data (first 5 records)
    print(f"\nSample comparison (first 5 records):")
    print("-" * 40)
    
    for i in range(min(5, len(generated_data), len(exported_data))):
        gen_record = generated_data[i]
        exp_record = exported_data[i]
        
        print(f"\nRecord {i+1}:")
        
        # Check a few key fields
        key_fields_to_check = ['name', 'email', 'id'] if not key_fields else key_fields
        for field in key_fields_to_check:
            if field in gen_record and field in exp_record:
                gen_value = gen_record[field]
                exp_value = exp_record[field]
                
                if gen_value != exp_value:
                    print(f"  ⚠️  {field}: Generated='{gen_value}' vs Exported='{exp_value}'")
                else:
                    print(f"  ✓ {field}: '{gen_value}'")
    
    return generated_data, exported_data

def check_file_paths_in_data(data, field_name, base_dir):
    """Check if file paths in data actually exist"""
    print(f"\nChecking {field_name} file paths...")
    
    missing_files = []
    existing_files = []
    
    for i, record in enumerate(data):
        if field_name in record and record[field_name]:
            file_path = record[field_name]
            full_path = os.path.join(base_dir, file_path)
            
            if os.path.exists(full_path):
                existing_files.append(file_path)
            else:
                missing_files.append((i+1, file_path))
    
    print(f"  Total {field_name} paths: {len(existing_files) + len(missing_files)}")
    print(f"  Existing files: {len(existing_files)}")
    print(f"  Missing files: {len(missing_files)}")
    
    if missing_files:
        print(f"  First 5 missing files:")
        for i, (record_num, path) in enumerate(missing_files[:5]):
            print(f"    Record {record_num}: {path}")
    
    return existing_files, missing_files

def main():
    """Main comparison function"""
    print("="*70)
    print("COMPARING GENERATED DATA WITH EXPORTED DATABASE DATA")
    print("="*70)
    
    # Define file paths
    files_to_compare = [
        ("dummy_data/auth_user.csv", "exported_data/auth_user_exported.csv", ['username', 'email']),
        ("dummy_data/companies_company.csv", "exported_data/companies_company_exported.csv", ['name', 'email']),
        ("dummy_data/listings_listing.csv", "exported_data/listings_listing_exported.csv", ['title']),
        ("dummy_data/applies_apply.csv", "exported_data/applies_apply_exported.csv", ['name', 'email']),
    ]
    
    all_results = []
    
    for gen_file, exp_file, key_fields in files_to_compare:
        gen_data, exp_data = compare_files(gen_file, exp_file, key_fields)
        all_results.append((gen_file, gen_data, exp_data))
    
    # Check file paths for logos and CVs
    print("\n" + "="*70)
    print("CHECKING FILE PATHS")
    print("="*70)
    
    # Check logo files in company data
    company_export_file = "exported_data/companies_company_exported.csv"
    if os.path.exists(company_export_file):
        with open(company_export_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            company_data = list(reader)
            
        check_file_paths_in_data(company_data, "logo", ".")
    
    # Check CV files in apply data
    apply_export_file = "exported_data/applies_apply_exported.csv"
    if os.path.exists(apply_export_file):
        with open(apply_export_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            apply_data = list(reader)
            
        check_file_paths_in_data(apply_data, "cv", ".")
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print("\nTo perform more detailed comparisons:")
    print("1. Use diff command: diff -u dummy_data/ exported_data/")
    print("2. Use Excel or Google Sheets to open and compare files")
    print("3. Check specific fields like emails, names, and file paths")
    print("\nNote: Some differences are expected:")
    print("  - Passwords will be different (hashed vs plain text)")
    print("  - Auto-generated dates/times might differ slightly")
    print("  - IDs will be sequential in database")
    print("="*70)

if __name__ == "__main__":
    main()