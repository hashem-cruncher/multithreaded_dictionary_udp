# PowerShell script to convert Markdown to HTML and then to PDF

# First check if we have necessary tools
try {
    # Check for wkhtmltopdf
    $wkhtmltopdf = Get-Command wkhtmltopdf -ErrorAction Stop
    $have_wkhtmltopdf = $true
}
catch {
    $have_wkhtmltopdf = $false
    Write-Output "wkhtmltopdf not found. Will create HTML only."
}

# Convert Markdown to HTML
$markdown_file = "dictionary_system_report.md"
$html_file = "dictionary_system_report.html"
$pdf_file = "dictionary_system_report.pdf"

# Simple HTML header with styling
$html_header = @"
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Multithreaded Dictionary System</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 40px;
            color: #333;
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        h1 {
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }
        h2 {
            border-bottom: 1px solid #eee;
            padding-bottom: 5px;
            margin-top: 30px;
        }
        img {
            max-width: 100%;
            border: 1px solid #ddd;
            padding: 5px;
            margin: 10px 0;
        }
        code {
            background-color: #f5f5f5;
            padding: 2px 5px;
            border-radius: 3px;
        }
        pre {
            background-color: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
    </style>
</head>
<body>
"@

$html_footer = @"
</body>
</html>
"@

# Read markdown content
$markdown_content = Get-Content -Path $markdown_file -Raw

# Very basic markdown to HTML conversion (for simple elements)
# Note: This is a simple conversion and doesn't handle all markdown features
$html_content = $markdown_content -replace '# (.*)', '<h1>$1</h1>'
$html_content = $html_content -replace '## (.*)', '<h2>$1</h2>'
$html_content = $html_content -replace '### (.*)', '<h3>$1</h3>'
$html_content = $html_content -replace '\*\*(.*?)\*\*', '<strong>$1</strong>'
$html_content = $html_content -replace '\*(.*?)\*', '<em>$1</em>'
$html_content = $html_content -replace '!\[(.*?)\]\((.*?)\)', '<img src="$2" alt="$1">'
$html_content = $html_content -replace '\[(.*?)\]\((.*?)\)', '<a href="$2">$1</a>'

# Handle code blocks
$html_content = $html_content -replace '```(?:python|json)(.*?)```', '<pre><code>$1</code></pre>'
$html_content = $html_content -replace '```(.*?)```', '<pre><code>$1</code></pre>'

# Handle lists
$html_content = $html_content -replace '- (.*)', '<ul><li>$1</li></ul>'

# Save the HTML file
$html_header + $html_content + $html_footer | Out-File -FilePath $html_file -Encoding utf8

Write-Output "Created HTML file: $html_file"

# Convert HTML to PDF if wkhtmltopdf is available
if ($have_wkhtmltopdf) {
    Write-Output "Converting HTML to PDF using wkhtmltopdf..."
    & wkhtmltopdf $html_file $pdf_file
    
    if (Test-Path $pdf_file) {
        Write-Output "Created PDF file: $pdf_file"
    }
    else {
        Write-Output "Failed to create PDF file."
    }
}
else {
    Write-Output "To create a PDF, please install wkhtmltopdf and run this script again,"
    Write-Output "or open the HTML file in a browser and use the browser's print function to save as PDF."
} 