## DotNet Web API integrate with Serilog and Sumologic

## Introduction

## Nuget packages in project file (.csproj)

    <PackageReference Include="Serilog" Version="3.1.1" />
    <PackageReference Include="Serilog.AspNetCore" Version="8.0.0" />
    <PackageReference Include="Serilog.Formatting.Compact" Version="2.0.0" />
    <PackageReference Include="Serilog.Settings.Configuration" Version="8.0.0" />
    <PackageReference Include="Serilog.Sinks.SumoLogic" Version="2.4.0" />
    <PackageReference Include="SumoLogic.Logging.Serilog" Version="1.0.1.7" />
    <PackageReference Include="Swashbuckle.AspNetCore" Version="6.2.3" />

## Install packages using `dotnet` cli
    dotnet add package Serilog --version=3.1.1
    dotnet add package Serilog.AspNetCore --version=8.0.0
    dotnet add package Serilog.Formatting.Compact --version=2.0.0
    dotnet add package Serilog.Settings.Configuration --version=8.0.0
    dotnet add package Serilog.Sinks.SumoLogic --version=2.4.0
    dotnet add package SumoLogic.Logging.Serilog --version=1.0.1.7
    dotnet add package Serilog --version=3.1.1

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
