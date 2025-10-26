# Personal Finance Manager

## 📋 Project Overview

A comprehensive console-based Personal Finance Manager that helps users track income, expenses, and generate financial reports. This application demonstrates modular Python programming with robust data management and user authentication.

---

## 🚀 How to Run the Program

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation Steps

1. **Install Required Dependencies**
   ```sh
   pip install -r requirements.txt
   ```
   
   Required packages:
   - pandas==2.3.3
   - numpy==2.3.4
   - python-dateutil==2.9.0.post0

2. **Run the Application**
   ```sh
   python main.py
   ```

3. **First Time Setup**
   - The application will automatically create necessary directories and files
   - users.json will be created to store user accounts
   - database directory will be created for user transaction data

---

## ✨ Feature List

### Core Features

#### 👤 User Management
- **Multi-user Support**: Multiple users can register and maintain separate accounts
- **Secure Authentication**: 
  - Password hashing using SHA-256
  - Secure password input (hidden characters)
  - Password validation (minimum 6 characters, no spaces)
- **User Profiles**: Each user has a unique ID and dedicated transaction storage

#### 💳 Transaction Management
- **Add Transactions**: Record income or expenses with detailed information
  - Date (auto-fills to today if left blank)
  - Type (Income/Expense)
  - Category (Food, Rent, Salary, etc.)
  - Amount (validated for positive numbers)
  - Payment Method (Cash, Card, Bank Transfer, Wallet, Other)
  - Description (optional)
- **View Transactions**: Display all transactions in a formatted list
- **Edit Transactions**: Modify existing transaction details
- **Delete Transactions**: Remove transactions with confirmation prompt
- **Balance Calculation**: Real-time income, expense, and net balance tracking

#### 🔍 Search & Filter
- **Search Transactions**: Find transactions by keyword in category, payment method, or description
- **Advanced Filtering**:
  - Filter by transaction type (Income/Expense)
  - Filter by category
  - Filter by date range (start and end dates)
  - Filter by amount range (min and max)
  - Filter by payment method
  - Multiple filters can be combined

#### 📊 Reports & Analytics
- **Dashboard Summary**: 
  - Total transactions count
  - Total income and expenses
  - Average transaction amount
- **Monthly Reports**: View transactions for a specific month and year
- **Category Breakdown**: See spending grouped by category
- **Spending Trends**: Analyze monthly spending patterns over time

#### 💾 Data Management
- **CSV Export**: Backup transactions to a separate CSV file in `exports/` folder
- **CSV Import**: Import transactions from external CSV files
- **Persistent Storage**: All data automatically saved to CSV files
- **Data Recovery**: Handles corrupted JSON files gracefully

#### 📈 Dashboard Features
- **User Profile Overview**: Display username and account information
- **Financial Summary**: Quick view of total income, expenses, and balance
- **Recent Transactions**: Shows last 3 transactions for quick reference
- **Rent Reminder**: Special alert if rent expense is recorded

### Advanced Features Implemented

1. ✅ **CSV Import/Export** - Full backup and restore functionality
2. ✅ **Dashboard with Financial Summary** - Real-time financial health overview
3. ✅ **Bill Reminders** - Automated rent payment reminders
4. ✅ **Advanced Search & Filter** - Multiple criteria filtering system
5. ✅ **Category Breakdown Reports** - Detailed spending analysis by category

---

## 📖 User Guide

### Getting Started

#### 1. Register a New Account
```
Main Menu → Select Option 1 (Register)
- Enter your name (alphanumeric only)
- Create a password (minimum 6 characters, no spaces)
- Account created successfully!
```

#### 2. Login
```
Main Menu → Select Option 2 (Login)
- Enter your registered name
- Enter your password
- Dashboard will display automatically
```

### Managing Transactions

#### Adding a Transaction
```
Dashboard Menu → Option 2 (Add Transaction)

Example Input:
- Date: 2025-01-15 (or press Enter for today)
- Type: Expense
- Category: Food
- Amount: 45.50
- Payment Method: Card
- Description: Lunch with colleagues
```

