import tkinter as tk
from tkinter import messagebox
from tool_manager import start_scan, list_sessions, run_multiple_nuclei_scans
from ai_interaction import ai_suggest_export_format
from report_exporter import export_report
from session_manager import create_new_session

root = tk.Tk()
root.title("Automated Bug Bounty Research Tool")
root.geometry("600x450")

# Input frame for domain and session name
frame = tk.Frame(root)
frame.pack(pady=20)

tk.Label(frame, text="Enter the domain to scan:").pack(side="left")
domain_entry = tk.Entry(frame)
domain_entry.pack(side="left")

tk.Label(frame, text="Enter a session name:").pack(side="left")
session_entry = tk.Entry(frame)
session_entry.pack(side="left")

def start_scan_action():
    domain = domain_entry.get()
    session_name = session_entry.get()
    
    if domain and session_name:
        session_id = create_new_session(session_name, domain)
        start_scan(domain, session_name, session_id)
        
        # Run multiple Nuclei scans (low, medium, high, critical + CVE, XSS, SQL)
        run_multiple_nuclei_scans(f'output/{domain}_subdomains_httpx.txt', session_id)
        
        scan_data = list_sessions()  # Get scan data
        ai_response = ai_suggest_export_format(domain, scan_data)
        
        # Export based on AI suggestion
        export_report(ai_response, domain, scan_data)
        messagebox.showinfo("Scan", f"Completed scanning {domain} under session '{session_name}'. Results exported as {ai_response}!")
    else:
        messagebox.showerror("Input Error", "Please provide both a domain and a session name.")

start_button = tk.Button(root, text="Start Scan", command=start_scan_action)
start_button.pack(pady=20)

def show_sessions():
    sessions = list_sessions()
    session_text = "\n".join([f"Session ID: {s[0]}, Name: {s[1]}, Domain: {s[2]}, Created: {s[3]}" for s in sessions])
    messagebox.showinfo("Sessions", session_text)

session_button = tk.Button(root, text="Show Sessions", command=show_sessions)
session_button.pack(pady=10)

root.mainloop()
