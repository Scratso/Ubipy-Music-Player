﻿Imports System.IO

Public Class frmLauncher
    Dim logShown As Boolean = False
    Dim online As Boolean = True

    Private Sub AboutToolStripMenuItem_Click(sender As System.Object, e As System.EventArgs) Handles AboutToolStripMenuItem.Click
        frmAbout.Show()
    End Sub

    Function AddLog(str As String)
        txtLog.Text = txtLog.Text & Environment.NewLine & str
        Return str
    End Function

    Private Sub ContactToolStripMenuItem_Click(sender As System.Object, e As System.EventArgs) Handles ContactToolStripMenuItem.Click
        webMain.Navigate("http://damianheaton.com/#contact")
    End Sub

    Private Sub ResetBrowserToolStripMenuItem_Click(sender As System.Object, e As System.EventArgs) Handles ResetBrowserToolStripMenuItem.Click
        webMain.Navigate("http://scratso.xyz/archives/fl")
    End Sub

    Private Sub frmLauncher_Load(sender As System.Object, e As System.EventArgs) Handles MyBase.Load
        ' Remove when done testing
        My.Settings.Reset()
        AddLog("Launcher Version: " & ProductVersion)
        UpdateGame()
        If My.Settings.Version <> -1 Then
            lblLaunch.Visible = True
            pbDl.Visible = False
        End If
        'If (Not System.IO.Directory.Exists("data")) Then
        '    AddLog("Data folder not found. Creating...")
        '    System.IO.Directory.CreateDirectory("data")
        '    AddLog("Data folder created.")
        'End If
        'AddLog("Attempting creation of temp folder...")
        'If (Not System.IO.Directory.Exists("temp")) Then
        '    System.IO.Directory.CreateDirectory("temp")
        '    AddLog("Temp folder created.")
        'Else
        '    AddLog("Folder ""temp"" already exists. Using that instead.")
        'End If
        'AddLog("Attempting to obtain version data from Master... ")
        'Try
        '    My.Computer.Network.DownloadFile(
        '        "http://www.scratso.xyz/libgen/lib/fl/ver.txt",
        '        "temp\ver.txt")
        'Catch err As Exception
        '    AddLog("Error: " & err.ToString())
        '    AddLog("Enabling Launcher offline mode fallback...")
        '    online = False
        '    AddLog("Launcher fallen back to offline mode.")
        'End Try
        'If online = True Then
        '    Dim latestVer As String
        '    ' Open the file using a stream reader.
        '    Using sr As New StreamReader("temp\ver.txt")
        '        latestVer = sr.Read()
        '    End Using
        '    AddLog("Latest Version: " & latestVer)
        '    AddLog("Current Version: " & My.Settings.Version)
        '    If My.Settings.Version = latestVer Then
        '        AddLog("No update available. Sprint to run.")
        '        pbDl.Visible = False
        '        lblLaunch.Visible = True
        '    Else
        '        AddLog("Update is available.")
        '        ' Update here
        '    End If
        'Else
        '    AddLog("[OFFLINE MODE]")
        '    AddLog("Current Version: " & My.Settings.Version)
        '    If My.Settings.Version = -1 Then
        '        AddLog("Error: Unable to download game and no version is installed. Aborting...")
        '        MsgBox("No game version is installed and an internet connection could not be established. Aborting game launch.",
        '               MsgBoxStyle.Critical, "Error: Unable to Launch")
        '        AddLog("Aborted.")
        '    Else
        '        AddLog("Game edition was found. Permitting launch.")
        '        pbDl.Visible = False
        '        lblLaunch.Visible = True
        '    End If
        'End If
    End Sub

    Private Sub UpdateGame()
        Dim RemoteUri As String ' the web location of the files
        Dim Files() As String ' the list of files to be updated

        ' Set variables
        RemoteUri = "http://scratso.xyz/archives/ubipy/bin/"

        ' Check key folders exist
        If (Not System.IO.Directory.Exists("data")) Then
            AddLog("Data folder not found. Creating...")
            System.IO.Directory.CreateDirectory("data")
            AddLog("Data folder created.")
        End If
        AddLog("Attempting creation of temp folder...")
        If (Not System.IO.Directory.Exists("temp")) Then
            System.IO.Directory.CreateDirectory("temp")
            AddLog("Temp folder created.")
        Else
            AddLog("Folder ""temp"" already exists. Using that instead.")
        End If

        ' Get the latest version from Master
        AddLog("Attempting to obtain version data from Master... ")
        Try
            Try
                My.Computer.FileSystem.DeleteFile("temp\ver.txt")
            Catch ex As Exception

            End Try
            My.Computer.Network.DownloadFile(
                RemoteUri & "version.txt",
                "temp\ver.txt")
        Catch err As Exception
            AddLog("Error: " & err.ToString())
            AddLog("Enabling Launcher offline mode fallback...")
            online = False
            AddLog("Launcher fallen back to offline mode.")
        End Try
        If online Then
            Dim latestVer As Integer
            ' Open the file using a stream reader.
            Using sr As New StreamReader("temp\ver.txt")
                latestVer = sr.ReadToEnd()
            End Using
            AddLog("Current Version: " & My.Settings.Version)
            AddLog("Latest Version: " & latestVer)

            ' Is there an update?
            If latestVer > My.Settings.Version Then
                ' An update is available!
                AddLog("Update available!")
                AddLog("The program is behind by " & latestVer - My.Settings.Version & " update(s).")

                While My.Settings.Version <> latestVer
                    My.Settings.Version = My.Settings.Version + 1
                    AddLog("UPDATE " & My.Settings.Version)
                    AddLog("Fetching file list for update " & My.Settings.Version & "...")

                    Try
                        Try
                            My.Computer.FileSystem.DeleteFile("temp\files.txt")
                        Catch ex As Exception

                        End Try
                        My.Computer.Network.DownloadFile(
                        RemoteUri & My.Settings.Version & "/files.txt",
                        "temp\files.txt")
                    Catch err As Exception
                        AddLog("Error: " & err.ToString())
                    End Try

                    Dim fileList As String
                    ' Open the file using a stream reader.
                    Using sr As New StreamReader("temp\files.txt")
                        fileList = sr.ReadToEnd()
                    End Using
                    Files = fileList.Split(";")

                    For Each File As String In Files
                        If File.Contains("f:") Then
                            If (Not System.IO.Directory.Exists("data\" & File.Split(":")(1))) Then
                                AddLog("Creating folder """ & "data\" & File.Split(":")(1) & """...")
                                System.IO.Directory.CreateDirectory("data\" & File.Split(":")(1))
                                AddLog("Folder created.")
                            End If
                        Else
                            AddLog("Downloading file """ & File & """...")
                            Try
                                Try
                                    My.Computer.FileSystem.DeleteFile("data\" & File)
                                Catch ex As Exception

                                End Try
                                My.Computer.Network.DownloadFile(
                                RemoteUri & My.Settings.Version & "/" & File,
                                "data\" & File)
                            Catch err As Exception
                                AddLog("Error: " & err.ToString())
                            End Try
                        End If
                    Next

                    AddLog("Updated!")
                End While
            End If
        End If
    End Sub

    Private Sub LauncherToolStripMenuItem_Click(sender As System.Object, e As System.EventArgs) Handles LauncherToolStripMenuItem.Click
        If logShown = False Then
            logShown = True
            txtLog.Visible = True
            webMain.Visible = False
        Else
            logShown = False
            txtLog.Visible = False
            webMain.Visible = True
        End If
    End Sub

    Private Sub CreditsToolStripMenuItem_Click(sender As System.Object, e As System.EventArgs) Handles CreditsToolStripMenuItem.Click
        frmCredits.Show()
    End Sub

    Private Sub ForceValidationToolStripMenuItem_Click(sender As System.Object, e As System.EventArgs) Handles ForceValidationToolStripMenuItem.Click
        AddLog("=== User Forced Re-Validation ===")
        AddLog("Launcher Version: " & ProductVersion)
        UpdateGame()
        If My.Settings.Version <> -1 Then
            lblLaunch.Visible = True
            pbDl.Visible = False
        End If
    End Sub

    Private Sub RedownloadFLToolStripMenuItem_Click(sender As System.Object, e As System.EventArgs) Handles RedownloadFLToolStripMenuItem.Click

    End Sub

    Private Sub LicenseToolStripMenuItem_Click(sender As System.Object, e As System.EventArgs) Handles LicenseToolStripMenuItem.Click
        MsgBox("Ubipy is licensed under the GNU General Public License version 3." & Environment.NewLine & Environment.NewLine & "The source code is available at http://github.com/Scratso/Ubipy-Music-Player",
               MsgBoxStyle.Information, "Ubipy: License")
    End Sub
End Class