# Intune to IT Glue Bridge 🌉

**Turn your Intune Tenant Config into Documentation in Seconds.**

This tool automates the documentation process for Microsoft Intune. It uses the [IntuneCD](https://github.com/Micke-K/IntuneManagement) tool to pull a raw backup of your tenant's configurations (Compliance, Device Config, App Protection, etc.) and processes that JSON data into a single, highly formatted HTML report.

The output is styled specifically to look professional when pasted directly into **IT Glue**, **Hudu**, or **Confluence**.

## 🚀 Features

* **Zero-Touch Formatting:** Converts raw JSON "blobs" into clean, readable HTML tables.
* **MSP Friendly:** Tables are compacted to remove dead space and fit perfectly in KB articles.
* **Smart Parsing:** Automatically handles lists, arrays, and complex objects so you don't have to manually format GUIDs or settings.
* **Secure:** Runs locally on your machine; no data is sent to third parties.

## 📋 Prerequisites

1.  **Python 3.10+** installed.
2.  **IntuneCD** installed via pip:
    ```bash
    pip install IntuneCD
    ```
3.  **Administrator Access** to the Client's Entra ID (Azure AD) to create an App Registration.

---

## ⚙️ Phase 1: Azure App Registration (One-Time Setup)

To allow the tool to audit the tenant programmatically, you need to create an App Registration in the client's Entra ID.

1.  Navigate to **Entra ID** > **App registrations** > **New registration**.
2.  **Name:** `Intune Audit Tool` (or similar).
3.  **Account Type:** Accounts in this organizational directory only (Single tenant).
4.  **API Permissions:**
    Go to **API permissions** > **Add a permission** > **Microsoft Graph** > **Application permissions**.
    Add the following permissions to ensure full backup capability:

    **Intune Data Access:**
    * `DeviceManagementApps.ReadWrite.All`
    * `DeviceManagementConfiguration.ReadWrite.All`
    * `DeviceManagementScripts.ReadWrite.All`
    * `DeviceManagementServiceConfig.ReadWrite.All`
    * `DeviceManagementManagedDevices.ReadWrite.All`
    * `DeviceManagementRBAC.ReadWrite.All`
    * `Group.Read.All`
    * `Policy.Read.All`
    * `Policy.ReadWrite.ConditionalAccess`
    * `Application.Read.All`

    **Entra Data Access:**
    * `Domain.ReadWrite.All`
    * `Policy.ReadAll`
    * `Policy.ReadWrite.AuthenticationFlows`
    * `Policy.ReadWrite.AuthenticationMethod`
    * `Policy.ReadWrite.Authorization`
    * `Policy.ReadWrite.DeviceConfiguration`
    * `Policy.ReadWrite.ExternalIdentities`
    * `Policy.ReadWrite.SecurityDefaults`
    * `Group.ReadWrite.All`

    *Note: While "Read" permissions are sufficient for auditing, "ReadWrite" allows IntuneCD to potentially restore data if you choose to use that feature later.*

5.  **Grant Admin Consent:** Click the **"Grant admin consent"** button after adding permissions.
6.  **Create Secret:** Go to **Certificates & secrets**, create a new client secret, and copy the **Value** immediately.

---

## 💾 Phase 2: Backup the Data

Use `IntuneCD` to pull the raw configuration. Set your environment variables in your terminal before running the backup.

### Windows (PowerShell)
```powershell
# CAUTION: Use the domain name (e.g., contoso.onmicrosoft.com), NOT the Tenant ID GUID.
$env:TENANT_NAME = "client-domain.onmicrosoft.com"
$env:CLIENT_ID = "your-app-client-id"
$env:CLIENT_SECRET = "your-client-secret-value"

# Create a local folder for the backup
mkdir C:\Temp\IntuneBackup

# Run the backup in "App Mode" (Mode 1)
IntuneCD-startbackup -m 1 -p "C:\Temp\IntuneBackup"
```
## 📝 Phase 3: Generate the Report
Once the backup is complete and your JSON files are in C:\Temp\IntuneBackup, run the included Python script to generate your report.
1.	Open the intune_to_itglue.py file and ensure the input_folder path matches your backup location.
2.	Run the script:

```Bash
python intune_to_itglue.py
```
4.	The script will generate an HTML file (e.g., ITGlue_Report.html) and automatically open it in your default browser.

## 🏁 Phase 4: Import to Knowledge Base
1.	In the opened browser window, press Ctrl + A (Select All) and Ctrl + C (Copy).
2.	Open your IT Glue, Hudu, or Confluence document editor.
3.	Press Ctrl + V (Paste).
The content will paste as fully formatted, native HTML tables with proper headers, styling, and borders.

# ⚠️ Security Note
Always include a .gitignore file if you fork or clone this repo to prevent uploading client JSON data or credentials.
```Plaintext
# .gitignore
IntuneBackup/
IntuneDocs/
.env
auth.json
*.token
```
### 🐍 The Script File Name
For consistency with the README above, ensure the python script file in your repo is named:
`intune_to_itglue.py`

