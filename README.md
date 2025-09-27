# 📚 Modern Library Management System

> A comprehensive, modern library management system built with Python and Tkinter, featuring an ultra-dark theme, enhanced search capabilities, and professional UI design.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-orange.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)

## ✨ Features

### 🎨 **Modern UI/UX Design**
- **Ultra-dark professional theme** with high contrast
- **Large, accessible buttons** with 36px icons
- **Responsive layout** that adapts to different screen sizes
- **Professional color palette** designed for enterprise use
- **Smooth hover effects** and visual feedback

### 🔍 **Enhanced Search System**
- **Real-time dropdown search** as you type
- **Multiple search criteria** (Title, Author, ID, Course, etc.)
- **Smart filtering** (Available books only, Issued books only)
- **Visual selection** from search results (up to 10 matches)
- **Context-aware search** for different operations

### 📖 **Complete Book Management**
- **Add Books** - Professional form with validation
- **Edit Books** - Search, select, and modify with auto-population
- **Delete Books** - Safe deletion with detailed confirmation
- **View All Books** - Modern table with status indicators
- **Advanced Search** - Find books by any criteria with detailed view

### 📚 **Enhanced Issue/Return System**
- **2-Step Issue Process**:
  1. Search and select student (Name, ERP ID, Roll Number, Course)
  2. Search and select available book (Title, Author, Book ID)
- **Smart Return Process**:
  - Search issued books by any criteria
  - Shows student info and issue date
  - One-click return with confirmation

### 👥 **Student Management**
- **View all students** with complete information
- **Search students** by multiple criteria
- **Track issued books** per student
- **Manage student records** efficiently

### 📊 **Live Dashboard**
- **Real-time statistics** (Total Books, Available, Issued, Students)
- **Visual charts** (Pie chart for book status, Bar chart for metrics)
- **Color-coded metrics** for quick overview
- **Professional card-based layout**

### 🔐 **Secure Authentication**
- **Username-based login** system
- **Multiple admin accounts** with different access levels
- **Secure password storage** in SQLite database

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Required packages: `tkinter`, `sqlite3`, `PIL` (Pillow)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/modern-library-system.git
   cd modern-library-system
   ```

2. **Install dependencies**
   ```bash
   pip install Pillow
   ```
   > Note: `tkinter` and `sqlite3` come with Python by default

3. **Run the application**
   ```bash
   python FullFunctionalModernLibrary.py
   ```

### Default Login Credentials

| Username | Password  | Role          |
|----------|-----------|---------------|
| glitch   | admin123  | Main Admin    |
| sarah    | sarah2024 | Admin         |
| mike     | mike2024  | Admin         |
| emily    | emily2024 | Admin         |
| david    | david2024 | Admin         |

## 📱 Screenshots

### Dashboard
*Professional dashboard with live statistics and visual charts*

### Enhanced Search
*Real-time dropdown search with multiple criteria*

### Issue Book Process
*2-step guided process for issuing books*

### Book Management
*Modern table view with status indicators*

## 🛠️ Technical Details

### Architecture
- **Frontend**: Tkinter with custom modern styling
- **Backend**: SQLite3 database with three tables
- **Icons**: Professional 40x40px PNG icons
- **Design**: Mobile-first responsive approach

### Database Schema

#### Admin Table (`admin.db`)
```sql
- User_ID (INTEGER)
- Name (CHAR)
- Password (CHAR)
- email (CHAR)
- phone_no (INTEGER)
- username (VARCHAR) -- For login
```

#### Books Table (`storebook.db`)
```sql
- Book_ID (INTEGER)
- Title (CHAR)
- Author (CHAR)
- Edition (CHAR)
- Price (INTEGER)
- Issue (CHAR) -- Issue date
- ID (INTEGER) -- Student ERP_ID
```

#### Students Table (`students.db`)
```sql
- ERP_ID (INTEGER)
- Name (CHAR)
- Course (CHAR)
- year (CHAR)
- Roll_no (INTEGER)
- e-mail (CHAR)
- Contact_no (INTEGER)
- College (CHAR)
- From_date (DATE)
- To_date (CHAR)
- submit_date (CHAR)
- Charge (INTEGER)
- No_book (INTEGER) -- Number of books issued
```

### Color Palette
```css
Primary: #1e40af (Dark Blue)
Secondary: #5b21b6 (Dark Purple)
Success: #065f46 (Dark Green)
Warning: #92400e (Dark Orange)
Danger: #991b1b (Dark Red)
Background: #d1d5db (Light Gray)
Surface: #e5e7eb (White-ish)
Text: #030712 (Almost Black)
```

## 📖 Usage Guide

### Adding a Book
1. Click "Add Book" from dashboard
2. Fill in all required fields (ID, Title, Author, Edition, Price)
3. Click "📖 Add New Book"
4. Book is added to catalog

### Issuing a Book
1. Click "Issue Book" from dashboard
2. **Step 1**: Search and select student
3. **Step 2**: Search and select available book
4. Click "📖 Issue Selected Book"
5. Confirm the issue

### Returning a Book
1. Click "Return Book" from dashboard
2. Search for issued book (by title, author, ID, or student)
3. Select book from dropdown
4. Click "📚 Return Selected Book"
5. Confirm the return

### Searching Books
1. Click "Search Books" from dashboard
2. Type in search box (real-time results appear)
3. Click on any result to select
4. Click "📖 Show Selected Book Details"
5. View complete book information

## 🔧 Customization

### Changing Colors
Edit the `self.colors` dictionary in `FullFunctionalModernLibrary.py`:
```python
self.colors = {
    'primary': '#your-color',
    'secondary': '#your-color',
    # ... etc
}
```

### Adding New Features
The codebase is modular and well-documented. Key areas:
- `create_button()` - For new buttons
- `create_search_dropdown()` - For search functionality
- Database methods - For data operations

### Custom Icons
Replace icons in `modern_icons_api/` folder with your own 40x40px PNG files.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Glitch**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

## 🙏 Acknowledgments

- Modern UI design inspired by contemporary web applications
- Icons generated using professional design principles
- Color palette based on 2024 design trends

## 📞 Support

If you have any questions or need help, please:
1. Check the [User Guide](USER_GUIDE.md)
2. Review the [Enhanced Search Documentation](ENHANCED_SEARCH_SYSTEM.md)
3. Open an issue on GitHub
4. Contact the author

---

**⭐ Star this repository if you find it helpful!**
