# Data Verification Scripts

This directory contains scripts to verify that data imported into your Django database matches the generated dummy data.

## Files Created

1. **`export_data_to_csv.py`** - Exports data from your Django database to CSV files
2. **`compare_data.py`** - Compares generated dummy data with exported database data
3. **`verify_imported_data.py`** - Main script that runs both export and comparison

## Prerequisites

1. Django project must be set up and running
2. Database must have data imported (from `dummy_data/` CSV files)
3. Python environment with Django installed

## How to Use

### Option 1: Run the complete verification

```bash
python verify_imported_data.py
```

This will:
1. Check if your database has data
2. Export database data to `exported_data/` directory
3. Compare with generated data in `dummy_data/` directory
4. Provide a summary of differences

### Option 2: Run individual steps

#### Step 1: Export data from database
```bash
python export_data_to_csv.py
```

This creates CSV files in `exported_data/` directory:
- `auth_user_exported.csv`
- `companies_company_exported.csv`
- `listings_listing_exported.csv`
- `applies_apply_exported.csv`

#### Step 2: Compare with generated data
```bash
python compare_data.py
```

This compares:
- `dummy_data/auth_user.csv` vs `exported_data/auth_user_exported.csv`
- `dummy_data/companies_company.csv` vs `exported_data/companies_company_exported.csv`
- `dummy_data/listings_listing.csv` vs `exported_data/listings_listing_exported.csv`
- `dummy_data/applies_apply.csv` vs `exported_data/applies_apply_exported.csv`

## Expected Differences

Some differences between generated and exported data are normal:

1. **Passwords**: 
   - Generated data: Plain text passwords ("user123", "company123")
   - Database: Hashed passwords (Django's make_password)
   - This is expected and correct!

2. **Auto-generated dates**:
   - Generated data: Random dates within specified ranges
   - Database: Actual import timestamps
   - May differ by seconds/minutes

3. **IDs**:
   - Generated data: Sequential IDs starting from 1
   - Database: Actual database IDs (should match if imported in order)

4. **File paths**:
   - Should match exactly between generated and exported data
   - Scripts check if logo and CV files exist at the specified paths

## Manual Comparison

For detailed comparison, you can:

1. **Use diff command**:
   ```bash
   diff -u dummy_data/ exported_data/
   ```

2. **Use Excel or Google Sheets**:
   - Open both CSV files side by side
   - Compare specific columns

3. **Check file existence**:
   ```bash
   # Check if logo files exist
   grep -o 'photos/.*\.png' exported_data/companies_company_exported.csv | xargs -I {} ls -la {}
   
   # Check if CV files exist
   grep -o 'cv/.*\.pdf' exported_data/applies_apply_exported.csv | xargs -I {} ls -la {}
   ```

## Troubleshooting

### Error: "No data found in database"
- Make sure you've imported the CSV files into your database
- Check that Django migrations are applied
- Verify database connection settings

### Error: "ModuleNotFoundError: No module named 'django'"
- Activate your virtual environment
- Install Django: `pip install django`

### Error: "File not found" when comparing
- Make sure `generate_dummy_data.py` was run first
- Check that `dummy_data/` directory exists with CSV files

### File paths don't match
- Check that logo and CV files were generated
- Verify the directory structure matches Django's `upload_to` pattern
- Ensure files were not moved or deleted

## Script Details

### `export_data_to_csv.py`
- Exports data from Django models to CSV
- Matches the exact format of `generate_dummy_data.py`
- Handles file paths for logos and CVs
- Preserves field order for easy comparison

### `compare_data.py`
- Compares record counts and field names
- Shows sample data differences
- Checks if referenced files (logos, CVs) exist
- Provides detailed mismatch reports

### `verify_imported_data.py`
- Orchestrates the entire verification process
- Checks database connectivity first
- Runs export and comparison
- Provides clear success/failure messages

## Example Output

```
==============================================================
VERIFYING IMPORTED DATA
==============================================================

Step 1: Checking if database has data...
  Users in database: 330
  Companies in database: 30
  Listings in database: 120
  Applies in database: 1800
✓ Database contains data

Step 2: Exporting data from database to CSV...
==============================================================
EXPORTING DATABASE DATA TO CSV FILES
==============================================================
Exporting auth_user data...
Exported 330 records to exported_data/auth_user_exported.csv
...
✓ Data exported successfully

Step 3: Comparing generated data with exported data...
==============================================================
COMPARING GENERATED DATA WITH EXPORTED DATABASE DATA
==============================================================

Comparing:
  Generated: dummy_data/auth_user.csv
  Exported:  exported_data/auth_user_exported.csv
------------------------------------------------------------
Generated records: 330
Exported records:  330
✓ Record counts match
✓ Field names match
...
✓ Comparison completed

==============================================================
VERIFICATION COMPLETE
==============================================================
```