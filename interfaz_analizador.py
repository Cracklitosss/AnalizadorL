import tkinter as tk
from tkinter import ttk, scrolledtext
from AL import analizador_lexico
import customtkinter as ctk

class InterfazAnalizador:
    def __init__(self, root):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = root
        self.root.title("Analizador Léxico")
        self.root.geometry("1000x800")
        self.root.configure(bg="#1a1a1a")
        
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.titulo = ctk.CTkLabel(
            self.main_frame,
            text="Analizador Léxico",
            font=("Helvetica", 24, "bold"),
            text_color="#4a9eff"
        )
        self.titulo.pack(pady=20)
        
        self.input_frame = ctk.CTkFrame(self.main_frame)
        self.input_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.lbl_entrada = ctk.CTkLabel(
            self.input_frame,
            text="Ingrese el código fuente:",
            font=("Helvetica", 14)
        )
        self.lbl_entrada.pack(anchor="w", padx=10, pady=5)
        
        self.txt_entrada = ctk.CTkTextbox(
            self.input_frame,
            width=900,
            height=200,
            font=("Consolas", 12),
            border_width=2,
            border_color="#2c2c2c",
            fg_color="#2b2b2b"
        )
        self.txt_entrada.pack(padx=10, pady=10)
        
        self.btn_analizar = ctk.CTkButton(
            self.main_frame,
            text="Analizar Código",
            font=("Helvetica", 14, "bold"),
            command=self.analizar_codigo,
            height=40,
            corner_radius=10
        )
        self.btn_analizar.pack(pady=20)
        
        self.results_frame = ctk.CTkFrame(self.main_frame)
        self.results_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.lbl_resultados = ctk.CTkLabel(
            self.results_frame,
            text="Resultados del análisis:",
            font=("Helvetica", 14)
        )
        self.lbl_resultados.pack(anchor="w", padx=10, pady=5)
        
        style = ttk.Style()
        
        style.configure("Custom.Treeview",
            background="#2b2b2b",
            foreground="white",
            fieldbackground="#2b2b2b",
            borderwidth=0,
            rowheight=30
        )
        
        style.layout("Custom.Treeview", [
            ('Custom.Treeview.treearea', {'sticky': 'nswe'})
        ])
        
        style.configure("Custom.Treeview.Heading",
            background="#4a9eff",  
            foreground="black",    
            relief="flat",
            font=("Helvetica", 12, "bold"),
            borderwidth=0
        )
        
        style.map("Custom.Treeview.Heading",
            background=[
                ('active', '#74b4ff'),      
                ('!active', '#4a9eff')    
            ],
            foreground=[
                ('active', 'black'),
                ('!active', 'black')
            ]
        )
        
        style.map("Custom.Treeview",
            background=[
                ('selected', '#1a73e8'),
                ('!selected', '#2b2b2b')
            ],
            foreground=[
                ('selected', 'white'),
                ('!selected', 'white')
            ]
        )
        
        self.tree_frame = ctk.CTkFrame(
            self.results_frame,
            fg_color="#1a1a1a",
            corner_radius=10
        )
        self.tree_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=('Tipo', 'Lexema'),
            show='headings',
            style="Custom.Treeview",
            height=15
        )

        for col in ('Tipo', 'Lexema'):
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, anchor="center", width=200, minwidth=200)
        
        self.scrollbar = ttk.Scrollbar(
            self.tree_frame,
            orient="vertical",
            command=self.tree.yview
        )
        self.scrollbar.pack(side="right", fill="y")
        
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)

    def analizar_codigo(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        codigo = self.txt_entrada.get("1.0", tk.END)
        try:
            tokens = analizador_lexico(codigo)
            for i, (tipo, lexema) in enumerate(tokens):
                tag = 'par' if i % 2 == 0 else 'impar'
                self.tree.insert('', tk.END, values=(tipo, lexema), tags=(tag,))
            
            self.tree.tag_configure('par', background='#2b2b2b', foreground='white')
            self.tree.tag_configure('impar', background='#232323', foreground='white')
            self.tree.tag_configure('error', background='#662222', foreground='white')
        except ValueError as e:
            self.tree.insert('', tk.END, values=('ERROR', str(e)), tags=('error',))

if __name__ == "__main__":
    root = ctk.CTk()
    app = InterfazAnalizador(root)
    root.mainloop() 