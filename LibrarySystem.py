import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime, date
import os

class FullFunctionalModernLibrary:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("📚 Complete Library System")
        self.root.geometry("1400x900")
        self.root.configure(bg='#d1d5db')
        
        # Ultra dark modern color palette - Even Darker
        self.colors = {
            'primary': '#1e40af',        # Even darker blue
            'primary_dark': '#1e3a8a',   # Ultra ultra dark blue
            'secondary': '#5b21b6',      # Even darker purple
            'success': '#065f46',        # Even darker green
            'warning': '#92400e',        # Even darker orange
            'danger': '#991b1b',         # Even darker red
            'info': '#0c4a6e',          # Even darker cyan
            'dark': '#030712',          # Almost black
            'light': '#9ca3af',         # Even darker light gray
            'background': '#d1d5db',     # Even darker background
            'surface': '#e5e7eb',        # Even darker surface
            'border': '#6b7280',         # Even darker border
            'text': '#030712',           # Almost black text
            'text_secondary': '#1f2937', # Even darker secondary text
        }
        
        # Typography
        self.fonts = {
            'display': ('Segoe UI', 24, 'bold'),
            'h1': ('Segoe UI', 20, 'bold'),
            'h2': ('Segoe UI', 16, 'bold'),
            'h3': ('Segoe UI', 14, 'bold'),
            'body': ('Segoe UI', 11),
            'small': ('Segoe UI', 9),
            'button': ('Segoe UI', 14, 'bold'),
        }
        
        self.current_screen = None
        self.setup_login_screen()
        self.root.mainloop()
    
    def clear_screen(self):
        if self.current_screen:
            self.current_screen.destroy()
    
    def load_icon(self, icon_name, size=(40, 40)):
        try:
            icon_path = f"modern_icons/{icon_name}.png"
            if os.path.exists(icon_path):
                from PIL import Image, ImageTk
                img = Image.open(icon_path)
                img = img.resize(size, Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(img)
        except:
            pass
        return None
    
    def create_button(self, parent, text, command, style='primary', width=None, icon=None):
        styles = {
            'primary': {'bg': self.colors['primary'], 'fg': 'white', 'hover': self.colors['primary_dark']},
            'secondary': {'bg': self.colors['secondary'], 'fg': 'white', 'hover': '#7c3aed'},
            'success': {'bg': self.colors['success'], 'fg': 'white', 'hover': '#059669'},
            'warning': {'bg': self.colors['warning'], 'fg': 'white', 'hover': '#d97706'},
            'danger': {'bg': self.colors['danger'], 'fg': 'white', 'hover': '#dc2626'},
            'outline': {'bg': self.colors['surface'], 'fg': self.colors['primary'], 'hover': self.colors['light']}
        }
        
        config = styles.get(style, styles['primary'])
        icon_img = self.load_icon(icon, (36, 36)) if icon else None
        
        btn = tk.Button(
            parent, text=text, command=command, font=self.fonts['button'],
            bg=config['bg'], fg=config['fg'], activebackground=config['hover'],
            activeforeground=config['fg'], relief='flat', bd=0, cursor='hand2',
            pady=18, padx=40
        )
        
        if width: btn.config(width=width)
        if icon_img:
            btn.config(image=icon_img, compound='left')
            btn.image = icon_img
        
        def on_enter(e): btn.config(bg=config['hover'])
        def on_leave(e): btn.config(bg=config['bg'])
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def create_entry(self, parent, placeholder="", show=None):
        frame = tk.Frame(parent, bg=self.colors['surface'], relief='solid', bd=1)
        entry = tk.Entry(frame, font=self.fonts['body'], bg=self.colors['surface'],
                        fg=self.colors['text'], relief='flat', bd=10, show=show)
        entry.pack(fill='both', expand=True)
        
        if placeholder:
            entry.insert(0, placeholder)
            entry.config(fg=self.colors['text_secondary'])
            
            def on_focus_in(e):
                if entry.get() == placeholder:
                    entry.delete(0, tk.END)
                    entry.config(fg=self.colors['text'])
            
            def on_focus_out(e):
                if not entry.get():
                    entry.insert(0, placeholder)
                    entry.config(fg=self.colors['text_secondary'])
            
            entry.bind("<FocusIn>", on_focus_in)
            entry.bind("<FocusOut>", on_focus_out)
        
        return frame, entry
    
    def create_search_dropdown(self, parent, placeholder="", search_type="books"):
        """Create an enhanced search entry with dropdown results"""
        # Main container
        search_container = tk.Frame(parent, bg=self.colors['surface'])
        
        # Search entry
        entry_frame = tk.Frame(search_container, bg=self.colors['surface'], relief='solid', bd=1)
        entry_frame.pack(fill='x')
        
        entry = tk.Entry(entry_frame, font=self.fonts['body'], bg=self.colors['surface'],
                        fg=self.colors['text'], relief='flat', bd=10)
        entry.pack(fill='both', expand=True)
        
        # Dropdown frame (initially hidden)
        dropdown_frame = tk.Frame(search_container, bg=self.colors['surface'], relief='solid', bd=1)
        
        # Listbox for results
        listbox = tk.Listbox(dropdown_frame, font=self.fonts['body'], bg=self.colors['surface'],
                           fg=self.colors['text'], selectbackground=self.colors['primary'],
                           relief='flat', bd=0, height=6)
        listbox.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Store references
        search_container.entry = entry
        search_container.dropdown_frame = dropdown_frame
        search_container.listbox = listbox
        search_container.search_type = search_type
        search_container.selected_data = None
        
        # Placeholder functionality
        if placeholder:
            entry.insert(0, placeholder)
            entry.config(fg=self.colors['text_secondary'])
            
            def on_focus_in(e):
                if entry.get() == placeholder:
                    entry.delete(0, tk.END)
                    entry.config(fg=self.colors['text'])
            
            def on_focus_out(e):
                if not entry.get():
                    entry.insert(0, placeholder)
                    entry.config(fg=self.colors['text_secondary'])
                    dropdown_frame.pack_forget()
            
            entry.bind("<FocusIn>", on_focus_in)
            entry.bind("<FocusOut>", on_focus_out)
        
        # Search functionality
        def on_key_release(e):
            search_term = entry.get().strip()
            if search_term and search_term != placeholder:
                self.perform_dropdown_search(search_container, search_term)
            else:
                dropdown_frame.pack_forget()
        
        def on_listbox_select(e):
            selection = listbox.curselection()
            if selection:
                selected_text = listbox.get(selection[0])
                # Store the full data for the selected item
                if hasattr(search_container, 'search_results'):
                    search_container.selected_data = search_container.search_results[selection[0]]
                
                # Update entry with selected text
                entry.delete(0, tk.END)
                entry.insert(0, selected_text)
                entry.config(fg=self.colors['text'])
                dropdown_frame.pack_forget()
        
        entry.bind("<KeyRelease>", on_key_release)
        listbox.bind("<<ListboxSelect>>", on_listbox_select)
        
        return search_container
    
    def perform_dropdown_search(self, search_container, search_term):
        """Perform search and show dropdown results"""
        try:
            if search_container.search_type == "books":
                results = self.search_books_data(search_term)
            elif search_container.search_type == "available_books":
                results = self.search_available_books_data(search_term)
            elif search_container.search_type == "issued_books":
                results = self.search_issued_books_data(search_term)
            elif search_container.search_type == "students":
                results = self.search_students_data(search_term)
            else:
                results = []
            
            # Store results and update listbox
            search_container.search_results = results
            search_container.listbox.delete(0, tk.END)
            
            if results:
                for result in results[:10]:  # Limit to 10 results
                    if search_container.search_type == "books" or search_container.search_type == "available_books":
                        display_text = f"{result[1]} - {result[2]} (ID: {result[0]})"
                    elif search_container.search_type == "issued_books":
                        display_text = f"{result[1]} - {result[2]} (ID: {result[0]}) - Student: {result[6] or 'Unknown'}"
                    elif search_container.search_type == "students":
                        display_text = f"{result[1]} - {result[2]} (ERP: {result[0]})"
                    
                    search_container.listbox.insert(tk.END, display_text)
                
                # Show dropdown
                search_container.dropdown_frame.pack(fill='x', pady=(2, 0))
            else:
                search_container.dropdown_frame.pack_forget()
                
        except Exception as e:
            print(f"Search error: {e}")
            search_container.dropdown_frame.pack_forget()
    
    def search_books_data(self, search_term):
        """Search books by title, author, or ID"""
        try:
            conn = sqlite3.connect("storebook.db")
            cursor = conn.cursor()
            cursor.execute("""SELECT Book_ID, Title, Author, Edition, Price, Issue, ID 
                            FROM stbook WHERE 
                            Title LIKE ? OR Author LIKE ? OR Book_ID LIKE ?""",
                          (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
            results = cursor.fetchall()
            conn.close()
            return results
        except:
            return []
    
    def search_available_books_data(self, search_term):
        """Search only available books"""
        try:
            conn = sqlite3.connect("storebook.db")
            cursor = conn.cursor()
            cursor.execute("""SELECT Book_ID, Title, Author, Edition, Price, Issue, ID 
                            FROM stbook WHERE 
                            (Issue='' OR Issue IS NULL) AND
                            (Title LIKE ? OR Author LIKE ? OR Book_ID LIKE ?)""",
                          (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
            results = cursor.fetchall()
            conn.close()
            return results
        except:
            return []
    
    def search_issued_books_data(self, search_term):
        """Search only issued books"""
        try:
            conn = sqlite3.connect("storebook.db")
            cursor = conn.cursor()
            cursor.execute("""SELECT Book_ID, Title, Author, Edition, Price, Issue, ID 
                            FROM stbook WHERE 
                            (Issue!='' AND Issue IS NOT NULL) AND
                            (Title LIKE ? OR Author LIKE ? OR Book_ID LIKE ?)""",
                          (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
            results = cursor.fetchall()
            conn.close()
            return results
        except:
            return []
    
    def search_students_data(self, search_term):
        """Search students by name, ERP ID, or roll number"""
        try:
            conn = sqlite3.connect("students.db")
            cursor = conn.cursor()
            cursor.execute("""SELECT ERP_ID, Name, Course, year, Roll_no, "e-mail", Contact_no 
                            FROM student WHERE 
                            Name LIKE ? OR ERP_ID LIKE ? OR Roll_no LIKE ? OR Course LIKE ?""",
                          (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
            results = cursor.fetchall()
            conn.close()
            return results
        except:
            return []
    
    def setup_login_screen(self):
        self.clear_screen()
        self.current_screen = tk.Frame(self.root, bg=self.colors['background'])
        self.current_screen.pack(fill='both', expand=True)
        
        center = tk.Frame(self.current_screen, bg=self.colors['background'])
        center.place(relx=0.5, rely=0.5, anchor='center')
        
        card = tk.Frame(center, bg=self.colors['surface'], padx=50, pady=40)
        card.pack()
        
        # Header
        header = tk.Frame(card, bg=self.colors['surface'])
        header.pack(fill='x', pady=(0, 30))
        
        logo_icon = self.load_icon('library', (64, 64))
        if logo_icon:
            logo_label = tk.Label(header, image=logo_icon, bg=self.colors['surface'])
            logo_label.image = logo_icon
            logo_label.pack()
        
        tk.Label(header, text="Modern Library System", font=self.fonts['h1'],
                bg=self.colors['surface'], fg=self.colors['text']).pack(pady=(10, 5))
        tk.Label(header, text="Sign in with your username", font=self.fonts['body'],
                bg=self.colors['surface'], fg=self.colors['text_secondary']).pack()
        
        # Form
        form = tk.Frame(card, bg=self.colors['surface'])
        form.pack(fill='x', pady=20)
        
        tk.Label(form, text="Username", font=self.fonts['body'],
                bg=self.colors['surface'], fg=self.colors['text']).pack(anchor='w', pady=(0, 5))
        self.username_frame, self.username_entry = self.create_entry(form, "Enter your username")
        self.username_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(form, text="Password", font=self.fonts['body'],
                bg=self.colors['surface'], fg=self.colors['text']).pack(anchor='w', pady=(0, 5))
        self.password_frame, self.password_entry = self.create_entry(form, "Enter your password", show="*")
        self.password_frame.pack(fill='x', pady=(0, 25))
        
        login_btn = self.create_button(form, "Sign In", self.login, 'primary', icon='user')
        login_btn.config(height=3)
        login_btn.pack(fill='x', padx=20)
    
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if username in ["Enter your username", ""] or password in ["Enter your password", ""]:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        try:
            conn = sqlite3.connect("admin.db")
            cursor = conn.cursor()
            # Use the new username column for login
            cursor.execute("SELECT * FROM adm WHERE username=? AND Password=?", (username, password))
            result = cursor.fetchone()
            
            if result:
                self.logged_in_user = result[1]  # Store full name for display
                messagebox.showinfo("Success", f"Welcome, {result[1]}!")
                self.setup_dashboard()
            else:
                messagebox.showerror("Error", "Invalid username or password")
            
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")
    
    def setup_dashboard(self):
        self.clear_screen()
        self.current_screen = tk.Frame(self.root, bg=self.colors['background'])
        self.current_screen.pack(fill='both', expand=True)
        
        # Header
        header = tk.Frame(self.current_screen, bg=self.colors['surface'], height=70)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        header_content = tk.Frame(header, bg=self.colors['surface'])
        header_content.pack(fill='both', expand=True, padx=30, pady=15)
        
        tk.Label(header_content, text="📚 Library Dashboard", font=self.fonts['h1'],
                bg=self.colors['surface'], fg=self.colors['text']).pack(side='left')
        
        user_label = tk.Label(header_content, text=f"Welcome, {self.logged_in_user}", 
                            font=self.fonts['body'], bg=self.colors['surface'], 
                            fg=self.colors['text_secondary'])
        user_label.pack(side='right', padx=(0, 20))
        
        logout_btn = self.create_button(header_content, "Logout", self.logout, 'outline', icon='logout')
        logout_btn.pack(side='right')
        
        # Main content
        main = tk.Frame(self.current_screen, bg=self.colors['background'])
        main.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Stats
        stats = tk.Frame(main, bg=self.colors['background'])
        stats.pack(fill='x', pady=(0, 25))
        
        self.create_stat_card(stats, "Total Books", self.get_books_count(), self.colors['primary']).pack(side='left', padx=(0, 15))
        self.create_stat_card(stats, "Available", self.get_available_count(), self.colors['success']).pack(side='left', padx=(0, 15))
        self.create_stat_card(stats, "Issued", self.get_issued_count(), self.colors['warning']).pack(side='left', padx=(0, 15))
        self.create_stat_card(stats, "Students", self.get_students_count(), self.colors['secondary']).pack(side='left')
        
        # Actions
        actions = tk.Frame(main, bg=self.colors['background'])
        actions.pack(fill='both', expand=True)
        
        buttons = [
            ("Add Book", self.add_book, 'success', 'add_book'),
            ("Issue Book", self.issue_book, 'primary', 'issue_book'),
            ("Return Book", self.return_book, 'info', 'return_book'),
            ("Search Books", self.search_book, 'secondary', 'search_book'),
            ("Edit Book", self.edit_book, 'warning', 'edit_book'),
            ("Show All Books", self.show_books, 'primary', 'show_books'),
            ("Delete Book", self.delete_book, 'danger', 'delete_book'),
            ("Student Records", self.show_students, 'secondary', 'student')
        ]
        
        for i, (text, cmd, style, icon) in enumerate(buttons):
            row, col = i // 4, i % 4
            btn = self.create_button(actions, text, cmd, style, width=32, icon=icon)
            btn.config(height=4)  # Make dashboard buttons even taller and bigger
            btn.grid(row=row, column=col, padx=20, pady=20, sticky='ew')
        
        for i in range(4):
            actions.columnconfigure(i, weight=1)
        
        # Charts section
        charts_frame = tk.Frame(main, bg=self.colors['background'])
        charts_frame.pack(fill='both', expand=True, pady=(20, 0))
        
        self.create_charts(charts_frame)
    
    def create_stat_card(self, parent, title, value, color):
        card = tk.Frame(parent, bg=self.colors['surface'], width=160, height=100)
        card.pack_propagate(False)
        
        content = tk.Frame(card, bg=self.colors['surface'])
        content.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Value label with proper spacing
        value_label = tk.Label(content, text=str(value), font=self.fonts['display'],
                              bg=self.colors['surface'], fg=color)
        value_label.pack(pady=(0, 5))
        
        # Title label with proper font size
        title_label = tk.Label(content, text=title, font=self.fonts['body'],
                              bg=self.colors['surface'], fg=self.colors['text_secondary'])
        title_label.pack()
        
        return card
    
    def create_charts(self, parent):
        """Create charts section with visual statistics"""
        # Charts container
        charts_container = tk.Frame(parent, bg=self.colors['background'])
        charts_container.pack(fill='both', expand=True)
        
        # Left chart - Book Status Pie Chart
        left_chart = tk.Frame(charts_container, bg=self.colors['surface'], width=400, height=250)
        left_chart.pack(side='left', fill='both', expand=True, padx=(0, 10))
        left_chart.pack_propagate(False)
        
        # Chart title
        tk.Label(left_chart, text="📊 Book Status Distribution", 
                font=self.fonts['h3'], bg=self.colors['surface'], 
                fg=self.colors['text']).pack(pady=(15, 10))
        
        # Create pie chart with canvas
        chart_canvas = tk.Canvas(left_chart, bg=self.colors['surface'], 
                               width=300, height=180, highlightthickness=0)
        chart_canvas.pack(pady=10)
        
        # Draw pie chart
        self.draw_pie_chart(chart_canvas)
        
        # Right chart - Monthly Activity Bar Chart
        right_chart = tk.Frame(charts_container, bg=self.colors['surface'], width=400, height=250)
        right_chart.pack(side='right', fill='both', expand=True, padx=(10, 0))
        right_chart.pack_propagate(False)
        
        # Chart title
        tk.Label(right_chart, text="📈 Library Activity Overview", 
                font=self.fonts['h3'], bg=self.colors['surface'], 
                fg=self.colors['text']).pack(pady=(15, 10))
        
        # Create bar chart with canvas
        bar_canvas = tk.Canvas(right_chart, bg=self.colors['surface'], 
                             width=350, height=180, highlightthickness=0)
        bar_canvas.pack(pady=10)
        
        # Draw bar chart
        self.draw_bar_chart(bar_canvas)
    
    def draw_pie_chart(self, canvas):
        """Draw a pie chart showing book status"""
        # Get data
        total_books = self.get_books_count()
        available = self.get_available_count()
        issued = self.get_issued_count()
        
        if total_books == 0:
            # Show "No Data" message
            canvas.create_text(150, 90, text="No Books Available", 
                             font=self.fonts['body'], fill=self.colors['text_secondary'])
            return
        
        # Calculate angles
        center_x, center_y = 150, 90
        radius = 60
        
        # Calculate percentages
        available_angle = (available / total_books) * 360 if total_books > 0 else 0
        issued_angle = (issued / total_books) * 360 if total_books > 0 else 0
        
        # Draw pie slices
        start_angle = 0
        
        # Available books (green)
        if available > 0:
            extent = available_angle
            canvas.create_arc(center_x - radius, center_y - radius, 
                            center_x + radius, center_y + radius,
                            start=start_angle, extent=extent, 
                            fill=self.colors['success'], outline='white', width=2)
            start_angle += extent
        
        # Issued books (orange)
        if issued > 0:
            extent = issued_angle
            canvas.create_arc(center_x - radius, center_y - radius, 
                            center_x + radius, center_y + radius,
                            start=start_angle, extent=extent, 
                            fill=self.colors['warning'], outline='white', width=2)
        
        # Legend
        legend_y = 160
        # Available
        canvas.create_rectangle(50, legend_y, 65, legend_y + 10, 
                              fill=self.colors['success'], outline='')
        canvas.create_text(75, legend_y + 5, text=f"Available ({available})", 
                         font=self.fonts['small'], fill=self.colors['text'], anchor='w')
        
        # Issued
        canvas.create_rectangle(180, legend_y, 195, legend_y + 10, 
                              fill=self.colors['warning'], outline='')
        canvas.create_text(205, legend_y + 5, text=f"Issued ({issued})", 
                         font=self.fonts['small'], fill=self.colors['text'], anchor='w')
    
    def draw_bar_chart(self, canvas):
        """Draw a bar chart showing library metrics"""
        # Get data
        total_books = self.get_books_count()
        available = self.get_available_count()
        issued = self.get_issued_count()
        students = self.get_students_count()
        
        # Chart dimensions
        chart_width = 280
        chart_height = 120
        margin_left = 50
        margin_bottom = 40
        
        # Data
        data = [
            ("Books", total_books, self.colors['primary']),
            ("Available", available, self.colors['success']),
            ("Issued", issued, self.colors['warning']),
            ("Students", students, self.colors['secondary'])
        ]
        
        if max([d[1] for d in data]) == 0:
            canvas.create_text(175, 90, text="No Data Available", 
                             font=self.fonts['body'], fill=self.colors['text_secondary'])
            return
        
        # Calculate bar dimensions
        bar_width = chart_width // len(data) - 10
        max_value = max([d[1] for d in data]) or 1
        
        # Draw bars
        for i, (label, value, color) in enumerate(data):
            x = margin_left + i * (bar_width + 10)
            bar_height = (value / max_value) * chart_height
            y = 160 - bar_height
            
            # Draw bar
            canvas.create_rectangle(x, y, x + bar_width, 160, 
                                  fill=color, outline='')
            
            # Draw value on top
            canvas.create_text(x + bar_width // 2, y - 10, text=str(value), 
                             font=self.fonts['small'], fill=self.colors['text'])
            
            # Draw label
            canvas.create_text(x + bar_width // 2, 175, text=label, 
                             font=self.fonts['small'], fill=self.colors['text'])
    
    def create_header(self, title, back_command):
        header = tk.Frame(self.current_screen, bg=self.colors['surface'], height=70)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        header_content = tk.Frame(header, bg=self.colors['surface'])
        header_content.pack(fill='both', expand=True, padx=30, pady=15)
        
        back_btn = self.create_button(header_content, "← Back", back_command, 'outline', icon='back')
        back_btn.pack(side='left')
        
        tk.Label(header_content, text=title, font=self.fonts['h1'],
                bg=self.colors['surface'], fg=self.colors['text']).pack(side='left', padx=(20, 0))
    
    def get_books_count(self):
        try:
            conn = sqlite3.connect("storebook.db")
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM stbook")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except: return 0
    
    def get_available_count(self):
        try:
            conn = sqlite3.connect("storebook.db")
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM stbook WHERE Issue='' OR Issue IS NULL")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except: return 0
    
    def get_issued_count(self):
        try:
            conn = sqlite3.connect("storebook.db")
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM stbook WHERE Issue!='' AND Issue IS NOT NULL")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except: return 0
    
    def get_students_count(self):
        try:
            conn = sqlite3.connect("students.db")
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM student")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except: return 0
    
    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.setup_login_screen()
    
    def add_book(self):
        self.clear_screen()
        self.current_screen = tk.Frame(self.root, bg=self.colors['background'])
        self.current_screen.pack(fill='both', expand=True)
        
        self.create_header("Add New Book", self.setup_dashboard)
        
        # Form container
        form_container = tk.Frame(self.current_screen, bg=self.colors['background'])
        form_container.pack(fill='both', expand=True, padx=30, pady=20)
        
        form_card = tk.Frame(form_container, bg=self.colors['surface'], padx=40, pady=30)
        form_card.pack(fill='x')
        
        # Form fields
        fields = [("Book ID", "book_id"), ("Title", "title"), ("Author", "author"), 
                 ("Edition", "edition"), ("Price", "price")]
        
        self.book_entries = {}
        
        for i, (label, key) in enumerate(fields):
            row = i // 2
            col = i % 2
            
            field_frame = tk.Frame(form_card, bg=self.colors['surface'])
            field_frame.grid(row=row, column=col, padx=15, pady=10, sticky='ew')
            
            tk.Label(field_frame, text=label, font=self.fonts['body'],
                    bg=self.colors['surface'], fg=self.colors['text']).pack(anchor='w', pady=(0, 5))
            
            entry_frame, entry = self.create_entry(field_frame, f"Enter {label.lower()}")
            entry_frame.pack(fill='x')
            self.book_entries[key] = entry
        
        form_card.columnconfigure(0, weight=1)
        form_card.columnconfigure(1, weight=1)
        
        # Submit button
        submit_frame = tk.Frame(form_card, bg=self.colors['surface'])
        submit_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        submit_btn = self.create_button(submit_frame, "📖 Add New Book", self.save_book, 'success', icon='add_book')
        submit_btn.config(height=3)
        submit_btn.pack(fill='x', padx=20)
    
    def save_book(self):
        values = {}
        placeholders = ["Enter book id", "Enter title", "Enter author", "Enter edition", "Enter price"]
        
        for key, entry in self.book_entries.items():
            value = entry.get().strip()
            if value in placeholders: value = ""
            values[key] = value
        
        if not all(values.values()):
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        try:
            # Validate price is numeric
            int(values['price'])
            
            conn = sqlite3.connect("storebook.db")
            cursor = conn.cursor()
            
            # Check if book ID exists
            cursor.execute("SELECT * FROM stbook WHERE Book_ID=?", (values['book_id'],))
            if cursor.fetchone():
                messagebox.showerror("Error", "Book ID already exists")
                conn.close()
                return
            
            # Insert new book
            cursor.execute("""INSERT INTO stbook (Book_ID, Title, Author, Edition, Price, Issue, ID)
                            VALUES (?, ?, ?, ?, ?, '', '')""",
                          (values['book_id'], values['title'], values['author'], 
                           values['edition'], values['price']))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Book added successfully!")
            self.setup_dashboard()
            
        except ValueError:
            messagebox.showerror("Error", "Price must be a number")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add book: {e}")
    
    def show_books(self):
        self.clear_screen()
        self.current_screen = tk.Frame(self.root, bg=self.colors['background'])
        self.current_screen.pack(fill='both', expand=True)
        
        self.create_header("All Books", self.setup_dashboard)
        
        # Table container
        table_container = tk.Frame(self.current_screen, bg=self.colors['background'])
        table_container.pack(fill='both', expand=True, padx=30, pady=20)
        
        table_frame = tk.Frame(table_container, bg=self.colors['surface'])
        table_frame.pack(fill='both', expand=True)
        
        # Configure treeview style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Treeview', background=self.colors['surface'], 
                       foreground=self.colors['text'], fieldbackground=self.colors['surface'])
        style.configure('Treeview.Heading', background=self.colors['primary'], 
                       foreground='white', font=self.fonts['body'])
        
        columns = ('ID', 'Title', 'Author', 'Edition', 'Price', 'Status')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor='center')
        
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True, padx=20, pady=20)
        scrollbar.pack(side='right', fill='y', pady=20)
        
        # Load books
        try:
            conn = sqlite3.connect("storebook.db")
            cursor = conn.cursor()
            cursor.execute("SELECT Book_ID, Title, Author, Edition, Price, Issue FROM stbook")
            books = cursor.fetchall()
            
            for book in books:
                status = "Available" if not book[5] or book[5] == "" else "Issued"
                book_data = book[:5] + (status,)
                tree.insert('', 'end', values=book_data)
            
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load books: {e}")
    
    def search_book(self):
        self.clear_screen()
        self.current_screen = tk.Frame(self.root, bg=self.colors['background'])
        self.current_screen.pack(fill='both', expand=True)
        
        self.create_header("Search Books", self.setup_dashboard)
        
        # Search container
        search_container = tk.Frame(self.current_screen, bg=self.colors['background'])
        search_container.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Enhanced search form
        search_card = tk.Frame(search_container, bg=self.colors['surface'], padx=30, pady=20)
        search_card.pack(fill='x', pady=(0, 20))
        
        tk.Label(search_card, text="🔍 Enhanced Book Search", font=self.fonts['h3'],
                bg=self.colors['surface'], fg=self.colors['text']).pack(anchor='w', pady=(0, 10))
        
        tk.Label(search_card, text="Search by Title, Author, Book ID, or Edition - Click on results to see details", 
                font=self.fonts['body'], bg=self.colors['surface'], fg=self.colors['text_secondary']).pack(anchor='w', pady=(0, 5))
        
        self.search_dropdown = self.create_search_dropdown(search_card, "Type book title, author, or ID to search...", "books")
        self.search_dropdown.pack(fill='x', pady=10)
        
        # Show selected book button
        show_btn = self.create_button(search_card, "📖 Show Selected Book Details", self.show_selected_book_details, 'secondary', icon='show_books')
        show_btn.config(height=3)
        show_btn.pack(fill='x', padx=20, pady=(10, 0))
        
        # Results area
        self.results_frame = tk.Frame(search_container, bg=self.colors['surface'])
        self.results_frame.pack(fill='both', expand=True)
        
        # Initially show message
        tk.Label(self.results_frame, text="Type in the search box above to find books instantly!\nClick on any result to select it, then click 'Show Selected Book Details'",
                font=self.fonts['body'], bg=self.colors['surface'], 
                fg=self.colors['text_secondary'], justify='center').pack(expand=True)
        
        # Status area
        self.search_status = tk.Label(search_card, text="", font=self.fonts['body'],
                                    bg=self.colors['surface'], fg=self.colors['text_secondary'])
        self.search_status.pack(pady=(10, 0))
    
    def show_selected_book_details(self):
        """Show detailed information about the selected book"""
        # Check if book is selected
        if not hasattr(self.search_dropdown, 'selected_data') or not self.search_dropdown.selected_data:
            self.search_status.config(text="❌ Please search and select a book first", fg=self.colors['danger'])
            return
        
        book_data = self.search_dropdown.selected_data
        
        # Clear results area
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Create detailed book info card
        detail_card = tk.Frame(self.results_frame, bg=self.colors['surface'], padx=30, pady=30)
        detail_card.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Book title
        tk.Label(detail_card, text=f"📖 {book_data[1]}", font=self.fonts['h1'],
                bg=self.colors['surface'], fg=self.colors['text']).pack(anchor='w', pady=(0, 10))
        
        # Book details in a nice layout
        details_frame = tk.Frame(detail_card, bg=self.colors['surface'])
        details_frame.pack(fill='x', pady=(0, 20))
        
        # Left column
        left_col = tk.Frame(details_frame, bg=self.colors['surface'])
        left_col.pack(side='left', fill='both', expand=True, padx=(0, 20))
        
        details = [
            ("👤 Author", book_data[2]),
            ("🆔 Book ID", book_data[0]),
            ("📝 Edition", book_data[3])
        ]
        
        for label, value in details:
            detail_row = tk.Frame(left_col, bg=self.colors['surface'])
            detail_row.pack(fill='x', pady=5)
            
            tk.Label(detail_row, text=label, font=self.fonts['h3'],
                    bg=self.colors['surface'], fg=self.colors['text']).pack(side='left')
            tk.Label(detail_row, text=str(value), font=self.fonts['body'],
                    bg=self.colors['surface'], fg=self.colors['text_secondary']).pack(side='left', padx=(10, 0))
        
        # Right column
        right_col = tk.Frame(details_frame, bg=self.colors['surface'])
        right_col.pack(side='right', fill='both', expand=True)
        
        # Price
        price_frame = tk.Frame(right_col, bg=self.colors['surface'])
        price_frame.pack(fill='x', pady=5)
        tk.Label(price_frame, text="💰 Price", font=self.fonts['h3'],
                bg=self.colors['surface'], fg=self.colors['text']).pack(side='left')
        tk.Label(price_frame, text=f"${book_data[4]}", font=self.fonts['body'],
                bg=self.colors['surface'], fg=self.colors['text_secondary']).pack(side='left', padx=(10, 0))
        
        # Status
        status_frame = tk.Frame(right_col, bg=self.colors['surface'])
        status_frame.pack(fill='x', pady=5)
        tk.Label(status_frame, text="📊 Status", font=self.fonts['h3'],
                bg=self.colors['surface'], fg=self.colors['text']).pack(side='left')
        
        status = "Available" if not book_data[5] or book_data[5] == "" else f"Issued ({book_data[5]})"
        status_color = self.colors['success'] if status == "Available" else self.colors['warning']
        
        tk.Label(status_frame, text=status, font=self.fonts['body'],
                bg=self.colors['surface'], fg=status_color).pack(side='left', padx=(10, 0))
        
        # If book is issued, show student info
        if book_data[5] and book_data[5] != "" and book_data[6]:
            student_frame = tk.Frame(right_col, bg=self.colors['surface'])
            student_frame.pack(fill='x', pady=5)
            tk.Label(student_frame, text="👤 Issued to", font=self.fonts['h3'],
                    bg=self.colors['surface'], fg=self.colors['text']).pack(side='left')
            tk.Label(student_frame, text=f"Student ID: {book_data[6]}", font=self.fonts['body'],
                    bg=self.colors['surface'], fg=self.colors['text_secondary']).pack(side='left', padx=(10, 0))
        
        self.search_status.config(text="✅ Book details displayed successfully!", fg=self.colors['success'])
    
    def perform_search(self):
        search_term = self.search_entry.get().strip()
        if search_term in ["Enter book title, author, or ID", ""]:
            messagebox.showerror("Error", "Please enter a search term")
            return
        
        # Clear results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        try:
            conn = sqlite3.connect("storebook.db")
            cursor = conn.cursor()
            
            # Search in multiple fields
            cursor.execute("""SELECT Book_ID, Title, Author, Edition, Price, Issue 
                            FROM stbook WHERE 
                            Title LIKE ? OR Author LIKE ? OR Book_ID LIKE ?""",
                          (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
            results = cursor.fetchall()
            
            if results:
                # Create results table
                style = ttk.Style()
                style.configure('Treeview', background=self.colors['surface'])
                
                columns = ('ID', 'Title', 'Author', 'Edition', 'Price', 'Status')
                tree = ttk.Treeview(self.results_frame, columns=columns, show='headings', height=15)
                
                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, width=120, anchor='center')
                
                for book in results:
                    status = "Available" if not book[5] or book[5] == "" else "Issued"
                    book_data = book[:5] + (status,)
                    tree.insert('', 'end', values=book_data)
                
                tree.pack(fill='both', expand=True, padx=20, pady=20)
                
                # Results count
                count_label = tk.Label(self.results_frame, text=f"Found {len(results)} book(s)",
                                     font=self.fonts['small'], bg=self.colors['surface'],
                                     fg=self.colors['text_secondary'])
                count_label.pack(pady=(0, 10))
            else:
                tk.Label(self.results_frame, text="No books found matching your search",
                        font=self.fonts['body'], bg=self.colors['surface'],
                        fg=self.colors['text_secondary']).pack(expand=True)
            
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {e}")
    
    def issue_book(self):
        self.clear_screen()
        self.current_screen = tk.Frame(self.root, bg=self.colors['background'])
        self.current_screen.pack(fill='both', expand=True)
        
        self.create_header("Enhanced Issue Book", self.setup_dashboard)
        
        # Form
        form_container = tk.Frame(self.current_screen, bg=self.colors['background'])
        form_container.pack(fill='both', expand=True, padx=30, pady=20)
        
        form_card = tk.Frame(form_container, bg=self.colors['surface'], padx=40, pady=30)
        form_card.pack(fill='x')
        
        # Step 1: Student Selection
        step1_frame = tk.Frame(form_card, bg=self.colors['surface'])
        step1_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(step1_frame, text="🔍 Step 1: Search and Select Student", 
                font=self.fonts['h3'], bg=self.colors['surface'], fg=self.colors['text']).pack(anchor='w', pady=(0, 10))
        
        tk.Label(step1_frame, text="Search by Name, ERP ID, Roll Number, or Course", 
                font=self.fonts['body'], bg=self.colors['surface'], fg=self.colors['text_secondary']).pack(anchor='w', pady=(0, 5))
        
        self.student_search = self.create_search_dropdown(step1_frame, "Type student name, ERP ID, or roll number...", "students")
        self.student_search.pack(fill='x', pady=(0, 15))
        
        # Step 2: Book Selection
        step2_frame = tk.Frame(form_card, bg=self.colors['surface'])
        step2_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(step2_frame, text="📚 Step 2: Search and Select Available Book", 
                font=self.fonts['h3'], bg=self.colors['surface'], fg=self.colors['text']).pack(anchor='w', pady=(0, 10))
        
        tk.Label(step2_frame, text="Search by Title, Author, or Book ID (Only Available Books)", 
                font=self.fonts['body'], bg=self.colors['surface'], fg=self.colors['text_secondary']).pack(anchor='w', pady=(0, 5))
        
        self.book_search = self.create_search_dropdown(step2_frame, "Type book title, author, or ID...", "available_books")
        self.book_search.pack(fill='x', pady=(0, 20))
        
        # Issue button
        issue_btn = self.create_button(form_card, "📖 Issue Selected Book", self.process_enhanced_issue, 'success', icon='issue_book')
        issue_btn.config(height=3)
        issue_btn.pack(fill='x', padx=20)
        
        # Status area
        self.issue_status = tk.Label(form_card, text="", font=self.fonts['body'],
                                   bg=self.colors['surface'], fg=self.colors['text_secondary'])
        self.issue_status.pack(pady=(10, 0))
    
    def process_enhanced_issue(self):
        """Process issue using enhanced dropdown selections"""
        # Check if student is selected
        if not hasattr(self.student_search, 'selected_data') or not self.student_search.selected_data:
            self.issue_status.config(text="❌ Please search and select a student first", fg=self.colors['danger'])
            return
        
        # Check if book is selected
        if not hasattr(self.book_search, 'selected_data') or not self.book_search.selected_data:
            self.issue_status.config(text="❌ Please search and select an available book", fg=self.colors['danger'])
            return
        
        student_data = self.student_search.selected_data
        book_data = self.book_search.selected_data
        
        # Confirm the issue
        student_name = student_data[1]
        book_title = book_data[1]
        confirm_msg = f"Issue '{book_title}' to {student_name}?"
        
        if not messagebox.askyesno("Confirm Issue", confirm_msg):
            return
        
        try:
            # Issue the book
            issue_date = datetime.now().strftime("%Y-%m-%d")
            
            # Update book status
            conn_book = sqlite3.connect("storebook.db")
            cursor_book = conn_book.cursor()
            cursor_book.execute("UPDATE stbook SET Issue=?, ID=? WHERE Book_ID=?", 
                              (issue_date, student_data[0], book_data[0]))
            
            # Update student record
            conn_student = sqlite3.connect("students.db")
            cursor_student = conn_student.cursor()
            cursor_student.execute("SELECT No_book FROM student WHERE ERP_ID=?", (student_data[0],))
            result = cursor_student.fetchone()
            current_books = (result[0] or 0) if result else 0
            
            cursor_student.execute("UPDATE student SET No_book=?, From_date=? WHERE ERP_ID=?",
                                 (current_books + 1, issue_date, student_data[0]))
            
            conn_book.commit()
            conn_student.commit()
            conn_book.close()
            conn_student.close()
            
            self.issue_status.config(text=f"✅ Book issued successfully to {student_name}!", fg=self.colors['success'])
            
            # Clear selections after success
            self.student_search.entry.delete(0, tk.END)
            self.student_search.entry.insert(0, "Type student name, ERP ID, or roll number...")
            self.student_search.entry.config(fg=self.colors['text_secondary'])
            self.student_search.selected_data = None
            
            self.book_search.entry.delete(0, tk.END)
            self.book_search.entry.insert(0, "Type book title, author, or ID...")
            self.book_search.entry.config(fg=self.colors['text_secondary'])
            self.book_search.selected_data = None
            
        except Exception as e:
            self.issue_status.config(text=f"❌ Error: {e}", fg=self.colors['danger'])
    
    def process_issue(self):
        student_id = self.student_entry.get().strip()
        book_id = self.book_issue_entry.get().strip()
        
        if student_id in ["Enter student ERP ID", ""] or book_id in ["Enter book ID", ""]:
            messagebox.showerror("Error", "Please enter both Student ID and Book ID")
            return
        
        try:
            # Check if student exists
            conn_student = sqlite3.connect("students.db")
            cursor_student = conn_student.cursor()
            cursor_student.execute("SELECT * FROM student WHERE ERP_ID=?", (student_id,))
            student = cursor_student.fetchone()
            
            if not student:
                messagebox.showerror("Error", "Student not found")
                conn_student.close()
                return
            
            # Check if book exists and is available
            conn_book = sqlite3.connect("storebook.db")
            cursor_book = conn_book.cursor()
            cursor_book.execute("SELECT * FROM stbook WHERE Book_ID=? AND (Issue='' OR Issue IS NULL)", (book_id,))
            book = cursor_book.fetchone()
            
            if not book:
                messagebox.showerror("Error", "Book not found or already issued")
                conn_book.close()
                conn_student.close()
                return
            
            # Issue the book
            issue_date = datetime.now().strftime("%Y-%m-%d")
            
            # Update book status
            cursor_book.execute("UPDATE stbook SET Issue=?, ID=? WHERE Book_ID=?", 
                              (issue_date, student_id, book_id))
            
            # Update student record
            current_books = student[12] or 0
            cursor_student.execute("UPDATE student SET No_book=?, From_date=? WHERE ERP_ID=?",
                                 (current_books + 1, issue_date, student_id))
            
            conn_book.commit()
            conn_student.commit()
            conn_book.close()
            conn_student.close()
            
            messagebox.showinfo("Success", f"Book '{book[1]}' issued successfully to {student[1]}")
            self.setup_dashboard()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to issue book: {e}")
    
    def return_book(self):
        self.clear_screen()
        self.current_screen = tk.Frame(self.root, bg=self.colors['background'])
        self.current_screen.pack(fill='both', expand=True)
        
        self.create_header("Enhanced Return Book", self.setup_dashboard)
        
        # Form
        form_container = tk.Frame(self.current_screen, bg=self.colors['background'])
        form_container.pack(fill='both', expand=True, padx=30, pady=20)
        
        form_card = tk.Frame(form_container, bg=self.colors['surface'], padx=40, pady=30)
        form_card.pack(fill='x')
        
        # Search issued books
        tk.Label(form_card, text="🔍 Search and Select Issued Book to Return", 
                font=self.fonts['h3'], bg=self.colors['surface'], fg=self.colors['text']).pack(anchor='w', pady=(0, 10))
        
        tk.Label(form_card, text="Search by Book Title, Author, Book ID, or Student Info", 
                font=self.fonts['body'], bg=self.colors['surface'], fg=self.colors['text_secondary']).pack(anchor='w', pady=(0, 5))
        
        self.return_search = self.create_search_dropdown(form_card, "Type book title, author, ID, or student name...", "issued_books")
        self.return_search.pack(fill='x', pady=(0, 20))
        
        # Return button
        return_btn = self.create_button(form_card, "📚 Return Selected Book", self.process_enhanced_return, 'success', icon='return_book')
        return_btn.config(height=3)
        return_btn.pack(fill='x', padx=20)
        
        # Status area
        self.return_status = tk.Label(form_card, text="", font=self.fonts['body'],
                                    bg=self.colors['surface'], fg=self.colors['text_secondary'])
        self.return_status.pack(pady=(10, 0))
    
    def process_enhanced_return(self):
        """Process return using enhanced dropdown selection"""
        # Check if book is selected
        if not hasattr(self.return_search, 'selected_data') or not self.return_search.selected_data:
            self.return_status.config(text="❌ Please search and select an issued book to return", fg=self.colors['danger'])
            return
        
        book_data = self.return_search.selected_data
        book_title = book_data[1]
        student_id = book_data[6]
        
        # Confirm the return
        confirm_msg = f"Return '{book_title}'?"
        if student_id:
            confirm_msg += f"\n(Currently issued to student ID: {student_id})"
        
        if not messagebox.askyesno("Confirm Return", confirm_msg):
            return
        
        try:
            # Update book status
            conn_book = sqlite3.connect("storebook.db")
            cursor_book = conn_book.cursor()
            cursor_book.execute("UPDATE stbook SET Issue='', ID='' WHERE Book_ID=?", (book_data[0],))
            
            # Update student record if we have student ID
            if student_id:
                conn_student = sqlite3.connect("students.db")
                cursor_student = conn_student.cursor()
                cursor_student.execute("SELECT No_book FROM student WHERE ERP_ID=?", (student_id,))
                result = cursor_student.fetchone()
                
                if result:
                    current_books = max(0, (result[0] or 1) - 1)
                    cursor_student.execute("UPDATE student SET No_book=? WHERE ERP_ID=?",
                                         (current_books, student_id))
                    conn_student.commit()
                
                conn_student.close()
            
            conn_book.commit()
            conn_book.close()
            
            self.return_status.config(text=f"✅ Book '{book_title}' returned successfully!", fg=self.colors['success'])
            
            # Clear selection after success
            self.return_search.entry.delete(0, tk.END)
            self.return_search.entry.insert(0, "Type book title, author, ID, or student name...")
            self.return_search.entry.config(fg=self.colors['text_secondary'])
            self.return_search.selected_data = None
            
        except Exception as e:
            self.return_status.config(text=f"❌ Error: {e}", fg=self.colors['danger'])
    
    def process_return(self):
        book_id = self.return_entry.get().strip()
        
        if book_id in ["Enter book ID", ""]:
            messagebox.showerror("Error", "Please enter Book ID")
            return
        
        try:
            # Check if book is issued
            conn_book = sqlite3.connect("storebook.db")
            cursor_book = conn_book.cursor()
            cursor_book.execute("SELECT * FROM stbook WHERE Book_ID=? AND Issue!='' AND Issue IS NOT NULL", (book_id,))
            book = cursor_book.fetchone()
            
            if not book:
                messagebox.showerror("Error", "Book not found or not currently issued")
                conn_book.close()
                return
            
            student_id = book[6]  # ID field contains student ERP_ID
            
            # Update book status
            cursor_book.execute("UPDATE stbook SET Issue='', ID='' WHERE Book_ID=?", (book_id,))
            
            # Update student record
            if student_id:
                conn_student = sqlite3.connect("students.db")
                cursor_student = conn_student.cursor()
                cursor_student.execute("SELECT No_book FROM student WHERE ERP_ID=?", (student_id,))
                result = cursor_student.fetchone()
                
                if result:
                    current_books = max(0, (result[0] or 1) - 1)
                    cursor_student.execute("UPDATE student SET No_book=? WHERE ERP_ID=?",
                                         (current_books, student_id))
                    conn_student.commit()
                
                conn_student.close()
            
            conn_book.commit()
            conn_book.close()
            
            messagebox.showinfo("Success", f"Book '{book[1]}' returned successfully")
            self.setup_dashboard()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to return book: {e}")
    
    def edit_book(self):
        self.clear_screen()
        self.current_screen = tk.Frame(self.root, bg=self.colors['background'])
        self.current_screen.pack(fill='both', expand=True)
        
        self.create_header("Enhanced Edit Book", self.setup_dashboard)
        
        # Search for book to edit
        search_container = tk.Frame(self.current_screen, bg=self.colors['background'])
        search_container.pack(fill='x', padx=30, pady=20)
        
        search_card = tk.Frame(search_container, bg=self.colors['surface'], padx=30, pady=20)
        search_card.pack(fill='x')
        
        tk.Label(search_card, text="🔍 Search and Select Book to Edit", font=self.fonts['h3'],
                bg=self.colors['surface'], fg=self.colors['text']).pack(anchor='w', pady=(0, 10))
        
        tk.Label(search_card, text="Search by Title, Author, Book ID, or Edition", 
                font=self.fonts['body'], bg=self.colors['surface'], fg=self.colors['text_secondary']).pack(anchor='w', pady=(0, 5))
        
        self.edit_search_dropdown = self.create_search_dropdown(search_card, "Type book title, author, or ID to edit...", "books")
        self.edit_search_dropdown.pack(fill='x', pady=10)
        
        load_btn = self.create_button(search_card, "📝 Load Selected Book for Editing", self.load_book_for_edit_enhanced, 'primary', icon='edit_book')
        load_btn.config(height=3)
        load_btn.pack(fill='x', padx=20, pady=(10, 0))
        
        # Edit form (initially hidden)
        self.edit_form_container = tk.Frame(self.current_screen, bg=self.colors['background'])
        self.edit_form_container.pack(fill='both', expand=True, padx=30, pady=(0, 20))
        
        # Status area
        self.edit_status = tk.Label(search_card, text="", font=self.fonts['body'],
                                   bg=self.colors['surface'], fg=self.colors['text_secondary'])
        self.edit_status.pack(pady=(10, 0))
    
    def load_book_for_edit_enhanced(self):
        """Load book for editing using enhanced dropdown selection"""
        # Check if book is selected
        if not hasattr(self.edit_search_dropdown, 'selected_data') or not self.edit_search_dropdown.selected_data:
            self.edit_status.config(text="❌ Please search and select a book to edit", fg=self.colors['danger'])
            return
        
        book_data = self.edit_search_dropdown.selected_data
        
        try:
            # Clear existing form
            for widget in self.edit_form_container.winfo_children():
                widget.destroy()
            
            # Create edit form
            form_card = tk.Frame(self.edit_form_container, bg=self.colors['surface'], padx=40, pady=30)
            form_card.pack(fill='x')
            
            tk.Label(form_card, text=f"📝 Editing: {book_data[1]} by {book_data[2]}", 
                    font=self.fonts['h3'], bg=self.colors['surface'], fg=self.colors['text']).pack(anchor='w', pady=(0, 20))
            
            fields = [("Book ID", "book_id", book_data[0], True), ("Title", "title", book_data[1], False), 
                     ("Author", "author", book_data[2], False), ("Edition", "edition", book_data[3], False), 
                     ("Price", "price", book_data[4], False)]
            
            self.edit_entries = {}
            
            for i, (label, key, value, readonly) in enumerate(fields):
                row = i // 2
                col = i % 2
                
                field_frame = tk.Frame(form_card, bg=self.colors['surface'])
                field_frame.grid(row=row, column=col, padx=15, pady=10, sticky='ew')
                
                tk.Label(field_frame, text=label, font=self.fonts['body'],
                        bg=self.colors['surface'], fg=self.colors['text']).pack(anchor='w', pady=(0, 5))
                
                entry_frame, entry = self.create_entry(field_frame, "")
                entry.delete(0, tk.END)
                entry.insert(0, str(value))
                
                if readonly:
                    entry.config(state='readonly', bg=self.colors['light'])
                
                entry_frame.pack(fill='x')
                self.edit_entries[key] = entry
            
            form_card.columnconfigure(0, weight=1)
            form_card.columnconfigure(1, weight=1)
            
            # Update button
            update_frame = tk.Frame(form_card, bg=self.colors['surface'])
            update_frame.grid(row=3, column=0, columnspan=2, pady=20)
            
            update_btn = self.create_button(update_frame, "💾 Update Book", self.update_book, 'success', icon='edit_book')
            update_btn.config(height=3)
            update_btn.pack(fill='x', padx=20)
            
            self.edit_status.config(text=f"✅ Book loaded successfully! Edit the fields above.", fg=self.colors['success'])
            
        except Exception as e:
            self.edit_status.config(text=f"❌ Error loading book: {e}", fg=self.colors['danger'])
    
    def load_book_for_edit(self):
        book_id = self.edit_search_entry.get().strip()
        
        if book_id in ["Enter book ID", ""]:
            messagebox.showerror("Error", "Please enter Book ID")
            return
        
        try:
            conn = sqlite3.connect("storebook.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM stbook WHERE Book_ID=?", (book_id,))
            book = cursor.fetchone()
            
            if not book:
                messagebox.showerror("Error", "Book not found")
                conn.close()
                return
            
            # Clear existing form
            for widget in self.edit_form_container.winfo_children():
                widget.destroy()
            
            # Create edit form
            form_card = tk.Frame(self.edit_form_container, bg=self.colors['surface'], padx=40, pady=30)
            form_card.pack(fill='x')
            
            fields = [("Book ID", "book_id", book[0], True), ("Title", "title", book[1], False), 
                     ("Author", "author", book[2], False), ("Edition", "edition", book[3], False), 
                     ("Price", "price", book[4], False)]
            
            self.edit_entries = {}
            
            for i, (label, key, value, readonly) in enumerate(fields):
                row = i // 2
                col = i % 2
                
                field_frame = tk.Frame(form_card, bg=self.colors['surface'])
                field_frame.grid(row=row, column=col, padx=15, pady=10, sticky='ew')
                
                tk.Label(field_frame, text=label, font=self.fonts['body'],
                        bg=self.colors['surface'], fg=self.colors['text']).pack(anchor='w', pady=(0, 5))
                
                entry_frame, entry = self.create_entry(field_frame, "")
                entry.delete(0, tk.END)
                entry.insert(0, str(value))
                
                if readonly:
                    entry.config(state='readonly')
                
                entry_frame.pack(fill='x')
                self.edit_entries[key] = entry
            
            form_card.columnconfigure(0, weight=1)
            form_card.columnconfigure(1, weight=1)
            
            # Update button
            update_frame = tk.Frame(form_card, bg=self.colors['surface'])
            update_frame.grid(row=3, column=0, columnspan=2, pady=20)
            
            update_btn = self.create_button(update_frame, "Update Book", self.update_book, 'success', width=20, icon='edit_book')
            update_btn.pack()
            
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load book: {e}")
    
    def update_book(self):
        values = {}
        for key, entry in self.edit_entries.items():
            values[key] = entry.get().strip()
        
        if not all(values.values()):
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        try:
            int(values['price'])  # Validate price
            
            conn = sqlite3.connect("storebook.db")
            cursor = conn.cursor()
            
            cursor.execute("""UPDATE stbook SET Title=?, Author=?, Edition=?, Price=? 
                            WHERE Book_ID=?""",
                          (values['title'], values['author'], values['edition'], 
                           values['price'], values['book_id']))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Book updated successfully!")
            self.setup_dashboard()
            
        except ValueError:
            messagebox.showerror("Error", "Price must be a number")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update book: {e}")
    
    def delete_book(self):
        self.clear_screen()
        self.current_screen = tk.Frame(self.root, bg=self.colors['background'])
        self.current_screen.pack(fill='both', expand=True)
        
        self.create_header("Enhanced Delete Book", self.setup_dashboard)
        
        form_container = tk.Frame(self.current_screen, bg=self.colors['background'])
        form_container.pack(fill='both', expand=True, padx=30, pady=20)
        
        form_card = tk.Frame(form_container, bg=self.colors['surface'], padx=40, pady=30)
        form_card.pack(fill='x')
        
        # Warning message
        warning_frame = tk.Frame(form_card, bg='#fef2f2', relief='solid', bd=1)
        warning_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(warning_frame, text="⚠️ WARNING: This action cannot be undone!", 
                font=self.fonts['h3'], bg='#fef2f2', fg=self.colors['danger']).pack(pady=10)
        
        tk.Label(form_card, text="🔍 Search and Select Book to Delete", font=self.fonts['h3'],
                bg=self.colors['surface'], fg=self.colors['text']).pack(anchor='w', pady=(0, 10))
        
        tk.Label(form_card, text="Search by Title, Author, Book ID, or Edition", 
                font=self.fonts['body'], bg=self.colors['surface'], fg=self.colors['text_secondary']).pack(anchor='w', pady=(0, 5))
        
        self.delete_search_dropdown = self.create_search_dropdown(form_card, "Type book title, author, or ID to delete...", "books")
        self.delete_search_dropdown.pack(fill='x', pady=(0, 20))
        
        delete_btn = self.create_button(form_card, "🗑️ Delete Selected Book", self.process_delete_enhanced, 'danger', icon='delete_book')
        delete_btn.config(height=3)
        delete_btn.pack(fill='x', padx=20)
        
        # Status area
        self.delete_status = tk.Label(form_card, text="", font=self.fonts['body'],
                                    bg=self.colors['surface'], fg=self.colors['text_secondary'])
        self.delete_status.pack(pady=(10, 0))
    
    def process_delete_enhanced(self):
        """Process delete using enhanced dropdown selection"""
        # Check if book is selected
        if not hasattr(self.delete_search_dropdown, 'selected_data') or not self.delete_search_dropdown.selected_data:
            self.delete_status.config(text="❌ Please search and select a book to delete", fg=self.colors['danger'])
            return
        
        book_data = self.delete_search_dropdown.selected_data
        book_title = book_data[1]
        book_author = book_data[2]
        book_id = book_data[0]
        
        # Enhanced confirmation with book details
        confirm_msg = f"Are you sure you want to DELETE this book?\n\n"
        confirm_msg += f"📖 Title: {book_title}\n"
        confirm_msg += f"👤 Author: {book_author}\n"
        confirm_msg += f"🆔 ID: {book_id}\n\n"
        confirm_msg += "⚠️ This action CANNOT be undone!"
        
        if not messagebox.askyesno("⚠️ Confirm Deletion", confirm_msg):
            return
        
        try:
            conn = sqlite3.connect("storebook.db")
            cursor = conn.cursor()
            
            # Check if book is currently issued
            if book_data[5] and book_data[5] != "":
                self.delete_status.config(text="❌ Cannot delete: Book is currently issued to a student", fg=self.colors['danger'])
                conn.close()
                return
            
            # Delete book
            cursor.execute("DELETE FROM stbook WHERE Book_ID=?", (book_id,))
            conn.commit()
            conn.close()
            
            self.delete_status.config(text=f"✅ Book '{book_title}' deleted successfully!", fg=self.colors['success'])
            
            # Clear selection after success
            self.delete_search_dropdown.entry.delete(0, tk.END)
            self.delete_search_dropdown.entry.insert(0, "Type book title, author, or ID to delete...")
            self.delete_search_dropdown.entry.config(fg=self.colors['text_secondary'])
            self.delete_search_dropdown.selected_data = None
            
        except Exception as e:
            self.delete_status.config(text=f"❌ Error deleting book: {e}", fg=self.colors['danger'])
    
    def process_delete(self):
        book_id = self.delete_entry.get().strip()
        
        if book_id in ["Enter book ID", ""]:
            messagebox.showerror("Error", "Please enter Book ID")
            return
        
        if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this book? This cannot be undone."):
            return
        
        try:
            conn = sqlite3.connect("storebook.db")
            cursor = conn.cursor()
            
            # Check if book exists
            cursor.execute("SELECT Title FROM stbook WHERE Book_ID=?", (book_id,))
            book = cursor.fetchone()
            
            if not book:
                messagebox.showerror("Error", "Book not found")
                conn.close()
                return
            
            # Delete book
            cursor.execute("DELETE FROM stbook WHERE Book_ID=?", (book_id,))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", f"Book '{book[0]}' deleted successfully")
            self.setup_dashboard()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete book: {e}")
    
    def show_students(self):
        self.clear_screen()
        self.current_screen = tk.Frame(self.root, bg=self.colors['background'])
        self.current_screen.pack(fill='both', expand=True)
        
        self.create_header("Student Records", self.setup_dashboard)
        
        table_container = tk.Frame(self.current_screen, bg=self.colors['background'])
        table_container.pack(fill='both', expand=True, padx=30, pady=20)
        
        table_frame = tk.Frame(table_container, bg=self.colors['surface'])
        table_frame.pack(fill='both', expand=True)
        
        style = ttk.Style()
        style.configure('Treeview', background=self.colors['surface'])
        
        columns = ('ERP_ID', 'Name', 'Course', 'Year', 'Roll_No', 'Email', 'Books_Issued')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor='center')
        
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True, padx=20, pady=20)
        scrollbar.pack(side='right', fill='y', pady=20)
        
        try:
            conn = sqlite3.connect("students.db")
            cursor = conn.cursor()
            cursor.execute("SELECT ERP_ID, Name, Course, year, Roll_no, \"e-mail\", No_book FROM student")
            students = cursor.fetchall()
            
            for student in students:
                tree.insert('', 'end', values=student)
            
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load students: {e}")

if __name__ == "__main__":
    app = FullFunctionalModernLibrary()

