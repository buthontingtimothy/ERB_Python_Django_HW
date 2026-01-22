import os
import sys
import csv
import django
from pathlib import Path
from datetime import datetime
from django.utils import timezone
import pytz
from datetime import datetime


# Add your project to the Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# Setup Django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from companies.models import Company
from listings.models import Listing
from applies.models import Apply



class CSVImporter:
    def __init__(self, csv_dir='dummy_data'):
        self.csv_dir = csv_dir
        self.import_stats = {
            'success': 0,
            'failed': 0,
            'skipped': 0,
            'total': 0
        }
        self.import_log = []
        
    def log_message(self, level, message, record_id=None):
        """Log import messages with timestamp"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{level}] {message}"
        if record_id:
            log_entry += f" (Record ID: {record_id})"
        print(log_entry)
        self.import_log.append(log_entry)
        
        # Also write to log file
        with open('import_log.txt', 'a') as f:
            f.write(log_entry + '\n')
    
    def setup_database(self):
        """Setup database connection and clear existing data if needed"""
        self.log_message('INFO', 'Setting up database connection...')
        
        try:
            # Test database connection
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            self.log_message('INFO', 'Database connection successful')
            return True
        except Exception as e:
            self.log_message('ERROR', f'Database connection failed: {str(e)}')
            return False
        
    def clear_existing_data(self, confirm=True):
        """Clear existing data from tables and reset sequences"""
        self.log_message('WARNING', 'Clearing existing data from tables...')
        
        # Check if tables have data
        tables = [User, Company, Listing, Apply]
        table_counts = {}
        
        for model in tables:
            count = model.objects.count()
            table_counts[model.__name__] = count
            if count > 0:
                self.log_message('INFO', f'{model.__name__}: {count} records')
        
        if any(count > 0 for count in table_counts.values()):
            if confirm:
                response = input(f"\n⚠️  Database contains data. Clear all and reset sequences? (yes/no): ")
                if response.lower() != 'yes':
                    self.log_message('INFO', 'Data clearance cancelled')
                    return False
            
            # Clear data in reverse order (due to foreign keys)
            self.log_message('INFO', 'Clearing data in safe order...')
            
            try:
                from django.db import connection
                
                # Clear data in reverse order (due to foreign keys)
                Apply.objects.all().delete()
                self.log_message('INFO', 'Cleared Apply table')
                
                Listing.objects.all().delete()
                self.log_message('INFO', 'Cleared Listing table')
                
                Company.objects.all().delete()
                self.log_message('INFO', 'Cleared Company table')
                
                # Don't delete superusers
                User.objects.filter(is_superuser=False).delete()
                self.log_message('INFO', 'Cleared non-superuser Users')
                
                # Reset PostgreSQL sequences for all tables
                self.log_message('INFO', 'Resetting PostgreSQL sequences...')
                
                with connection.cursor() as cursor:
                    # Get all table names
                    tables_to_reset = [
                        'applies_apply',
                        'listings_listing', 
                        'companies_company',
                        'auth_user'
                    ]
                    
                    for table_name in tables_to_reset:
                        try:
                            # Reset the sequence for each table
                            cursor.execute(f"SELECT setval(pg_get_serial_sequence('{table_name}', 'id'), 1, false);")
                            self.log_message('INFO', f'Reset sequence for {table_name}')
                        except Exception as e:
                            self.log_message('WARNING', f'Could not reset sequence for {table_name}: {str(e)}')
                
                self.log_message('SUCCESS', 'All data cleared and sequences reset successfully')
                return True
                
            except Exception as e:
                self.log_message('ERROR', f'Failed to clear data: {str(e)}')
                return False
        else:
            self.log_message('INFO', 'Database is already empty')
            return True
    def validate_csv_file(self, filepath, expected_fields):
        """Validate CSV file structure"""
        if not os.path.exists(filepath):
            self.log_message('ERROR', f'CSV file not found: {filepath}')
            return False
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                actual_fields = reader.fieldnames
                
                if not actual_fields:
                    self.log_message('ERROR', f'CSV file is empty or has no headers: {filepath}')
                    return False
                
                # Check if all expected fields are present
                missing_fields = set(expected_fields) - set(actual_fields)
                if missing_fields:
                    self.log_message('ERROR', f'Missing fields in {filepath}: {missing_fields}')
                    return False
                
                # Count rows
                rows = list(reader)
                self.log_message('INFO', f'CSV validation passed: {len(rows)} records, {len(actual_fields)} fields')
                return True
                
        except Exception as e:
            self.log_message('ERROR', f'Error reading CSV file {filepath}: {str(e)}')
            return False
                
    def import_users(self):
        def make_aware(date_str):
            if not date_str or date_str.strip() == '':
                return None
            try:
                # Parse the naive datetime
                naive_dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                # Make it aware (using UTC)
                return timezone.make_aware(naive_dt, pytz.UTC)
            except:
                return None
        """Import User data from auth_user.csv"""
        self.log_message('INFO', '=' * 50)
        self.log_message('INFO', 'STARTING USER IMPORT')
        self.log_message('INFO', '=' * 50)
        
        csv_file = os.path.join(self.csv_dir, 'auth_user.csv')
        expected_fields = [
            'password', 'last_login', 'is_superuser', 'username', 
            'first_name', 'last_name', 'email', 'is_staff', 
            'is_active', 'date_joined'
        ]
        
        # Validate CSV
        if not self.validate_csv_file(csv_file, expected_fields):
            self.log_message('ERROR', 'User import aborted due to CSV validation failure')
            return False
        
        imported_count = 0
        failed_count = 0
        skipped_count = 0
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for i, row in enumerate(reader, 1):
                    try:
                        # Check if user already exists
                        if User.objects.filter(username=row['username']).exists():
                            self.log_message('WARNING', f'User {row["username"]} already exists, skipping')
                            skipped_count += 1
                            continue
                        
                        # Convert string booleans to actual booleans
                        row['is_superuser'] = row['is_superuser'].lower() == 'true' or row['is_superuser'] == '1'
                        row['is_staff'] = row['is_staff'].lower() == 'true' or row['is_staff'] == '1'
                        row['is_active'] = row['is_active'].lower() == 'true' or row['is_active'] == '1'
                        
                        # Convert empty last_login to None
                        if not row['last_login'] or row['last_login'].strip() == '':
                            row['last_login'] = None
                                            
                        # Create user with already-hashed password
                        # We can't use create_user() because it expects plain text password
                        # Instead, we create the user object and set the password field directly
                        user = User(
                            username=row['username'],
                            email=row['email'],
                            password=row['password'],  # Already hashed
                            first_name=row['first_name'],
                            last_name=row['last_name'],
                            is_superuser=row['is_superuser'],
                            is_staff=row['is_staff'],
                            is_active=row['is_active'],
                            date_joined=make_aware(row['date_joined'])
                        )
                        
                        # Set last_login if provided
                        if row['last_login']:
                            user.last_login = make_aware(row['last_login'])
                        
                        # Save the user
                        user.save()
                        
                        imported_count += 1
                        if imported_count % 10 == 0:
                            self.log_message('INFO', f'Imported {imported_count} users...')
                            
                    except IntegrityError as e:
                        self.log_message('ERROR', f'Integrity error for user {row.get("username", "Unknown")}: {str(e)}')
                        failed_count += 1
                    except Exception as e:
                        self.log_message('ERROR', f'Error importing user row {i}: {str(e)}')
                        failed_count += 1
            
            self.log_message('SUCCESS', f'User import completed: {imported_count} imported, {failed_count} failed, {skipped_count} skipped')
            self.import_stats['success'] += imported_count
            self.import_stats['failed'] += failed_count
            self.import_stats['skipped'] += skipped_count
            self.import_stats['total'] += imported_count + failed_count + skipped_count
            
            return imported_count > 0
            
        except Exception as e:
            self.log_message('ERROR', f'Fatal error during user import: {str(e)}')
            return False
    
    def import_companies(self):
        """Import Company data from companies_company.csv"""
        self.log_message('INFO', '=' * 50)
        self.log_message('INFO', 'STARTING COMPANY IMPORT')
        self.log_message('INFO', '=' * 50)
        
        csv_file = os.path.join(self.csv_dir, 'companies_company.csv')
        expected_fields = [
            'name', 'logo', 'industry', 'serivces', 'description',
            'phone', 'email', 'create_date', 'user_id'
        ]
        
        # Validate CSV
        if not self.validate_csv_file(csv_file, expected_fields):
            self.log_message('ERROR', 'Company import aborted due to CSV validation failure')
            return False
        
        imported_count = 0
        failed_count = 0
        skipped_count = 0
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for i, row in enumerate(reader, 1):
                    try:
                        # Check if company already exists by email
                        if Company.objects.filter(email=row['email']).exists():
                            self.log_message('WARNING', f'Company with email {row["email"]} already exists, skipping')
                            skipped_count += 1
                            continue
                        
                        # Get the user
                        try:
                            user = User.objects.get(id=int(row['user_id']))
                        except User.DoesNotExist:
                            self.log_message('ERROR', f'User with ID {row["user_id"]} not found for company {row["name"]}')
                            failed_count += 1
                            continue
                        
                        # Check if user already has a company
                        if Company.objects.filter(user=user).exists():
                            self.log_message('WARNING', f'User {user.username} already has a company, skipping')
                            skipped_count += 1
                            continue
                        
                        # Create company
                        company = Company.objects.create(
                            name=row['name'],
                            logo=row['logo'],
                            industry=row['industry'],
                            serivces=row['serivces'],
                            description=row['description'],
                            phone=row['phone'],
                            email=row['email'],
                            create_date=row['create_date'],
                            user=user
                        )
                        
                        imported_count += 1
                        if imported_count % 5 == 0:
                            self.log_message('INFO', f'Imported {imported_count} companies...')
                            
                    except IntegrityError as e:
                        self.log_message('ERROR', f'Integrity error for company {row.get("name", "Unknown")}: {str(e)}')
                        failed_count += 1
                    except Exception as e:
                        self.log_message('ERROR', f'Error importing company row {i}: {str(e)}')
                        failed_count += 1
            
            self.log_message('SUCCESS', f'Company import completed: {imported_count} imported, {failed_count} failed, {skipped_count} skipped')
            self.import_stats['success'] += imported_count
            self.import_stats['failed'] += failed_count
            self.import_stats['skipped'] += skipped_count
            self.import_stats['total'] += imported_count + failed_count + skipped_count
            
            return imported_count > 0
            
        except Exception as e:
            self.log_message('ERROR', f'Fatal error during company import: {str(e)}')
            return False
    
    def import_listings(self):
        """Import Listing data from listings_listing.csv"""
        self.log_message('INFO', '=' * 50)
        self.log_message('INFO', 'STARTING LISTING IMPORT')
        self.log_message('INFO', '=' * 50)
        
        csv_file = os.path.join(self.csv_dir, 'listings_listing.csv')
        expected_fields = [
            'company_id', 'title', 'industry', 'budget', 'duration',
            'description', 'requirement', 'publish_date', 'is_active'
        ]
        
        # Validate CSV
        if not self.validate_csv_file(csv_file, expected_fields):
            self.log_message('ERROR', 'Listing import aborted due to CSV validation failure')
            return False
        
        imported_count = 0
        failed_count = 0
        skipped_count = 0
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for i, row in enumerate(reader, 1):
                    try:
                        # Get the company
                        try:
                            company = Company.objects.get(id=int(row['company_id']))
                        except Company.DoesNotExist:
                            self.log_message('ERROR', f'Company with ID {row["company_id"]} not found for listing {row["title"]}')
                            failed_count += 1
                            continue
                        
                        # Convert is_active to boolean
                        is_active = row['is_active'].lower() == 'true' or row['is_active'] == '1'
                        
                        # Create listing
                        listing = Listing.objects.create(
                            company=company,
                            title=row['title'],
                            industry=row['industry'],
                            budget=row['budget'],
                            duration=row['duration'],
                            description=row['description'],
                            requirement=row['requirement'],
                            publish_date=row['publish_date'],
                            is_active=is_active
                        )
                        
                        imported_count += 1
                        if imported_count % 10 == 0:
                            self.log_message('INFO', f'Imported {imported_count} listings...')
                            
                    except IntegrityError as e:
                        self.log_message('ERROR', f'Integrity error for listing {row.get("title", "Unknown")}: {str(e)}')
                        failed_count += 1
                    except Exception as e:
                        self.log_message('ERROR', f'Error importing listing row {i}: {str(e)}')
                        failed_count += 1
            
            self.log_message('SUCCESS', f'Listing import completed: {imported_count} imported, {failed_count} failed, {skipped_count} skipped')
            self.import_stats['success'] += imported_count
            self.import_stats['failed'] += failed_count
            self.import_stats['skipped'] += skipped_count
            self.import_stats['total'] += imported_count + failed_count + skipped_count
            
            return imported_count > 0
            
        except Exception as e:
            self.log_message('ERROR', f'Fatal error during listing import: {str(e)}')
            return False
    
    def import_applies(self):
        """Import Apply data from applies_apply.csv"""
        self.log_message('INFO', '=' * 50)
        self.log_message('INFO', 'STARTING APPLY IMPORT')
        self.log_message('INFO', '=' * 50)
        
        csv_file = os.path.join(self.csv_dir, 'applies_apply.csv')
        expected_fields = [
            'listing_id', 'name', 'email', 'phone', 'message',
            'cv', 'apply_date', 'user_id'
        ]
        
        # Validate CSV
        if not self.validate_csv_file(csv_file, expected_fields):
            self.log_message('ERROR', 'Apply import aborted due to CSV validation failure')
            return False
        
        imported_count = 0
        failed_count = 0
        skipped_count = 0
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for i, row in enumerate(reader, 1):
                    try:
                        # Get the listing
                        try:
                            listing = Listing.objects.get(id=int(row['listing_id']))
                        except Listing.DoesNotExist:
                            self.log_message('ERROR', f'Listing with ID {row["listing_id"]} not found for apply from {row["name"]}')
                            failed_count += 1
                            continue
                        
                        # Get the user
                        try:
                            user = User.objects.get(id=int(row['user_id']))
                        except User.DoesNotExist:
                            self.log_message('ERROR', f'User with ID {row["user_id"]} not found for apply from {row["name"]}')
                            failed_count += 1
                            continue
                        
                        # Create apply
                        apply = Apply.objects.create(
                            listing=listing,
                            name=row['name'],
                            email=row['email'],
                            phone=row['phone'],
                            message=row['message'],
                            cv=row['cv'],
                            apply_date=row['apply_date'],
                            user=user
                        )
                        
                        imported_count += 1
                        if imported_count % 10 == 0:
                            self.log_message('INFO', f'Imported {imported_count} applications...')
                            
                    except IntegrityError as e:
                        self.log_message('ERROR', f'Integrity error for apply from {row.get("name", "Unknown")}: {str(e)}')
                        failed_count += 1
                    except Exception as e:
                        self.log_message('ERROR', f'Error importing apply row {i}: {str(e)}')
                        failed_count += 1
            
            self.log_message('SUCCESS', f'Apply import completed: {imported_count} imported, {failed_count} failed, {skipped_count} skipped')
            self.import_stats['success'] += imported_count
            self.import_stats['failed'] += failed_count
            self.import_stats['skipped'] += skipped_count
            self.import_stats['total'] += imported_count + failed_count + skipped_count
            
            return imported_count > 0
            
        except Exception as e:
            self.log_message('ERROR', f'Fatal error during apply import: {str(e)}')
            return False
    
    def validate_import(self):
        """Validate that import was successful by checking counts"""
        self.log_message('INFO', '=' * 50)
        self.log_message('INFO', 'VALIDATING IMPORT RESULTS')
        self.log_message('INFO', '=' * 50)
        
        validation_results = {}
        
        # Count actual records in database
        try:
            validation_results['User'] = User.objects.count()
            validation_results['Company'] = Company.objects.count()
            validation_results['Listing'] = Listing.objects.count()
            validation_results['Apply'] = Apply.objects.count()
            
            # Count active vs inactive listings
            active_listings = Listing.objects.filter(is_active=True).count()
            inactive_listings = Listing.objects.filter(is_active=False).count()
            
            self.log_message('INFO', f'Database counts after import:')
            self.log_message('INFO', f'  Users: {validation_results["User"]}')
            self.log_message('INFO', f'  Companies: {validation_results["Company"]}')
            self.log_message('INFO', f'  Listings: {validation_results["Listing"]} ({active_listings} active, {inactive_listings} inactive)')
            self.log_message('INFO', f'  Applications: {validation_results["Apply"]}')
            
            # Check relationships
            self.log_message('INFO', 'Checking relationships...')
            
            # Check companies without users
            companies_without_users = Company.objects.filter(user__isnull=True).count()
            if companies_without_users > 0:
                self.log_message('WARNING', f'{companies_without_users} companies have no associated user')
            
            # Check listings without companies
            listings_without_companies = Listing.objects.filter(company__isnull=True).count()
            if listings_without_companies > 0:
                self.log_message('WARNING', f'{listings_without_companies} listings have no associated company')
            
            # Check applies without listings or users
            applies_without_listings = Apply.objects.filter(listing__isnull=True).count()
            applies_without_users = Apply.objects.filter(user__isnull=True).count()
            
            if applies_without_listings > 0:
                self.log_message('WARNING', f'{applies_without_listings} applications have no associated listing')
            if applies_without_users > 0:
                self.log_message('WARNING', f'{applies_without_users} applications have no associated user')
            
            return validation_results
            
        except Exception as e:
            self.log_message('ERROR', f'Validation failed: {str(e)}')
            return None
    
    def generate_report(self):
        """Generate import summary report"""
        self.log_message('INFO', '=' * 50)
        self.log_message('INFO', 'IMPORT SUMMARY REPORT')
        self.log_message('INFO', '=' * 50)
        
        report = f"""
