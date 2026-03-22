import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import os
from modifier import EmailModifier

# Configuración de tema y apariencia
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Colores personalizados
COLORS = {
    "success": "#2ecc71",
    "error": "#e74c3c",
    "warning": "#f39c12",
    "info": "#3498db",
    "bg_light": "#2b2b2b",
    "bg_dark": "#1e1e1e"
}

class ToolTip:
    """Tooltips simples para widgets"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        widget.bind('<Enter>', self.enter)
        widget.bind('<Leave>', self.leave)

    def enter(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("Segoe UI", 10))
        label.pack()

    def leave(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

class EmailHeaderEditorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Professional Email Header Modifier - Ethical Hacking")
        self.iconbitmap('app_icon.ico')
        self.geometry("1300x900")
        self.minsize(1000, 700)
        
        self.modificador = EmailModifier()
        self.current_file = tk.StringVar(value="No file loaded")
        
        # Configurar pesos del grid principal
        self.grid_columnconfigure(0, weight=1)
        # Filas: 0 banner, 1 toolbar, 2 headers, 3 notebook, 4 status
        self.grid_rowconfigure(2, weight=1)   # headers expandible
        self.grid_rowconfigure(3, weight=2)   # notebook más expandible

        self.crear_widgets()

    def crear_widgets(self):
        # ---------- Banner superior ----------
        banner_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#2c3e50", height=70)
        banner_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        banner_frame.grid_propagate(False)  # Evita que se encoja
        banner_frame.grid_columnconfigure(0, weight=1)
        
        banner_label = ctk.CTkLabel(
            banner_frame,
            text="🛡️ EMAIL HEADER MODIFIER",
            font=("Segoe UI", 22, "bold"),
            text_color="white"
        )
        banner_label.grid(row=0, column=0, pady=(10, 0))
        
        subtitle = ctk.CTkLabel(
            banner_frame,
            text="Professional tool for ethical hacking and forensic analysis",
            font=("Segoe UI", 12),
            text_color="#bdc3c7"
        )
        subtitle.grid(row=1, column=0, pady=(0, 10))

        # ---------- Barra de herramientas ----------
        toolbar_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent", height=40)
        toolbar_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        toolbar_frame.grid_propagate(False)
        toolbar_frame.grid_columnconfigure(0, weight=1)  # Label archivo expande
        toolbar_frame.grid_columnconfigure(1, weight=0)  # Botones fijos

        # Indicador de archivo
        self.file_label = ctk.CTkLabel(
            toolbar_frame,
            textvariable=self.current_file,
            font=("Segoe UI", 11, "bold"),
            text_color=COLORS["success"]
        )
        self.file_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Botones de acción
        btn_frame = ctk.CTkFrame(toolbar_frame, fg_color="transparent")
        btn_frame.grid(row=0, column=1, padx=10, pady=5, sticky="e")

        buttons = [
            ("📂 Load .eml", self.cargar_archivo, "Load an email file (.eml)"),
            ("💾 Save as...", self.guardar_archivo, "Save current headers to a new .eml file"),
            ("🔄 Refresh", self.ver_cabeceras, "Refresh headers view"),
            ("🔍 Validate", self.validar_cabeceras, "Run forensic analysis on current headers")
        ]

        for text, cmd, tooltip in buttons:
            btn = ctk.CTkButton(btn_frame, text=text, command=cmd, width=110, corner_radius=8)
            btn.pack(side="left", padx=3)
            ToolTip(btn, tooltip)

        # ---------- Área de cabeceras ----------
        headers_frame = ctk.CTkFrame(self, corner_radius=10)
        headers_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
        headers_frame.grid_columnconfigure(0, weight=1)
        headers_frame.grid_rowconfigure(1, weight=1)

        headers_label = ctk.CTkLabel(
            headers_frame,
            text="📋 Current Headers",
            font=("Segoe UI", 14, "bold")
        )
        headers_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.text_area = ctk.CTkTextbox(
            headers_frame,
            font=("Consolas", 11),
            corner_radius=8,
            wrap="word"
        )
        self.text_area.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

        # ---------- Notebook (pestañas) ----------
        self.notebook = ctk.CTkTabview(self, corner_radius=10)
        self.notebook.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)

        # Crear pestañas
        self.crear_pestana_perfiles()
        self.crear_pestana_envio()
        self.crear_pestana_forense()
        self.crear_pestana_received_editor()
        self.crear_pestana_campanas()
        self.crear_pestana_ejemplos()

        # ---------- Barra de estado ----------
        self.status_bar = ctk.CTkLabel(
            self,
            text="Ready",
            anchor="w",
            font=("Segoe UI", 10),
            corner_radius=0,
            fg_color="#34495e",
            text_color="white"
        )
        self.status_bar.grid(row=4, column=0, sticky="ew", padx=0, pady=0)

    # ------------------------------------------------------------
    # Métodos auxiliares
    # ------------------------------------------------------------
    def set_status(self, mensaje, color="white"):
        self.status_bar.configure(text=mensaje, text_color=color)
        self.update()

    def cargar_archivo(self):
        filepath = filedialog.askopenfilename(filetypes=[("EML files", "*.eml"), ("All files", "*.*")])
        if filepath:
            try:
                ok, msg = self.modificador.cargar_correo(filepath)
                if ok:
                    self.current_file.set(f"File: {filepath}")
                    self.set_status(msg, COLORS["success"])
                    self.ver_cabeceras()
                    num_headers = len(self.modificador.obtener_todas_cabeceras())
                    messagebox.showinfo("Success", f"Email loaded successfully.\n{num_headers} headers found.")
                else:
                    self.set_status(msg, COLORS["error"])
                    messagebox.showerror("Error", msg)
            except Exception as e:
                messagebox.showerror("Exception", f"An error occurred:\n{str(e)}")

    def guardar_archivo(self):
        if not self.modificador.msg:
            messagebox.showwarning("No data", "No email loaded.")
            return
        filepath = filedialog.asksaveasfilename(defaultextension=".eml",
                                                filetypes=[("EML files", "*.eml"), ("All files", "*.*")])
        if filepath:
            ok, msg = self.modificador.guardar_como(filepath)
            if ok:
                self.set_status(msg, COLORS["success"])
                messagebox.showinfo("Saved", msg)
            else:
                self.set_status(msg, COLORS["error"])
                messagebox.showerror("Error", msg)

    def ver_cabeceras(self):
        if not self.modificador.msg:
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", "No email loaded.")
            return
        cabeceras = self.modificador.obtener_todas_cabeceras()
        self.text_area.delete("1.0", "end")
        for nombre, valor in cabeceras:
            self.text_area.insert("end", f"{nombre}: {valor}\n")
        self.actualizar_lista_received()
        self.set_status("Headers updated", COLORS["info"])

    def validar_cabeceras(self):
        if not self.modificador.msg:
            messagebox.showwarning("No data", "No email loaded.")
            return
        resultados = self.modificador.analizar_forense()
        if resultados:
            msg = "\n".join([f"{r['status']}: {r['check']} - {r['message']}" for r in resultados])
            messagebox.showinfo("Forensic Analysis", msg)
        else:
            messagebox.showinfo("Forensic Analysis", "No results (maybe no headers?)")

    # ------------------------------------------------------------
    # Pestaña: Perfiles
    # ------------------------------------------------------------
    def crear_pestana_perfiles(self):
        self.notebook.add("📧 Profiles")
        frame = self.notebook.tab("📧 Profiles")
        # Usar grid centrado con columnas ponderadas
        frame.grid_columnconfigure(0, weight=0)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=0)

        perfiles = self.modificador.generator.get_profile_names()
        valores_perfil = [p[1] for p in perfiles]

        ctk.CTkLabel(frame, text="Select profile:", font=("Segoe UI", 12)).grid(row=0, column=0, padx=15, pady=8, sticky="e")
        self.perfil_combo = ctk.CTkComboBox(frame, values=valores_perfil, width=300)
        self.perfil_combo.grid(row=0, column=1, padx=15, pady=8, sticky="w")
        if valores_perfil:
            self.perfil_combo.set(valores_perfil[0])
        ToolTip(self.perfil_combo, "Choose the email client/profile to simulate")

        ctk.CTkLabel(frame, text="Sender name:", font=("Segoe UI", 12)).grid(row=1, column=0, padx=15, pady=8, sticky="e")
        self.perfil_from_name = ctk.CTkEntry(frame, width=300, placeholder_text="e.g. John Doe")
        self.perfil_from_name.grid(row=1, column=1, padx=15, pady=8, sticky="w")
        ToolTip(self.perfil_from_name, "The display name of the sender")

        ctk.CTkLabel(frame, text="Sender email:", font=("Segoe UI", 12)).grid(row=2, column=0, padx=15, pady=8, sticky="e")
        self.perfil_from_email = ctk.CTkEntry(frame, width=300, placeholder_text="sender@example.com")
        self.perfil_from_email.grid(row=2, column=1, padx=15, pady=8, sticky="w")
        ToolTip(self.perfil_from_email, "Email address of the sender")

        ctk.CTkLabel(frame, text="Recipient email:", font=("Segoe UI", 12)).grid(row=3, column=0, padx=15, pady=8, sticky="e")
        self.perfil_to_email = ctk.CTkEntry(frame, width=300, placeholder_text="recipient@example.com")
        self.perfil_to_email.grid(row=3, column=1, padx=15, pady=8, sticky="w")
        ToolTip(self.perfil_to_email, "Destination email address")

        ctk.CTkLabel(frame, text="Subject:", font=("Segoe UI", 12)).grid(row=4, column=0, padx=15, pady=8, sticky="e")
        self.perfil_subject = ctk.CTkEntry(frame, width=400, placeholder_text="Email subject")
        self.perfil_subject.grid(row=4, column=1, padx=15, pady=8, sticky="w")
        ToolTip(self.perfil_subject, "Subject line of the email")

        ctk.CTkLabel(frame, text="Error mode:", font=("Segoe UI", 12)).grid(row=5, column=0, padx=15, pady=8, sticky="e")
        self.error_combo = ctk.CTkComboBox(frame, values=['none', 'spf_fail', 'dkim_fail', 'dmarc_fail', 'mixed'], width=150)
        self.error_combo.grid(row=5, column=1, padx=15, pady=8, sticky="w")
        self.error_combo.set('none')
        ToolTip(self.error_combo, "Simulate authentication failures")

        self.btn_generar = ctk.CTkButton(frame, text="Generate with profile", command=self.aplicar_perfil,
                                          corner_radius=8, height=35, font=("Segoe UI", 12))
        self.btn_generar.grid(row=6, column=0, columnspan=2, pady=20)

    def aplicar_perfil(self):
        name = self.perfil_from_name.get().strip()
        from_email = self.perfil_from_email.get().strip()
        to_email = self.perfil_to_email.get().strip()
        subject = self.perfil_subject.get().strip()
        if not (name and from_email and to_email and subject):
            messagebox.showwarning("Empty fields", "Please fill all fields.")
            return
        perfiles = self.modificador.generator.get_profile_names()
        seleccion = self.perfil_combo.get()
        perfil_key = None
        for key, nombre in perfiles:
            if nombre == seleccion:
                perfil_key = key
                break
        if not perfil_key:
            messagebox.showerror("Error", "Profile not found.")
            return
        error_mode = self.error_combo.get()
        msg = self.modificador.generar_con_perfil(perfil_key, name, from_email, to_email, subject, error_mode)
        self.set_status(msg, COLORS["success"])
        self.ver_cabeceras()
        messagebox.showinfo("Profile applied", msg)

    # ------------------------------------------------------------
    # Pestaña: SMTP Send
    # ------------------------------------------------------------
    def crear_pestana_envio(self):
        self.notebook.add("📬 SMTP Send")
        frame = self.notebook.tab("📬 SMTP Send")
        frame.grid_columnconfigure(0, weight=0)
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(frame, text="SMTP Server:", font=("Segoe UI", 12)).grid(row=0, column=0, padx=15, pady=8, sticky="e")
        self.smtp_server = ctk.CTkEntry(frame, width=250, placeholder_text="smtp.gmail.com")
        self.smtp_server.grid(row=0, column=1, padx=15, pady=8, sticky="w")
        ToolTip(self.smtp_server, "SMTP server address")

        ctk.CTkLabel(frame, text="Port:", font=("Segoe UI", 12)).grid(row=1, column=0, padx=15, pady=8, sticky="e")
        self.smtp_port = ctk.CTkEntry(frame, width=100, placeholder_text="587")
        self.smtp_port.insert(0, "587")
        self.smtp_port.grid(row=1, column=1, padx=15, pady=8, sticky="w")
        ToolTip(self.smtp_port, "SMTP port (587 for TLS)")

        ctk.CTkLabel(frame, text="Username:", font=("Segoe UI", 12)).grid(row=2, column=0, padx=15, pady=8, sticky="e")
        self.smtp_user = ctk.CTkEntry(frame, width=250, placeholder_text="user@example.com")
        self.smtp_user.grid(row=2, column=1, padx=15, pady=8, sticky="w")
        ToolTip(self.smtp_user, "SMTP username (usually your email)")

        ctk.CTkLabel(frame, text="Password:", font=("Segoe UI", 12)).grid(row=3, column=0, padx=15, pady=8, sticky="e")
        self.smtp_pass = ctk.CTkEntry(frame, width=250, show="*", placeholder_text="••••••••")
        self.smtp_pass.grid(row=3, column=1, padx=15, pady=8, sticky="w")
        ToolTip(self.smtp_pass, "SMTP password")

        self.smtp_tls = ctk.BooleanVar(value=True)
        self.chk_tls = ctk.CTkCheckBox(frame, text="Use TLS", variable=self.smtp_tls)
        self.chk_tls.grid(row=4, column=1, padx=15, pady=8, sticky="w")
        ToolTip(self.chk_tls, "Enable STARTTLS for secure connection")

        ctk.CTkLabel(frame, text="Delay (sec):", font=("Segoe UI", 12)).grid(row=5, column=0, padx=15, pady=8, sticky="e")
        self.smtp_delay = ctk.CTkEntry(frame, width=100, placeholder_text="0")
        self.smtp_delay.insert(0, "0")
        self.smtp_delay.grid(row=5, column=1, padx=15, pady=8, sticky="w")
        ToolTip(self.smtp_delay, "Delay before sending (to simulate scheduling)")

        ctk.CTkLabel(frame, text="Relays (optional):", font=("Segoe UI", 12)).grid(row=6, column=0, padx=15, pady=8, sticky="ne")
        self.smtp_relays = ctk.CTkTextbox(frame, height=80, width=400, font=("Consolas", 10))
        self.smtp_relays.grid(row=6, column=1, padx=15, pady=8, sticky="w")
        ToolTip(self.smtp_relays, "One per line: server:port:user:pass")

        self.btn_send = ctk.CTkButton(frame, text="Send Email", command=self.enviar_correo,
                                      corner_radius=8, height=35, font=("Segoe UI", 12))
        self.btn_send.grid(row=7, column=0, columnspan=2, pady=20)

    def enviar_correo(self):
        if not self.modificador.msg:
            messagebox.showwarning("No data", "No email loaded.")
            return
        server = self.smtp_server.get().strip()
        if not server:
            messagebox.showwarning("Missing server", "SMTP server is required.")
            return
        try:
            port = int(self.smtp_port.get().strip())
        except:
            port = 587
        user = self.smtp_user.get().strip()
        pwd = self.smtp_pass.get().strip()
        use_tls = self.smtp_tls.get()
        try:
            delay = int(self.smtp_delay.get().strip())
        except:
            delay = 0

        relays = []
        relay_text = self.smtp_relays.get("1.0", "end").strip()
        if relay_text:
            for line in relay_text.split('\n'):
                parts = line.strip().split(':')
                if len(parts) >= 2:
                    relays.append((parts[0], int(parts[1]), parts[2] if len(parts)>2 else '', parts[3] if len(parts)>3 else ''))

        ok, msg = self.modificador.enviar_smtp(server, port, user, pwd, use_tls, relays if relays else None, delay)
        self.set_status(msg, COLORS["success"] if ok else COLORS["error"])
        if ok:
            messagebox.showinfo("Send", "Email sent successfully (background).")
        else:
            messagebox.showerror("Send error", msg)

    # ------------------------------------------------------------
    # Pestaña: Forense
    # ------------------------------------------------------------
    def crear_pestana_forense(self):
        self.notebook.add("🕵️ Forensic")
        frame = self.notebook.tab("🕵️ Forensic")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        self.btn_analyze = ctk.CTkButton(frame, text="🔍 Analyze current headers", command=self.analizar_forense,
                                         corner_radius=8, height=35, font=("Segoe UI", 12))
        self.btn_analyze.grid(row=0, column=0, pady=10)

        self.forense_text = ctk.CTkTextbox(frame, font=("Consolas", 11), corner_radius=8)
        self.forense_text.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

    def analizar_forense(self):
        if not self.modificador.msg:
            messagebox.showwarning("No data", "No email loaded.")
            return
        results = self.modificador.analizar_forense()
        self.forense_text.delete("1.0", "end")
        for r in results:
            if r['status'] == 'PASS':
                icon = "✅"
            elif r['status'] == 'FAIL':
                icon = "❌"
            elif r['status'] == 'WARN':
                icon = "⚠️"
            else:
                icon = "ℹ️"
            line = f"{icon} {r['check']}: {r['message']}\n"
            self.forense_text.insert("end", line)

    # ------------------------------------------------------------
    # Pestaña: Received Editor
    # ------------------------------------------------------------
    def crear_pestana_received_editor(self):
        self.notebook.add("🧩 Received")
        frame = self.notebook.tab("🧩 Received")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        # Usamos tk.Listbox porque CTk no tiene Listbox nativo
        self.received_listbox = tk.Listbox(frame, height=8, font=("Consolas", 10), bg=COLORS["bg_light"], fg="white", selectbackground=COLORS["info"])
        self.received_listbox.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)

        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.grid(row=1, column=0, pady=5)

        buttons = [
            ("➕ Add new", self.add_received_dialog, "Add a custom Received header"),
            ("❌ Delete selected", self.remove_received, "Delete selected Received header"),
            ("⬆️ Move up", self.move_received_up, "Move header up (more recent)"),
            ("⬇️ Move down", self.move_received_down, "Move header down (older)")
        ]

        for text, cmd, tooltip in buttons:
            btn = ctk.CTkButton(btn_frame, text=text, command=cmd, width=110)
            btn.pack(side="left", padx=3)
            ToolTip(btn, tooltip)

        self.actualizar_lista_received()

    def actualizar_lista_received(self):
        self.received_listbox.delete(0, tk.END)
        received = self.modificador.get_received_list()
        for idx, _, valor in received:
            self.received_listbox.insert(tk.END, f"{idx}: {valor[:80]}...")

    def add_received_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add Received header")
        dialog.geometry("600x150")
        dialog.transient(self)
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="Full Received line:", font=("Segoe UI", 12)).pack(padx=10, pady=5)
        entry = ctk.CTkEntry(dialog, width=550)
        entry.pack(padx=10, pady=5)
        ctk.CTkButton(dialog, text="Add", command=lambda: self.add_received(entry.get(), dialog)).pack(pady=5)

    def add_received(self, valor, dialog):
        if valor:
            self.modificador.add_received_at_position(0, valor)
            self.actualizar_lista_received()
            self.ver_cabeceras()
        dialog.destroy()

    def remove_received(self):
        seleccion = self.received_listbox.curselection()
        if seleccion:
            idx = seleccion[0]
            if self.modificador.remove_received_at_index(idx):
                self.actualizar_lista_received()
                self.ver_cabeceras()

    def move_received_up(self):
        seleccion = self.received_listbox.curselection()
        if not seleccion:
            messagebox.showinfo("Info", "Select a Received header to move.")
            return
        idx = seleccion[0]
        if self.modificador.move_received_up(idx):
            self.actualizar_lista_received()
            self.ver_cabeceras()
        else:
            messagebox.showinfo("Info", "Cannot move up: already at the top.")

    def move_received_down(self):
        seleccion = self.received_listbox.curselection()
        if not seleccion:
            messagebox.showinfo("Info", "Select a Received header to move.")
            return
        idx = seleccion[0]
        if self.modificador.move_received_down(idx):
            self.actualizar_lista_received()
            self.ver_cabeceras()
        else:
            messagebox.showinfo("Info", "Cannot move down: already at the bottom.")

    # ------------------------------------------------------------
    # Pestaña: Campañas
    # ------------------------------------------------------------
    def crear_pestana_campanas(self):
        self.notebook.add("📊 Campaigns")
        frame = self.notebook.tab("📊 Campaigns")
        frame.grid_columnconfigure(0, weight=0)
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(frame, text="Save current headers as a template.", font=("Segoe UI", 12, "italic")).grid(row=0, column=0, columnspan=2, pady=5, sticky="w", padx=15)

        ctk.CTkLabel(frame, text="Template name:", font=("Segoe UI", 12)).grid(row=1, column=0, padx=15, pady=8, sticky="e")
        self.template_name = ctk.CTkEntry(frame, width=250, placeholder_text="my_template")
        self.template_name.grid(row=1, column=1, padx=15, pady=8, sticky="w")
        ToolTip(self.template_name, "Name for the template")

        ctk.CTkButton(frame, text="💾 Save template", command=self.guardar_plantilla,
                      width=150).grid(row=2, column=0, columnspan=2, pady=5)

        ctk.CTkLabel(frame, text="Saved templates:", font=("Segoe UI", 12)).grid(row=3, column=0, padx=15, pady=8, sticky="ne")
        self.template_listbox = tk.Listbox(frame, height=6, bg=COLORS["bg_light"], fg="white", selectbackground=COLORS["info"])
        self.template_listbox.grid(row=3, column=1, padx=15, pady=8, sticky="ew")

        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.grid(row=4, column=1, pady=5, sticky="w")
        ctk.CTkButton(btn_frame, text="📂 Load", command=self.cargar_plantilla,
                      width=100).pack(side="left", padx=2)
        ctk.CTkButton(btn_frame, text="🗑️ Delete", command=self.eliminar_plantilla,
                      width=100).pack(side="left", padx=2)

        ctk.CTkLabel(frame, text="X-Campaign-ID (optional):", font=("Segoe UI", 12)).grid(row=5, column=0, padx=15, pady=8, sticky="e")
        self.campaign_id = ctk.CTkEntry(frame, width=250, placeholder_text="campaign_123")
        self.campaign_id.grid(row=5, column=1, padx=15, pady=8, sticky="w")
        ToolTip(self.campaign_id, "Unique ID for tracking")

        ctk.CTkButton(frame, text="🔖 Insert ID into headers", command=self.insertar_campaign_id,
                      width=200).grid(row=6, column=0, columnspan=2, pady=10)

        self.actualizar_lista_plantillas()

    def actualizar_lista_plantillas(self):
        self.template_listbox.delete(0, tk.END)
        for tpl in self.modificador.campaign_manager.list_templates():
            self.template_listbox.insert(tk.END, tpl)

    def guardar_plantilla(self):
        nombre = self.template_name.get().strip()
        if not nombre:
            messagebox.showwarning("Empty name", "Please enter a template name.")
            return
        msg = self.modificador.guardar_como_plantilla(nombre)
        self.set_status(msg, COLORS["success"])
        self.actualizar_lista_plantillas()
        messagebox.showinfo("Saved", f"Template '{nombre}' saved in 'campaigns' folder.")

    def cargar_plantilla(self):
        seleccion = self.template_listbox.curselection()
        if seleccion:
            nombre = self.template_listbox.get(seleccion[0])
            msg = self.modificador.cargar_plantilla(nombre)
            self.set_status(msg, COLORS["success"])
            self.ver_cabeceras()
            messagebox.showinfo("Loaded", f"Template '{nombre}' loaded.")

    def eliminar_plantilla(self):
        seleccion = self.template_listbox.curselection()
        if seleccion:
            nombre = self.template_listbox.get(seleccion[0])
            if self.modificador.campaign_manager.delete_template(nombre):
                self.set_status(f"Template '{nombre}' deleted.", COLORS["success"])
                self.actualizar_lista_plantillas()
                messagebox.showinfo("Deleted", f"Template '{nombre}' deleted.")

    def insertar_campaign_id(self):
        cid = self.campaign_id.get().strip()
        if cid:
            self.modificador.anadir_cabecera('X-Campaign-ID', cid)
            self.ver_cabeceras()
            self.set_status("X-Campaign-ID inserted.", COLORS["success"])

    # ------------------------------------------------------------
    # Pestaña: Ejemplos
    # ------------------------------------------------------------
    def crear_pestana_ejemplos(self):
        self.notebook.add("📚 Examples")
        frame = self.notebook.tab("📚 Examples")
        frame.grid_columnconfigure(0, weight=1)

        examples_dir = os.path.join(os.path.dirname(__file__), 'examples')
        self.ejemplos = []
        if os.path.exists(examples_dir):
            self.ejemplos = [f for f in os.listdir(examples_dir) if f.lower().endswith('.eml')]

        ctk.CTkLabel(frame, text="Select an example email:", font=("Segoe UI", 12)).pack(pady=5)
        self.ejemplo_combo = ctk.CTkComboBox(frame, values=self.ejemplos, width=400)
        self.ejemplo_combo.pack(pady=5)
        if self.ejemplos:
            self.ejemplo_combo.set(self.ejemplos[0])

        ctk.CTkButton(frame, text="📂 Load Example", command=self.cargar_ejemplo,
                      width=150).pack(pady=10)

        if not self.ejemplos:
            ctk.CTkLabel(frame, text="No example files found in 'examples/' folder.", 
                         text_color=COLORS["warning"]).pack(pady=10)

    def cargar_ejemplo(self):
        nombre = self.ejemplo_combo.get()
        if not nombre:
            messagebox.showwarning("No selection", "Please select an example.")
            return
        examples_dir = os.path.join(os.path.dirname(__file__), 'examples')
        filepath = os.path.join(examples_dir, nombre)
        if os.path.exists(filepath):
            ok, msg = self.modificador.cargar_correo(filepath)
            if ok:
                self.current_file.set(f"File: {filepath}")
                self.set_status(msg, COLORS["success"])
                self.ver_cabeceras()
                num_headers = len(self.modificador.obtener_todas_cabeceras())
                messagebox.showinfo("Success", f"Example loaded.\n{num_headers} headers found.")
            else:
                self.set_status(msg, COLORS["error"])
                messagebox.showerror("Error", msg)
        else:
            messagebox.showerror("Error", f"File {filepath} not found.")

if __name__ == "__main__":
    app = EmailHeaderEditorApp()
    app.mainloop()