#### Viewing All Transactions
```
Dashboard Menu → Option 3 (View Transactions)
```

#### Editing a Transaction
```
Dashboard Menu → Option 4 (Edit Transaction)
1. View all transactions first
2. Enter transaction number to edit
3. Update fields (press Enter to keep current value)
```

#### Deleting a Transaction
```
Dashboard Menu → Option 5 (Delete Transaction)
1. View all transactions first
2. Enter transaction number to delete
3. Confirm deletion (y/n)
```

### Using Reports

#### Access Reports Menu
```
Dashboard Menu → Option 6 (Reports)
```

#### Available Reports:
1. **Dashboard Summary** - Overall financial overview
2. **Monthly Report** - Enter month (1-12) and year
3. **Category Breakdown** - Spending by category
4. **Spending Trends** - Monthly spending analysis
5. **Export to CSV** - Creates backup in `exports/` folder
6. **Import from CSV** - Merge transactions from file

### Search & Filter

#### Search Transactions
```
Dashboard Menu → Option 7 (Search)
- Enter keyword to search in category, payment method, or description
```

#### Filter Transactions
```
Dashboard Menu → Option 8 (Filter)
- Type: Income or Expense (or leave blank)
- Category: specific category (or leave blank)
- Start Date: YYYY-MM-DD format (or leave blank)
- End Date: YYYY-MM-DD format (or leave blank)
- Min Amount: minimum value (or leave blank)
- Max Amount: maximum value (or leave blank)
- Payment Method: specific method (or leave blank)
```

### Data Export/Import

#### Export Transactions
```
Reports Menu → Option 5
- Exports all transactions to: database/[username]_[id]/exports/transactions_export.csv
```

#### Import Transactions
```
Reports Menu → Option 6
- Enter full path to CSV file
- Transactions will be appended to your existing data
```

### Logging Out
```
Dashboard Menu → Option 9 (Logout)
- Returns to main menu
```

---


## 📁 File Structure

```
python-project/
├── main.py                          # Main application entry point
├── requirements.txt                 # Python dependencies
├── users.json                       # User accounts (auto-generated)
├── modules/
│   ├── user_manager.py             # User registration and login
│   ├── transaction_manager.py      # Transaction CRUD operations
│   ├── reports_manager.py          # Reports and analytics
│   ├── dashboard_manager.py        # Dashboard display
│   ├── data_handler.py             # File I/O operations
│   └── utils.py                    # Password hashing utilities
└── database/
    └── [username_userid]/          # Per-user folders
        ├── transactions.csv        # User transaction data
        └── exports/                # Export destination
            └── transactions_export.csv
```

---

## 🎯 Usage Tips

1. **Regular Backups**: Use the export feature weekly to backup your data
2. **Consistent Categories**: Use standardized category names for better reports
3. **Date Format**: Always use YYYY-MM-DD format for dates
4. **Amount Entry**: Enter amounts without currency symbols (e.g., "45.50" not "$45.50")
5. **Search Effectively**: Use partial words in search (e.g., "foo" finds "Food")
6. **Filter Smart**: Combine multiple filters to narrow down results
7. **Review Dashboard**: Check dashboard regularly for financial health overview

---

## 🆘 Troubleshooting

### "No module named 'pandas'" Error
```sh
pip install -r requirements.txt
```

### "File not found" Error on Startup
- Ensure you're running from the project root directory
- Application will auto-create necessary files

### Corrupted users.json
- Application will automatically recreate the file
- Previous user accounts will be lost
- Check for backup files

### CSV Import Not Working
- Verify CSV file has correct columns: Date, Type, Category, Amount, Payment Method, Description
- Ensure file path is absolute or relative to project root
- Check file encoding is UTF-8

### Transactions Not Saving
- Verify write permissions in database/ directory
- Check available disk space
- Ensure CSV file is not open in another program

---
