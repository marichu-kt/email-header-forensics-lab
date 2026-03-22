# 📧 Email Header Forensics Lab

![Application Icon](./app_icon.ico)

**A desktop application for email header inspection, forensic review, and controlled authentication testing**  
*Load messages, generate realistic header sets for lab scenarios, review delivery chains, and validate common email-authentication signals.*

---

## Overview

**Email Header Forensics Lab** is a desktop application built for analysts, defenders, students, and researchers who need to **inspect, understand, and test email headers** in a controlled environment.

Instead of focusing on raw header text alone, the application provides a visual workflow for:

- opening and reviewing `.eml` files
- generating realistic header sets from common mail-client profiles
- editing and reorganizing `Received` headers
- running forensic checks against the current message
- saving reusable templates for repeated testing
- loading sample emails for learning and comparison
- sending test messages through SMTP in authorized environments

The project is especially useful for:
- forensic analysis
- blue-team training
- email authentication troubleshooting
- secure lab simulations
- analyst education and demonstrations

---

## What the Application Does

At its core, the application manages an email message object and lets you work with its headers through a GUI.

You can:

1. **Load an existing `.eml` file**
2. **Inspect all current headers in a text view**
3. **Generate a realistic header set using a selected profile**
4. **Review authentication-related fields such as SPF, DKIM, and DMARC**
5. **Edit the `Received` chain visually**
6. **Run forensic validation checks**
7. **Save your current header set as a reusable template**
8. **Open example messages to study real-looking formats**
9. **Send the message through SMTP for approved internal testing**

---

## Main Features

### 1. Open, View, and Save `.eml` Files

The application can load existing email files and display all current headers in a central text area.

This makes it easy to:
- inspect raw header values
- review message metadata in one place
- compare original and modified versions
- save the current message back to a new `.eml` file

This is helpful for both forensic review and repeatable testing workflows.

---

### 2. Profile-Based Header Generation

One of the main functions of the tool is the ability to generate realistic header sets inspired by common email clients and platforms.

The generator includes profiles such as:

- Gmail Web
- Gmail App Android
- Gmail App iOS
- Outlook Desktop
- Outlook Web
- Outlook Mobile
- iPhone with iCloud
- iPhone with Gmail
- Exchange On-Premise
- Zimbra

When a profile is applied, the application builds a realistic combination of headers such as:

- `From`
- `To`
- `Subject`
- `Date`
- `Message-ID`
- `Received`
- `Authentication-Results`
- `DKIM-Signature`
- `X-Mailer`
- additional platform-specific `X-*` headers

This makes the project useful for:
- analyst training
- understanding how different mail ecosystems structure headers
- creating lab scenarios for detection engineering
- comparing suspicious messages with expected client patterns

---

### 3. Authentication Result Simulation

The profile generator can also simulate different authentication outcomes for lab use.

Available modes include:
- `none`
- `spf_fail`
- `dkim_fail`
- `dmarc_fail`
- `mixed`

This allows you to study how authentication-related headers may look under different conditions and how your analysis workflow responds to them.

This feature is intended for:
- training analysts
- validating internal rules
- demonstrating the relationship between sender domains and authentication results
- reproducing controlled failure scenarios during research

---

### 4. Forensic Analysis Engine

The application includes a built-in forensic analyzer that reviews the current headers and produces structured results such as **PASS**, **WARN**, and **FAIL**.

The analyzer checks for issues including:

- missing required headers
- mismatches between `Message-ID` and `From` domains
- suspicious or private IP addresses in the `Received` chain
- inconsistent ordering in header dates
- authentication failures in SPF, DKIM, or DMARC results
- unusual `X-Mailer` values

This gives analysts a quick way to identify suspicious patterns without manually reviewing every field.

The forensic tab is useful when:
- triaging suspicious messages
- teaching students how to read headers
- testing how modified headers affect validation results
- documenting why a message looks legitimate or suspicious

---

### 5. Received Header Editor

The **Received** tab provides a visual way to work with the delivery chain.

Instead of editing everything by hand, you can:

- list all current `Received` headers
- add a new one
- delete a selected one
- move a header up
- move a header down

This is useful because the `Received` chain often tells the story of how a message moved through infrastructure.

In a lab or educational setting, this helps users:
- understand how mail routing appears in headers
- compare normal and abnormal delivery chains
- create controlled examples for training
- test forensic logic against different routing patterns

---

### 6. Template and Campaign Management

The application lets you save the current header set as a reusable template.

With this system, you can:
- save templates to the `campaigns` folder
- list previously saved templates
- load a template back into the application
- delete templates you no longer need

There is also an option to insert an `X-Campaign-ID` header, which can be useful for organizing internal exercises or identifying a particular scenario in a test dataset.

This part of the application is helpful when you want:
- repeatable lab cases
- reusable demo scenarios
- consistent sample sets for team training
- organized header libraries for internal use

---

### 7. Example Email Library

If the project includes an `examples/` directory with `.eml` files, the application can list and load them directly from the GUI.

This feature is useful for:
- onboarding new analysts
- reviewing sample header structures
- comparing multiple message types
- learning how different platforms format email metadata

