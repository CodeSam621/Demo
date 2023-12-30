using System;
using Microsoft.Extensions.Configuration;
using Serilog.Formatting.Compact;

// using Microsoft.AspNetCore.Builder;
using Serilog;
// using Serilog.Sinks.SumoLogic;
using SumoLogic.Logging.Serilog.Extensions;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.

// IConfigurationRoot configuration = new ConfigurationBuilder()
//     .AddJsonFile("appsettings.json")
//     .Build();

var logger = new LoggerConfiguration()
    .ReadFrom.Configuration(builder.Configuration)
    .WriteTo.Console()
    .WriteTo.BufferedSumoLogic(
               new Uri("YOUR SUMOLOGIC COLLETOR URL"),
                sourceName: "ExampleNameSerilogBufferedSink",
                formatter: new CompactJsonFormatter())
    .Enrich.FromLogContext()
    .CreateLogger();

    builder.Logging.AddSerilog(logger);

builder.Services.AddControllers();
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();



var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}
app.UseHttpsRedirection();

app.UseAuthorization();

app.MapControllers();

app.Run();
