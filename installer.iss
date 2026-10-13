[Setup]
AppName=Study Master
AppVersion=1.0.0
AppPublisher=Niki Nasirzadeh
AppPublisherURL=https://github.com/https://github.com/niki1404wildfencer-tech/study-master
DefaultDirName={autopf}\Study Master
DefaultGroupName=Study Master
OutputDir=installer_output
OutputBaseFilename=StudyMaster-Setup-v1.0.0
SetupIconFile=assets\app_icon.ico
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
DisableProgramGroupPage=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"; Flags: checkedonce
Name: "quicklaunchicon"; Description: "Create a &Quick Launch shortcut"; GroupDescription: "Additional icons:"; Flags: unchecked

[Files]
Source: "dist\StudyMaster\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Study Master"; Filename: "{app}\StudyMaster.exe"
Name: "{group}\Uninstall Study Master"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Study Master"; Filename: "{app}\StudyMaster.exe"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\Study Master"; Filename: "{app}\StudyMaster.exe"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\StudyMaster.exe"; Description: "Launch Study Master"; Flags: nowait postinstall skipifsilent