# tool_manager.py
import subprocess
import os
from session_manager import save_scan_results

def install_tools():
    tools = {
        'katana': 'https://github.com/projectdiscovery/katana.git',
        'subfinder': 'https://github.com/projectdiscovery/subfinder.git',
        'httpx': 'https://github.com/projectdiscovery/httpx.git',
        'nuclei': 'https://github.com/projectdiscovery/nuclei.git',
        'xsstrike': 'https://github.com/s0md3v/XSStrike.git',
        'sqlmap': 'https://github.com/sqlmapproject/sqlmap.git',
        'nikto': 'https://github.com/sullo/nikto.git'
    }

    for tool, url in tools.items():
        tool_path = f'tools/{tool}'
        if not os.path.exists(tool_path):
            print(f"Cloning {tool}...")
            subprocess.run(['git', 'clone', url, tool_path])

    # Install dependencies for tools that use Go and Python
    subprocess.run(['pip', 'install', '-r', 'requirements.txt'])
    subprocess.run(['go', 'install', 'github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest'])
    subprocess.run(['go', 'install', 'github.com/projectdiscovery/httpx/cmd/httpx@latest'])
    subprocess.run(['go', 'install', 'github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest'])

    print("Tools installed successfully!")

def run_tool(command, output_file):
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        with open(output_file, 'w') as f:
            f.write(result.stdout)
        return True
    except Exception as e:
        print(f"Error running tool: {e}")
        return False

# Function to install and update Nuclei templates
def install_nuclei_templates():
    """Downloads or updates the Nuclei templates."""
    if not os.path.exists("nuclei-templates"):
        print("Cloning Nuclei templates repository...")
        subprocess.run(['git', 'clone', 'https://github.com/projectdiscovery/nuclei-templates.git'])
    else:
        print("Updating Nuclei templates...")
        subprocess.run(['git', '-C', 'nuclei-templates', 'pull'])
    print("Nuclei templates are ready!")

def run_subfinder(domain, session_id):
    output_file = f'output/{domain}_subdomains.txt'
    if run_tool(['subfinder', '-d', domain, '-silent'], output_file):
        save_scan_results(session_id, "subfinder", output_file)
        return True
    return False

def run_httpx(domain, session_id):
    subdomains_file = f'output/{domain}_subdomains.txt'
    output_file = subdomains_file.replace('.txt', '_httpx.txt')
    if run_tool(['httpx', '-l', subdomains_file, '-silent'], output_file):
        save_scan_results(session_id, "httpx", output_file)
        return True
    return False

def run_katana(domain, session_id):
    output_file = f'output/{domain}_katana.txt'
    if run_tool(['katana', '-u', f'https://{domain}', '-silent'], output_file):
        save_scan_results(session_id, "katana", output_file)
        return True
    return False

def run_nuclei_custom(input_file, session_id, severity='medium', tags=None):
    """Runs Nuclei with custom severity and optionally filters by tags."""
    output_file = input_file.replace('.txt', f'_nuclei_{severity}.txt')
    
    command = ['nuclei', '-l', input_file, '-t', 'nuclei-templates/', '-severity', severity, '-silent']
    
    if tags:
        command += ['-tags', tags]
    
    if run_tool(command, output_file):
        save_scan_results(session_id, "nuclei_custom", output_file)
        return True
    return False

def run_multiple_nuclei_scans(input_file, session_id):
    """Run multiple Nuclei scans with varying severities and tags in one go."""
    severities = ['low', 'medium', 'high', 'critical']
    tags = ['cve', 'xss', 'sql']
    
    for severity in severities:
        run_nuclei_custom(input_file, session_id, severity=severity)
    
    for tag in tags:
        run_nuclei_custom(input_file, session_id, tags=tag)

def start_scan(domain, session_name, session_id):
    """Main function to start a scan for a domain and manage a session."""
    print(f"Starting scan for {domain}...")

    # Run Subfinder
    if run_subfinder(domain, session_id):
        print(f"Subfinder completed for {domain}")
        
    # Run HTTPX
    if run_httpx(domain, session_id):
        print(f"HTTPX completed for {domain}")
        
    # Run Katana for endpoint discovery
    run_katana(domain, session_id)
    print(f"Katana completed for {domain}")

def list_sessions():
    """For showing all sessions to the user."""
    from session_manager import load_sessions
    return load_sessions()
