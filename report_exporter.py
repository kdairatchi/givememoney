# report_exporter.py
import json
import csv
from fpdf import FPDF
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree

def export_to_json(domain, data, output_dir='output'):
    filename = f"{output_dir}/{domain}_report.json"
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Exported results to {filename}")

def export_to_csv(domain, data, output_dir='output'):
    filename = f"{output_dir}/{domain}_report.csv"
    with open(filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(data[0].keys())  # Write header
        for row in data:
            writer.writerow(row.values())
    print(f"Exported results to {filename}")

def export_to_html(domain, data, output_dir='output'):
    filename = f"{output_dir}/{domain}_report.html"
    html_content = f"<html><head><title>Report for {domain}</title></head><body>"
    html_content += f"<h1>Scan Report for {domain}</h1><table border='1'>"
    
    # Table headers
    headers = data[0].keys()
    html_content += "<tr>" + "".join([f"<th>{header}</th>" for header in headers]) + "</tr>"
    
    # Table rows
    for row in data:
        html_content += "<tr>" + "".join([f"<td>{value}</td>" for value in row.values()]) + "</tr>"
    
    html_content += "</table></body></html>"
    
    with open(filename, 'w') as html_file:
        html_file.write(html_content)
    
    print(f"Exported results to {filename}")

def export_to_pdf(domain, data, output_dir='output'):
    """Exports data to a PDF file."""
    filename = f"{output_dir}/{domain}_report.pdf"
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, f"Bug Bounty Report for {domain}", 0, 1, 'C')
    
    # Table
    pdf.set_font('Arial', 'B', 12)
    headers = data[0].keys()
    for header in headers:
        pdf.cell(40, 10, header, 1)
    pdf.ln()
    
    pdf.set_font('Arial', '', 12)
    for row in data:
        for value in row.values():
            pdf.cell(40, 10, str(value), 1)
        pdf.ln()

    pdf.output(filename)
    print(f"Exported results to {filename}")

def export_to_xml(domain, data, output_dir='output'):
    """Exports data to an XML file."""
    filename = f"{output_dir}/{domain}_report.xml"
    root = Element('ScanReport')
    root.set('domain', domain)

    for row in data:
        item = SubElement(root, 'Item')
        for key, value in row.items():
            child = SubElement(item, key)
            child.text = str(value)

    tree = ElementTree(root)
    tree.write(filename)
    print(f"Exported results to {filename}")

def export_report(format_type, domain, data):
    """Exports report in the selected format."""
    if format_type.lower() == 'json':
        export_to_json(domain, data)
    elif format_type.lower() == 'csv':
        export_to_csv(domain, data)
    elif format_type.lower() == 'html':
        export_to_html(domain, data)
    elif format_type.lower() == 'pdf':
        export_to_pdf(domain, data)
    elif format_type.lower() == 'xml':
        export_to_xml(domain, data)
    else:
        print(f"Unknown format {format_type}. Export failed.")
