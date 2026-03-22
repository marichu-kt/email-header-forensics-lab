import os
import datetime
import random
import re
from email import policy
from email.parser import BytesParser
from email.message import EmailMessage
from email.header import Header
from realistic_generator import RealisticHeaderGenerator
from campaign_manager import CampaignManager
from forensic_analyzer import ForensicAnalyzer
import smtplib
import time
import threading

class EmailModifier:
    def __init__(self, filepath=None):
        self.filepath = filepath
        self.msg = None
        self.generator = RealisticHeaderGenerator()
        self.campaign_manager = CampaignManager()
        self.history = []
        self.history_index = -1
        if filepath and os.path.exists(filepath):
            self.cargar_correo(filepath)
        else:
            self.msg = EmailMessage(policy=policy.default)

    # ------------------- Métodos básicos -------------------
    def cargar_correo(self, filepath):
        try:
            with open(filepath, 'rb') as fp:
                self.msg = BytesParser(policy=policy.default).parse(fp)
            self.filepath = filepath
            return True, f"Email loaded from: {filepath}"
        except FileNotFoundError:
            self.msg = EmailMessage(policy=policy.default)
            return False, f"Error: File not found {filepath}"
        except Exception as e:
            self.msg = EmailMessage(policy=policy.default)
            return False, f"Error loading email: {e}"

    def guardar_como(self, filepath):
        try:
            with open(filepath, 'wb') as fp:
                fp.write(self.msg.as_bytes())
            return True, f"Email saved to: {filepath}"
        except Exception as e:
            return False, f"Error saving: {e}"

    def obtener_todas_cabeceras(self):
        if not self.msg:
            return []
        return [(name, value) for name, value in self.msg._headers]

    def _reemplazar_cabecera_con_posicion(self, nombre, nuevo_valor):
        headers = self.msg._headers
        nuevo_nombre = nombre.lower()
        encontrado = False
        nuevo_headers = []
        for name, value in headers:
            if name.lower() == nuevo_nombre and not encontrado:
                nuevo_headers.append((nombre, nuevo_valor))
                encontrado = True
            elif name.lower() == nuevo_nombre:
                continue
            else:
                nuevo_headers.append((name, value))
        if not encontrado:
            nuevo_headers.append((nombre, nuevo_valor))
        self.msg._headers = nuevo_headers
        return f"Header '{nombre}' set to: {nuevo_valor}"

    def reemplazar_cabecera(self, nombre, valor):
        return self._reemplazar_cabecera_con_posicion(nombre, valor)

    def eliminar_cabecera(self, nombre):
        headers = self.msg._headers
        nuevo_headers = [(n, v) for n, v in headers if n.lower() != nombre.lower()]
        if len(nuevo_headers) == len(headers):
            return f"Header '{nombre}' does not exist."
        self.msg._headers = nuevo_headers
        return f"All headers '{nombre}' removed."

    def anadir_cabecera(self, nombre, valor):
        self.msg._headers.append((nombre, valor))
        return f"Header '{nombre}: {valor}' added."

    # ------------------- Perfiles y generación -------------------
    def generar_con_perfil(self, profile_key, from_name, from_email, to_email, subject, error_mode='none'):
        self.msg._headers = []
        profile = self.generator.profiles[profile_key]
        from_domain = from_email.split('@')[-1]
        envelope_domain = profile.get('envelope_domain') or from_domain
        dkim_domain = profile.get('dkim_domain')

        with_private = 'exchange_onprem' in profile_key or 'zimbra' in profile_key
        received_chain = self.generator.generate_received_chain(profile_key, length=random.randint(2,3), with_private=with_private)
        for rec in received_chain:
            self.msg._headers.append(('Received', rec))

        if random.random() < 0.9:
            auth = self.generator.generate_authentication_results(from_domain, envelope_domain, dkim_domain, error_mode)
            self.msg._headers.append(('Authentication-Results', auth))

        if dkim_domain and random.random() < 0.8:
            self.msg._headers.append(('DKIM-Signature', self.generator.generate_dkim_signature(dkim_domain)))

        extra = profile.get('extra_headers', [])
        random.shuffle(extra)
        for h in extra:
            self.msg._headers.append(h)

        if profile.get('x_mailer') and random.random() < 0.7:
            self.msg._headers.append(('X-Mailer', profile['x_mailer']))

        self.msg._headers.append(('MIME-Version', '1.0'))
        fecha = datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
        self.msg._headers.append(('Date', fecha))
        self.msg._headers.append(('From', f'"{from_name}" <{from_email}>'))
        self.msg._headers.append(('To', to_email))
        self.msg._headers.append(('Subject', subject))
        msg_id_domain = from_domain if dkim_domain is None else dkim_domain
        self.msg._headers.append(('Message-ID', self.generator.generate_message_id(msg_id_domain)))
        self.msg._headers.append(('Content-Type', 'text/plain; charset="utf-8"'))
        return f"Profile {profile['name']} applied with error mode={error_mode}"

    # ------------------- Envío SMTP -------------------
    def enviar_smtp(self, servidor, puerto, usuario, password, use_tls=True, relay_chain=None, delay=0):
        def _enviar():
            time.sleep(delay)
            try:
                if relay_chain:
                    # Usar el primer relay de la lista (simplificado)
                    servidor, puerto, usuario, password = relay_chain[0]
                with smtplib.SMTP(servidor, puerto) as smtp:
                    if use_tls:
                        smtp.starttls()
                    if usuario and password:
                        smtp.login(usuario, password)
                    smtp.send_message(self.msg)
                return True, "Email sent successfully."
            except Exception as e:
                return False, f"Error sending: {e}"

        thread = threading.Thread(target=_enviar)
        thread.start()
        return True, "Sending started in background."

    # ------------------- Análisis forense -------------------
    def analizar_forense(self):
        analyzer = ForensicAnalyzer(self.msg._headers)
        return analyzer.analyze()

    # ------------------- Editor Received -------------------
    def get_received_list(self):
        return [(i, name, value) for i, (name, value) in enumerate(self.msg._headers) if name.lower() == 'received']

    def add_received_at_position(self, pos, valor):
        self.msg._headers.insert(pos, ('Received', valor))

    def remove_received_at_index(self, idx):
        received_indices = [i for i, (name, _) in enumerate(self.msg._headers) if name.lower() == 'received']
        if 0 <= idx < len(received_indices):
            del self.msg._headers[received_indices[idx]]
            return True
        return False

    def move_received_up(self, idx):
        received_list = self.get_received_list()
        if idx <= 0 or idx >= len(received_list):
            return False
        global_idx_current = received_list[idx][0]
        global_idx_prev = received_list[idx-1][0]
        self.msg._headers[global_idx_current], self.msg._headers[global_idx_prev] = \
            self.msg._headers[global_idx_prev], self.msg._headers[global_idx_current]
        return True

    def move_received_down(self, idx):
        received_list = self.get_received_list()
        if idx < 0 or idx >= len(received_list)-1:
            return False
        global_idx_current = received_list[idx][0]
        global_idx_next = received_list[idx+1][0]
        self.msg._headers[global_idx_current], self.msg._headers[global_idx_next] = \
            self.msg._headers[global_idx_next], self.msg._headers[global_idx_current]
        return True

    # ------------------- Campañas y plantillas -------------------
    def guardar_como_plantilla(self, nombre):
        headers = [(n, v) for n, v in self.msg._headers]
        self.campaign_manager.save_template(nombre, headers)
        return f"Template '{nombre}' saved."

    def cargar_plantilla(self, nombre):
        headers = self.campaign_manager.load_template(nombre)
        if headers:
            self.msg._headers = headers
            return f"Template '{nombre}' loaded."
        return f"Template '{nombre}' not found."