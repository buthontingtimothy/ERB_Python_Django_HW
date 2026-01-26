#!/usr/bin/env python
"""
Main script to verify imported data matches generated data.
Run this after importing dummy data into your database.
"""

import os
import sys
import subprocess

print("="*70)
print("VERIFYING IMPORTED DATA")
print("="*70)

# Step 1: Check if database has data
print("\nStep 1: Checking if database has data...")
try:
    # Try to import Django and check if there's any data
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    import django
    django.setup()
    
    from django.contrib.auth.models import User
    from companies.models import Company
    from listings.models import Listing
    from applies.models import Apply
    
    user_count = User.objects.count()
    company_count = Company.objects.count()
    listing_count = Listing.objects.count()
    apply_count = Apply.objects.count()
    
    print(f"  Users in database: {user_count}")
    print(f"  Companies in database: {company_count}")
    print(f"  Listings in database: {listing_count}")
    print(f"  Applies in database: {apply_count}")
    
    if user_count == 0:
        print("⚠️  No data found in database. Have you imported the CSV files?")
        print("   Run: python import_data.py or use Django's loaddata command")
        sys.exit(1)
    
    print("✓ Database contains data")
    
except ImportError as e:
    print(f"Error: Could not import Django modules: {e}")
    print("Make sure you're in the correct directory and Django is installed.")
    sys.exit(1)
except Exception as e:
    print(f"Error checking database: {e}")
    sys.exit(1)

# Step 2: Export data from database
print("\nStep 2: Exporting data from database to CSV...")
try:
    result = subprocess.run([sys.executable, 'export_data_to_csv.py'], 
                          capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)
    
    if result.returncode != 0:
        print("⚠️  Export failed")
        sys.exit(1)
    
    print("✓ Data exported successfully")
    
except Exception as e:
    print(f"Error exporting data: {e}")
    sys.exit(1)

# Step 3: Compare generated vs exported data
print("\nStep 3: Comparing generated data with exported data...")
try:
    result = subprocess.run([sys.executable, 'compare_data.py'], 
                          capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)
    
    if result.returncode != 0:
        print("⚠️  Comparison failed")
        sys.exit(1)
    
    print("✓ Comparison completed")
    
except Exception as e:
    print(f"Error comparing data: {e}")
    sys.exit(1)

print("\n" + "="*70)
print("VERIFICATION COMPLETE")
print("="*70)
print("\nNext steps:")
print("1. Review the comparison results above")
print("2. Check the 'exported_data/' directory for exported CSV files")
print("3. Compare with 'dummy_data/' directory")
print("4. If there are issues, check your import process")
print("\nExpected differences:")
print("  • Passwords: Hashed in database vs plain text in generated data")
print("  • Auto-generated dates: Might differ by seconds")
print("  • File paths: Should match exactly")
print("="*70)