## DotNet Web API integrate with Serilog and Sumologic

## Step by Step guide
You can find the step by step guidance in this video: TBD

## Introduction
This project is a step by step guide to setup a `dotnet 6` peoject with `Serilog` logs and `Sumologic`.
After setting up the project, the logs should be available in Sumologic application and optionally you can see in logs file in local folder. The path to the log file in the folder will be config in the `appsettings.json` file.  Tested the below packages with dotnet 6 and should be work latest dotnet version like `dotnet 7, 8`, etc

## Install packages using `dotnet` cli
    dotnet add package Serilog --version=3.1.1
    dotnet add package Serilog.AspNetCore --version=8.0.0
    dotnet add package Serilog.Formatting.Compact --version=2.0.0
    dotnet add package Serilog.Settings.Configuration --version=8.0.0
    dotnet add package Serilog.Sinks.SumoLogic --version=2.4.0
    dotnet add package SumoLogic.Logging.Serilog --version=1.0.1.7
    dotnet add package Serilog --version=3.1.1

## Nuget packages in project file (.csproj) should be as below after install above packages

    <other dotnt packages>
    <PackageReference Include="Serilog" Version="3.1.1" />
    <PackageReference Include="Serilog.AspNetCore" Version="8.0.0" />
    <PackageReference Include="Serilog.Formatting.Compact" Version="2.0.0" />
    <PackageReference Include="Serilog.Settings.Configuration" Version="8.0.0" />
    <PackageReference Include="Serilog.Sinks.SumoLogic" Version="2.4.0" />
    <PackageReference Include="SumoLogic.Logging.Serilog" Version="1.0.1.7" />
    <PackageReference Include="Swashbuckle.AspNetCore" Version="6.2.3" />

## appsetting.json file

``` json
{
  "Logging": {
    "LogLevel": {
      "Default": "Debug",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*",
  "Serilog": {
    "Using": [ "Serilog.Sinks.File" ],
    "MinimumLevel": {
      "Default": "Information"
    },
    "WriteTo": [
      {
        "Name": "File",
        "Args": {
          "path": "./logs/webapi-.log",
          "rollingInterval": "Day",
          "outputTemplate": "{Timestamp:yyyy-MM-dd HH:mm:ss.fff zzz} {CorrelationId} {Level:u3} {Username} {Message:lj}{Exception}{NewLine}"
        }
      }
      
    ]
  }
}

```
