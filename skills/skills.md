# Skills for Earnings Dashboard

## HTML to PDF Conversion Skill

**Name:** html-to-pdf-converter

**Description:** Converts completed HTML dashboard pages from the dashboard folder into PDF format for reporting and distribution. This skill handles the conversion process, ensuring proper formatting, layout preservation, and professional output.

**Usage:**
- Locate the HTML dashboard file in the `dashboard/` folder.
- Use a PDF generation tool (e.g., Puppeteer, wkhtmltopdf, or browser-based conversion) to convert the HTML to PDF.
- Preserve interactive elements as static images if necessary.
- Ensure the PDF includes all charts, tables, and text with correct fonts (Georgia 22pt for headers, Arial 14pt for content).
- Add page breaks, headers, and footers as needed for professional presentation.
- Output the PDF to a `reports/` folder or specified location.

**Requirements:**
- Input: Path to HTML file in `dashboard/` folder (e.g., `dashboard/index.html`).
- Output: PDF file with the same name or custom name.
- Dependencies: PDF generation library or tool installed (e.g., via npm for Puppeteer).
- Handle errors for missing files or conversion failures.

**Example Prompt:**
"Convert the earnings dashboard HTML file to PDF, preserving all charts and formatting."