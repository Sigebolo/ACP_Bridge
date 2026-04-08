# Antigravity RPA Trigger Script (Service Compatible)
param([string]$Message = "Bridge上有新的任务")

try {
    $code = 'using System; using System.Runtime.InteropServices; public class Win32 { [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd); [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow); [DllImport("user32.dll")] public static extern bool IsIconic(IntPtr hWnd); public const int SW_RESTORE = 9; }'
    Add-Type -TypeDefinition $code -ErrorAction SilentlyContinue
} catch {}

Add-Type -AssemblyName System.Windows.Forms

Write-Host "Searching for Antigravity IDE (Antigravity.exe)..."

# Try multiple methods to find Antigravity
$window = Get-Process -Name "Antigravity" -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1

if ($window) {
    Write-Host "Found Antigravity window. Bringing to foreground..."
    $hwnd = $window.MainWindowHandle
    
    # Restore window if minimized
    if ([Win32]::IsIconic($hwnd)) {
        [Win32]::ShowWindow($hwnd, 9) | Out-Null
    }
    
    # Bring to front
    [Win32]::SetForegroundWindow($hwnd) | Out-Null
    Start-Sleep -Milliseconds 500
    
    try {
        # Send ESC to clear any active menus
        [System.Windows.Forms.SendKeys]::SendWait("{ESC}")
        Start-Sleep -Milliseconds 200
        
        # Focus chat input (Ctrl+L or similar)
        [System.Windows.Forms.SendKeys]::SendWait("^l")
        Start-Sleep -Milliseconds 500
        
        # Clear any existing text
        [System.Windows.Forms.SendKeys]::SendWait("^a")
        Start-Sleep -Milliseconds 200
        
        # Paste the message
        [System.Windows.Forms.Clipboard]::SetText($Message)
        [System.Windows.Forms.SendKeys]::SendWait("^v")
        Start-Sleep -Milliseconds 200
        
        # Send the message
        [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
        
        Write-Host "Informed Antigravity successfully."
    } catch {
        Write-Host "Failed to send keys to Antigravity: $($_.Exception.Message)"
        # Fallback: Write to log file
        $logPath = "d:\Gemini\agent-hand\bridge\logs\antigravity-messages.log"
        if (!(Test-Path (Split-Path $logPath))) {
            New-Item -ItemType Directory -Path (Split-Path $logPath) -Force | Out-Null
        }
        Add-Content -Path $logPath -Value "$(Get-Date): $Message"
        Write-Host "Message logged to: $logPath"
    }
} else {
    Write-Host "Antigravity window not found. Logging message instead."
    # Fallback: Write to log file
    $logPath = "d:\Gemini\agent-hand\bridge\logs\antigravity-messages.log"
    if (!(Test-Path (Split-Path $logPath))) {
        New-Item -ItemType Directory -Path (Split-Path $logPath) -Force | Out-Null
    }
    Add-Content -Path $logPath -Value "$(Get-Date): $Message"
    Write-Host "Message logged to: $logPath"
}
