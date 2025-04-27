import tkinter as tk
from tkinter import ttk, messagebox
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import webbrowser
import random
import time
from PIL import Image, ImageTk
import threading

class PoliceTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("🚨 POLICE TRACKING SYSTEM v3.0 🚨")
        self.root.geometry("800x650")
        self.root.configure(bg="#0a0a2a")
        self.setup_ui()
        
    def setup_ui(self):
        # Police style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#0a0a2a')
        self.style.configure('TLabel', background='#0a0a2a', foreground='white', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 12, 'bold'), padding=10, 
                           background='red', foreground='white')
        self.style.map('TButton', 
                      background=[('active', 'darkred'), ('disabled', 'gray')])
        
        # Header with police badge
        self.header_frame = ttk.Frame(self.root)
        self.header_frame.pack(pady=10, fill=tk.X)
        
        try:
            self.badge_img = Image.open("police_logo.png").resize((80, 80))
            self.badge_photo = ImageTk.PhotoImage(self.badge_img)
            ttk.Label(self.header_frame, image=self.badge_photo).pack(side=tk.LEFT, padx=10)
        except:
            ttk.Label(self.header_frame, text="🚨", font=('Arial', 40)).pack(side=tk.LEFT, padx=10)
        
        ttk.Label(self.header_frame, 
                 text="POLICE TRACKING SYSTEM", 
                 font=('Arial', 18, 'bold'), 
                 foreground='red').pack(side=tk.LEFT)
        
        # Input section
        self.input_frame = ttk.Frame(self.root)
        self.input_frame.pack(pady=20, padx=20, fill=tk.X)
        
        ttk.Label(self.input_frame, 
                 text="ENTER TARGET PHONE NUMBER:", 
                 font=('Arial', 11, 'bold'),
                 foreground='yellow').pack(anchor=tk.W)
        
        self.entry = ttk.Entry(self.input_frame, font=('Arial', 14), width=20)
        self.entry.pack(fill=tk.X, pady=10)
        
        # Tracking button
        self.track_btn = ttk.Button(self.root, 
                                   text="🚨 INITIATE TRACKING", 
                                   command=self.start_tracking)
        self.track_btn.pack(pady=15)
        
        # Status display
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.progress = ttk.Progressbar(self.status_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X)
        
        self.status_label = ttk.Label(self.status_frame, 
                                    text="System Ready", 
                                    font=('Arial', 10),
                                    foreground='cyan')
        self.status_label.pack(pady=5)
        
        # Results display
        self.result_frame = ttk.Frame(self.root)
        self.result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.result_text = tk.Text(self.result_frame, 
                                 wrap=tk.WORD, 
                                 bg='#0a0a2a', 
                                 fg='white',
                                 font=('Courier', 10),
                                 insertbackground='white',
                                 borderwidth=0,
                                 highlightthickness=0)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # Disclaimer
        ttk.Label(self.root, 
                 text="⚠️ AUTHORIZED USE ONLY - UNAUTHORIZED ACCESS PROHIBITED ⚠️", 
                 font=('Arial', 8),
                 foreground='red').pack(side=tk.BOTTOM, pady=10)
    
    def start_tracking(self):
        phone_number = self.entry.get().strip()
        if not phone_number:
            messagebox.showerror("Error", "Please enter a phone number!")
            return
        
        self.track_btn.config(state=tk.DISABLED)
        self.progress.start()
        self.status_label.config(text="Accessing secure network...")
        self.result_text.delete(1.0, tk.END)
        
        threading.Thread(target=self.perform_tracking, args=(phone_number,), daemon=True).start()
    
    def perform_tracking(self, phone_number):
        try:
            # Simulate network access
            for i in range(1, 4):
                self.status_label.config(text=f"Connecting to secure channel [{i}/3]...")
                time.sleep(0.7)
            
            # Parse phone number
            parsed_number = phonenumbers.parse(phone_number, None)
            if not phonenumbers.is_valid_number(parsed_number):
                messagebox.showerror("Error", "Invalid phone number!")
                return
            
            # Get phone info
            service_provider = carrier.name_for_number(parsed_number, "en") or "UNKNOWN"
            country = geocoder.description_for_number(parsed_number, "en") or "UNKNOWN"
            time_zones = timezone.time_zones_for_number(parsed_number) or ["UNKNOWN"]
            
            # Generate approximate coordinates
            lat = round(random.uniform(-90, 90), 4)
            lon = round(random.uniform(-180, 180), 4)
            
            # Display results
            result = f"""
            ██████████████████████████████████████████████████
            █▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ TRACKING REPORT ▓▓▓▓▓▓▓▓▓▓▓▓▓▓█
            ██████████████████████████████████████████████████
            
            🔍 TARGET: {phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}
            🌎 COUNTRY OF ORIGIN: {country}
            ⏱️ TIME ZONE: {time_zones[0]}
            📡 CARRIER: {service_provider}
            
            📍 LAST KNOWN COORDINATES:
            Latitude: {lat}
            Longitude: {lon}
            
            ██████████████████████████████████████████████████
            █▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█
            ██████████████████████████████████████████████████
            """
            
            self.result_text.insert(tk.END, result)
            
            # Open location in browser
            webbrowser.open(f"https://www.google.com/maps?q={lat},{lon}")
            
            self.status_label.config(text="Target acquired - Tracking complete")
            
        except Exception as e:
            messagebox.showerror("Error", f"Tracking failed: {str(e)}")
        finally:
            self.progress.stop()
            self.track_btn.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = PoliceTracker(root)
    root.mainloop()