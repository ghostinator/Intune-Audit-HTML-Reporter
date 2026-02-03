import os
import json
import html
import webbrowser
import re

# --- CONFIGURATION ---
# UPDATE THESE PATHS IF NEEDED
input_folder = r"C:\Temp\IntuneBackup"
output_file = r"C:\Temp\IntuneDocs\ITGlue_Report.html"

# --- STYLING (Optimized for IT Glue / Hudu) ---
css_style = """
<style>
    body { font-family: 'Segoe UI', Tahoma, sans-serif; color: #222; font-size: 13px; }
    
    /* SECTION HEADERS (Red/Bold) */
    h1 { 
        color: #B00020; 
        border-bottom: 3px solid #B00020; 
        padding-bottom: 8px; 
        margin-top: 50px; 
        font-size: 24px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* POLICY NAMES (Blue/Boxed) */
    h2 { 
        color: #003366; 
        margin-top: 30px; 
        margin-bottom: 10px; 
        font-size: 18px; 
        border-left: 6px solid #0078d4; 
        padding-left: 10px; 
        background-color: #f4f9ff;
        padding-top: 5px;
        padding-bottom: 5px;
    }
    
    /* TABLE STYLING */
    table { 
        border-collapse: collapse; 
        width: auto; 
        min-width: 50%; 
        margin-bottom: 20px; 
        border: 1px solid #bbb;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    
    th, td { 
        padding: 5px 10px; 
        border: 1px solid #ccc; 
        vertical-align: top; 
        text-align: left;
    }
    
    th { background-color: #eaeaea; font-weight: 700; white-space: nowrap; }
    
    /* Setting Name Column */
    td:first-child { 
        font-weight: 600; 
        color: #444; 
        white-space: nowrap; 
        background-color: #fafafa; 
    }
    
    /* Value Column - Wrap long text */
    td { word-wrap: break-word; max-width: 800px; }
    tr:nth-child(even) { background-color: #fcfcfc; }
</style>
"""

# Keys to exclude from the report (Metadata/Noise)
IGNORE_KEYS = {
    'id', 'lastModifiedDateTime', 'createdDateTime', 'version', 
    '@odata.context', '@odata.type', 'lastModifiedBy', 'generatedId',
    'groupId', 'policyId', 'roleScopeTagIds', 'supportsScopeTags'
}

def clean_key_name(key):
    """Converts camelCase to Title Case (e.g. passwordMinimumLength -> Password Minimum Length)"""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', key)
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1 \2', s1)
    return s2.title()

def flatten_json(y):
    """Flattens nested JSON objects for table display"""
    out = {}
    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + ' / ')
        elif type(x) is list:
            if len(x) > 0 and isinstance(x[0], str):
                out[name[:-3]] = ", ".join(x)
            else:
                out[name[:-3]] = json.dumps(x, indent=2)
        else:
            out[name[:-3]] = x
    flatten(y)
    return out

def process_policy_item(item, filename, html_content):
    if not isinstance(item, dict): return

    # Attempt to find the Policy Name
    policy_name = item.get('displayName', item.get('name', item.get('description', filename)))
    
    html_content.append(f"<h2>{html.escape(str(policy_name))}</h2>")
    html_content.append("<table><thead><tr><th>Setting</th><th>Value</th></tr></thead><tbody>")
    
    flat_data = flatten_json(item)
    
    for k in sorted(flat_data.keys()):
        if any(x in k for x in IGNORE_KEYS): continue
        if k.strip() == "": continue
        
        pretty_key = clean_key_name(k)
        safe_val = html.escape(str(flat_data[k]))
        
        html_content.append(f"<tr><td>{html.escape(pretty_key)}</td><td>{safe_val}</td></tr>")
        
    html_content.append("</tbody></table>")

def generate_report():
    # Create Output Directory if missing
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    html_content = [f"<html><head>{css_style}</head><body>"]
    html_content.append("<div style='font-size: 30px; font-weight: bold; margin-bottom: 20px;'>Intune Configuration Audit</div>")
    html_content.append(f"<p>Source Data: {input_folder}</p>")

    for root, dirs, files in os.walk(input_folder):
        if root == input_folder: continue
            
        category_name = os.path.basename(root)
        json_files = [f for f in files if f.endswith('.json')]
        
        if not json_files: continue
            
        html_content.append(f"<h1>{category_name}</h1>")

        for filename in json_files:
            filepath = os.path.join(root, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                except:
                    continue 

            if isinstance(data, list):
                for item in data:
                    process_policy_item(item, filename, html_content)
            elif isinstance(data, dict):
                if 'value' in data and isinstance(data['value'], list):
                    for item in data['value']:
                         process_policy_item(item, filename, html_content)
                else:
                    process_policy_item(data, filename, html_content)

    html_content.append("</body></html>")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(html_content))

    print(f"✅ Report Generated: {output_file}")
    webbrowser.open('file://' + output_file)

if __name__ == "__main__":
    generate_report()
