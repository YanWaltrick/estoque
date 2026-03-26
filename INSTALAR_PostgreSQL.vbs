' Script VBScript para elevar permissoes e instalar PostgreSQL
' Duplo-clique para executar com privilégios de administrador

Set objShell = CreateObject("Shell.Application")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Obter caminho do script PowerShell
scriptPath = objFSO.GetParentFolderName(WScript.ScriptFullName) & "\instalar_postgresql_admin.ps1"

' Verificar se o arquivo existe
If Not objFSO.FileExists(scriptPath) Then
    MsgBox "Erro: instalar_postgresql_admin.ps1 nao encontrado!", vbCritical
    WScript.Quit 1
End If

' Solicitar privilégios de administrador
objShell.ShellExecute "powershell.exe", "-NoProfile -ExecutionPolicy Bypass -File """ & scriptPath & """", , "runas", 1

WScript.Quit 0