Instead of building every scenario from scratch, users can start from prepared example messages and study them immediately.

---

### 8. SMTP Sending for Controlled Testing

The application includes an SMTP sending tab so the current message can be sent in an approved environment.

The SMTP workflow supports:
- SMTP server and port configuration
- username and password fields
- optional TLS
- optional sending delay
- optional relay list input

This can be useful for internal validation and controlled testing where a team wants to see how a message behaves after being delivered through a real SMTP path.

This feature should only be used in:
- owned infrastructure
- approved security labs
- internal testing environments
- authorized training exercises

---

### 9. Desktop Interface Built with CustomTkinter

The GUI is built with **CustomTkinter** and organized into separate tabs so each part of the workflow is easier to understand.

The main interface includes:
- a top banner
- a toolbar for loading, saving, refreshing, and validating
- a central header viewer
- tabs for profiles, SMTP, forensic analysis, received-chain editing, templates, and examples
- a status bar for feedback messages

This structure makes the application easier to use than manually editing raw email files in a text editor.

---

## Application Tabs Explained

### Profiles
Use this tab to generate a realistic header set based on a selected email-client profile.

You provide:
- sender name
- sender email
- recipient email
- subject
- authentication error mode

Then the application generates the corresponding headers and updates the current message.

### SMTP Send
Use this tab to send the current message through an SMTP server in an authorized environment.

You can configure:
- server
- port
- username
- password
- TLS
- delay
- optional relays

### Forensic
Use this tab to run a structured analysis of the current headers.

The results are shown in a readable text panel with visual status indicators.

### Received
Use this tab to inspect and rearrange `Received` headers.

This is one of the most useful tabs for understanding message routing and mail-hop order.

### Campaigns
Use this tab to save or load reusable templates and optionally insert an `X-Campaign-ID`.

### Examples
Use this tab to load `.eml` samples from the `examples/` directory.

---

## Project Structure

A typical repository layout looks like this:

```text
.
├── main_gui.py
├── modifier.py
├── realistic_generator.py
├── forensic_analyzer.py
├── campaign_manager.py
├── app_icon.ico
├── campaigns/
├── examples/
└── requirements.txt
```

### File Roles

#### `main_gui.py`
Contains the graphical interface and connects all features together.

#### `modifier.py`
Acts as the main controller for loading emails, editing headers, applying profiles, sending through SMTP, running forensic analysis, and working with templates.

#### `realistic_generator.py`
Generates realistic header sets, `Received` chains, `Message-ID` values, authentication results, and profile-specific metadata.

#### `forensic_analyzer.py`
Implements the forensic checks used by the validation system.

#### `campaign_manager.py`
Handles saving, loading, listing, and deleting templates.

---

## Installation

### Requirements
- Python 3.8 or newer
- `pip`

### Install from source

```bash
git clone https://github.com/yourusername/email-header-forensics-lab.git
cd email-header-forensics-lab
pip install -r requirements.txt
```

### Main dependencies

- `customtkinter` for the desktop interface
- `pillow` for image-related support

If you use Python from **MSYS2/MinGW** on Windows, install Pillow with:

```bash
pacman -S mingw-w64-x86_64-python-pillow
```

---

## Usage

### Start the application

```bash
python main_gui.py
```

### Typical workflow

1. Launch the application
2. Load a `.eml` file or create a new scenario from the **Profiles** tab
3. Review the generated or loaded headers in the main text area
4. Adjust the `Received` chain if needed
5. Run **Validate** or open the **Forensic** tab
6. Save the message as a new `.eml` file
7. Optionally store the result as a reusable template
8. Optionally send the message through SMTP in an approved test environment

---

## Build a Standalone Windows Executable

To package the application as a single Windows executable:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=app_icon.ico --add-data "campaigns;campaigns" --add-data "examples;examples" main_gui.py
```

The generated executable will be placed in the `dist/` directory.

### Notes
- `--add-data` includes the `campaigns` and `examples` folders inside the build
- `app_icon.ico` is used as the executable icon
- you can replace the icon file if you want a different visual identity

---

## Why This Project Is Useful

This project is useful because email headers are often difficult to read, compare, and explain manually.

By turning that process into a visual workflow, the application helps users:
- understand how mail clients format headers
- inspect delivery chains more easily
- spot suspicious metadata faster
- create repeatable test cases
- train others using controlled examples
- validate email-authentication scenarios in a lab

---

## Ethical and Legal Notice

This software is intended only for:

- education
- defensive security research
- forensic analysis
- authorized testing in controlled environments

It must not be used for:
- unauthorized impersonation
- phishing
- bypassing security controls
- deceptive or unlawful activity

Always obtain explicit written authorization before using this software in any environment you do not own or administer.

---

## Contributing

Contributions are welcome, especially in areas such as:

- interface improvements
- forensic checks
- profile realism for defensive research
- additional examples
- packaging and documentation
- code cleanup and maintainability

Please open an issue or submit a pull request.

---

## License

MIT License

---

## Acknowledgements

- Built with **CustomTkinter**
- Designed for analysts, researchers, and blue-team training
- Inspired by practical email-header analysis workflows
