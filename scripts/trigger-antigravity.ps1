# Antigravity RPA Trigger Script (Simplified)
param([string]$Message = "Bridge上有新的任务")

try {
    $code = 'using System; using System.Runtime.InteropServices; public class Win32 { [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd); [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow); [DllImport("user32.dll")] public static extern bool IsIconic(IntPtr hWnd); public const int SW_RESTORE = 9; }'
    Add-Type -TypeDefinition $code -ErrorAction SilentlyContinue
} catch {}

Add-Type -AssemblyName System.Windows.Forms

Write-Host "Searching for Antigravity IDE (Antigravity.exe)..."
$window = Get-Process -Name "Antigravity" -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1

if ($window) {
    Write-Host "Found Antigravity window. Bringing to foreground..."
    $hwnd = $window.MainWindowHandle
    [Win32]::ShowWindow($hwnd, 9) | Out-Null
    [Win32]::SetForegroundWindow($hwnd) | Out-Null
    Start-Sleep -Milliseconds 1200
    
    # NEW: Safety sequence to clear menus and ensure editor is ready
    Write-Host "Sending ESC to clear menus..."
    [System.Windows.Forms.SendKeys]::SendWait("{ESC}")
    Start-Sleep -Milliseconds 300
    
    # NEW: Try multiple ways to focus the chat input
    Write-Host "Focusing chat panel..."
    [System.Windows.Forms.SendKeys]::SendWait("^l") # Standard chat focus
    Start-Sleep -Milliseconds 1000
    
    # NEW: Clear any existing text in the input box to prevent mess
    # We do this twice to be super sure we didn't miss the focus
    Write-Host "Cleaning input box..."
    [System.Windows.Forms.SendKeys]::SendWait("^a") # Select all
    Start-Sleep -Milliseconds 200
    [System.Windows.Forms.SendKeys]::SendWait("{BACKSPACE}") # Clear
    Start-Sleep -Milliseconds 300
    
    [System.Windows.Forms.Clipboard]::SetText($Message)
    Start-Sleep -Milliseconds 200
    
    Write-Host "Pasting Mission Briefing..."
    [System.Windows.Forms.SendKeys]::SendWait("^v") # Paste
    Start-Sleep -Milliseconds 600
    [System.Windows.Forms.SendKeys]::SendWait("{ENTER}") # Send
    Write-Host "Informed Antigravity successfully."
} else {
    Write-Host "Window not found."
}
