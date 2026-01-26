#!/usr/bin/env python
"""
Django management command to export database data to CSV files.
This script exports data in the same format as generate_dummy_data.py
so you can verify imported data matches generated data.
"""

import os
import sys
import csv
import django
from datetime import datetime

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from companies.models import Company
from listings.models import Listing
from applies.models import Apply

def export_auth_user_data():
    """Export auth_user data to CSV"""
    print("Exporting auth_user data...")
    
    users = User.objects.all().order_by('id')
    data = []
    
    for user in users:
        user_data = {
            "password": user.password,
            "last_login": user.last_login.strftime("%Y-%m-%d %H:%M:%S") if user.last_login else "",
            "is_superuser": "1" if user.is_superuser else "0",
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "is_staff": "1" if user.is_staff else "0",
            "is_active": "1" if user.is_active else "0",
            "date_joined": user.date_joined.strftime("%Y-%m-%d %H:%M:%S"),
        }
        data.append(user_data)
    
    return data

def export_company_data():
    """Export company data to CSV"""
    print("Exporting company data...")
    
    companies = Company.objects.all().order_by('id')
    data = []
    
    for company in companies:
        company_data = {
            "name": company.name,
            "logo": str(company.logo) if company.logo else "",  # Get the file path
            "industry": company.industry,
            "serivces": company.serivces,  # Note: Typo in field name matches model
            "description": company.description,
            "phone": company.phone,
            "email": company.email,
            "create_date": company.create_date.strftime("%Y-%m-%d %H:%M:%S"),
            "user_id": company.user.id if company.user else "",
        }
        data.append(company_data)
    
    return data

def export_listing_data():
    """Export listing data to CSV"""
    print("Exporting listing data...")
    
    listings = Listing.objects.all().order_by('id')
    data = []
    
    for listing in listings:
        listing_data = {
            "company_id": listing.company.id if listing.company else "",
            "title": listing.title,
            "industry": listing.industry,
            "budget": listing.budget,
            "duration": listing.duration,
            "description": listing.description,
            "requirement": listing.requirement,
            "publish_date": listing.publish_date.strftime("%Y-%m-%d %H:%M:%S"),
            "is_active": "1" if listing.is_active else "0",
        }
        data.append(listing_data)
    
    return data

def export_apply_data():
    """Export apply data to CSV"""
    print("Exporting apply data...")
    
    applies = Apply.objects.all().order_by('id')
    data = []
    
    for apply in applies:
        apply_data = {
            "listing_id": apply.listing.id if apply.listing else "",
            "name": apply.name,
            "email": apply.email,
            "phone": apply.phone,
            "message": apply.message,
            "cv": str(apply.cv) if apply.cv else "",  # Get the file path
            "apply_date": apply.apply_date.strftime("%Y-%m-%d %H:%M:%S"),
            "user_id": apply.user.id if apply.user else "",
        }
        data.append(apply_data)
    
    return data

def write_csv(filename, data, fieldnames):
    """Write data to CSV file"""
    os.makedirs('exported_data', exist_ok=True)
    filepath = f'exported_data/{filename}'
    
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"Exported {len(data)} records to {filepath}")
    return filepath

def main():
    """Main function to export all data"""
    print("="*60)
    print("EXPORTING DATABASE DATA TO CSV FILES")
    print("="*60)
    
    # Export auth_user data
    auth_user_fields = [
        "password", "last_login", "is_superuser", "username", "first_name",
        "last_name", "email", "is_staff", "is_active", "date_joined"
    ]
    auth_user_data = export_auth_user_data()
    write_csv('auth_user_exported.csv', auth_user_data, auth_user_fields)
    
    # Export company data
    company_fields = [
        "name", "logo", "industry", "serivces", "description", 
        "phone", "email", "create_date", "user_id"
    ]
    company_data = export_company_data()
    write_csv('companies_company_exported.csv', company_data, company_fields)
    
    # Export listing data
    listing_fields = [
        "company_id", "title", "industry", "budget", "duration",
        "description", "requirement", "publish_date", "is_active"
    ]
    listing_data = export_listing_data()
    write_csv('listings_listing_exported.csv', listing_data, listing_fields)
    
    # Export apply data
    apply_fields = [
        "name", "email", "phone", "message",
        "cv", "apply_date", "listing_id", "user_id"
    ]
    apply_data = export_apply_data()
    write_csv('applies_apply_exported.csv', apply_data, apply_fields)
    
    print("\n" + "="*60)
    print("EXPORT COMPLETE!")
    print("="*60)
    print(f"Total auth_user records exported: {len(auth_user_data)}")
    print(f"Total company records exported: {len(company_data)}")
    print(f"Total listing records exported: {len(listing_data)}")
    print(f"Total apply records exported: {len(apply_data)}")
    print("\nFiles saved in 'exported_data/' directory:")
    print("1. auth_user_exported.csv")
    print("2. companies_company_exported.csv")
    print("3. listings_listing_exported.csv")
    print("4. applies_apply_exported.csv")
    print("\n" + "="*60)
    print("COMPARISON INSTRUCTIONS:")
    print("1. Compare these exported files with the generated files in 'dummy_data/'")
    print("2. Use diff tool or Excel to compare the data")
    print("3. Check that file paths (logos and CVs) match the actual files")
    print("4. Verify that all data was imported correctly")
    print("="*60)

if __name__ == "__main__":
    main()