IMPORT REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

OVERALL STATISTICS:
------------------
Total Records Processed: {self.import_stats['total']}
Successfully Imported: {self.import_stats['success']}
Failed: {self.import_stats['failed']}
Skipped: {self.import_stats['skipped']}
Success Rate: {(self.import_stats['success'] / self.import_stats['total'] * 100):.1f}%

DATABASE COUNTS:
----------------
"""
        
        try:
            report += f"Users: {User.objects.count()}\n"
            report += f"Companies: {Company.objects.count()}\n"
            report += f"Listings: {Listing.objects.count()}\n"
            report += f"Applications: {Apply.objects.count()}\n"
        except Exception as e:
            report += f"Error getting counts: {str(e)}\n"
        
        report += f"""
LOG FILE:
---------
Import log saved to: import_log.txt
"""
        
        print(report)
        
        # Save report to file
        with open('import_report.txt', 'w') as f:
            f.write(report)
        
        return report
    
    def run_import(self, clear_existing=False):
        """Run the complete import process"""
        print("\n" + "=" * 60)
        print("📥 CSV TO POSTGRESQL IMPORT SCRIPT")
        print("=" * 60)
        print(f"CSV Directory: {self.csv_dir}")
        print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Setup database
        if not self.setup_database():
            return False
        
        # Clear existing data if requested
        if clear_existing:
            if not self.clear_existing_data():
                return False
        else:
            # Just check if we have data
            self.clear_existing_data(confirm=False)
        
        # Import in correct order (respecting foreign key constraints)
        import_steps = [
            ('Users', self.import_users),
            ('Companies', self.import_companies),
            ('Listings', self.import_listings),
            ('Applications', self.import_applies)
        ]
        
        # Ask for confirmation
        print("\n⚠️  IMPORT CONFIRMATION")
        print("=" * 40)
        print("This will import data in the following order:")
        for i, (name, _) in enumerate(import_steps, 1):
            print(f"  {i}. {name}")
        
        response = input("\nProceed with import? (yes/no): ")
        if response.lower() != 'yes':
            self.log_message('INFO', 'Import cancelled by user')
            return False
        
        # Execute import steps
        all_successful = True
        for step_name, step_function in import_steps:
            print(f"\n{'='*60}")
            print(f"Step: {step_name}")
            print(f"{'='*60}")
            
            if not step_function():
                self.log_message('ERROR', f'{step_name} import failed!')
                # Ask whether to continue
                response = input(f"\n⚠️  {step_name} import had issues. Continue? (yes/no): ")
                if response.lower() != 'yes':
                    self.log_message('INFO', f'Import stopped after {step_name}')
                    all_successful = False
                    break
            else:
                self.log_message('SUCCESS', f'{step_name} import completed')
        
        # Validate import results
        if all_successful:
            self.validate_import()
            self.generate_report()
            
            print("\n" + "=" * 60)
            print("🎉 IMPORT COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            print("\nCheck 'import_report.txt' for detailed summary.")
            print("Check 'import_log.txt' for detailed log of operations.")
        else:
            print("\n" + "=" * 60)
            print("⚠️  IMPORT COMPLETED WITH ERRORS")
            print("=" * 60)
            print("\nCheck 'import_log.txt' for error details.")
        
        return all_successful

# Quick test function
def quick_test_connection():
    """Test database connection and models"""
    try:
        print("Testing database connection...")
        
        # Test User model
        user_count = User.objects.count()
        print(f"✓ User model accessible ({user_count} users)")
        
        # Test Company model
        company_count = Company.objects.count()
        print(f"✓ Company model accessible ({company_count} companies)")
        
        # Test Listing model
        listing_count = Listing.objects.count()
        print(f"✓ Listing model accessible ({listing_count} listings)")
        
        # Test Apply model
        apply_count = Apply.objects.count()
        print(f"✓ Apply model accessible ({apply_count} applications)")
        
        print("\n✓ All models are accessible and database connection is working!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nMake sure:")
        print("1. Django is properly configured")
        print("2. Database settings are correct")
        print("3. Models exist in the correct apps")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Import CSV data into Django PostgreSQL database')
    parser.add_argument('--test', action='store_true', help='Test database connection only')
    parser.add_argument('--clear', action='store_true', help='Clear existing data before import')
    parser.add_argument('--dir', type=str, default='dummy_data', help='Directory containing CSV files')
    parser.add_argument('--step', type=str, choices=['users', 'companies', 'listings', 'applies'],
                        help='Import only specific step')
    
    args = parser.parse_args()
    
    # Run connection test
    if args.test:
        if quick_test_connection():
            print("\n✅ Database connection test passed!")
        else:
            print("\n❌ Database connection test failed!")
        sys.exit(0)
    
    # Create importer instance
    importer = CSVImporter(csv_dir=args.dir)
    
    # Run specific step or full import
    if args.step:
        print(f"\nRunning single step: {args.step}")
        
        # Setup database first
        if not importer.setup_database():
            sys.exit(1)
        
        # Run specific step
        if args.step == 'users':
            success = importer.import_users()
        elif args.step == 'companies':
            success = importer.import_companies()
        elif args.step == 'listings':
            success = importer.import_listings()
        elif args.step == 'applies':
            success = importer.import_applies()
        
        if success:
            print(f"\n✅ {args.step.capitalize()} import completed!")
        else:
            print(f"\n❌ {args.step.capitalize()} import failed!")
            sys.exit(1)
    else:
        # Run full import
        success = importer.run_import(clear_existing=args.clear)
        if not success:
            sys.exit(1)