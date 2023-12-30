using Microsoft.AspNetCore.Mvc;

namespace DotnetSerilog.Controllers;

[ApiController]
[Route("[controller]")]
public class WeatherForecastController : ControllerBase
{
    private static readonly string[] Summaries = new[]
    {
        "Freezing", "Bracing", "Chilly", "Cool", "Mild", "Warm", "Balmy", "Hot", "Sweltering", "Scorching"
    };

    private readonly ILogger<WeatherForecastController> _logger;

    public WeatherForecastController(ILogger<WeatherForecastController> logger)
    {
        _logger = logger;
    }

    [HttpGet(Name = "GetWeatherForecast")]
    public IEnumerable<WeatherForecast> Get()
    {
          _logger.LogInformation("Logging mycontroller index route");

        return Enumerable.Range(1, 5).Select(index => new WeatherForecast
        {
            Date = DateTime.Now.AddDays(index),
            TemperatureC = Random.Shared.Next(-20, 55),
            Summary = Summaries[Random.Shared.Next(Summaries.Length)]
        })
        .ToArray();
    }
    [HttpGet]
        [Route("parse-as-json")]
        public IActionResult ParseAsJson()
        {
            _logger.LogInformation("Calling route 'parse-as-json'");
            var randomBoolean = new Random().Next(1, 10)/2 == 1? true: false;
            var randomString = randomBoolean? "C#": "JavaScript";

            var message = new Message{
                Id= Guid.NewGuid(),
                Type = randomBoolean? "HTTP": "HTTPS",
                Data = new SupportedType []{
                    new SupportedType{ VerbType= "POST", Message = "Test message: " + randomString},
                    new SupportedType{ VerbType= "GET", Message = "Test message: " + randomString},
                    new SupportedType{ VerbType= "DELETE", Message = "Test message: " + randomString},
                }
            };

            _logger.LogInformation("{@message}",message);
            return Ok(message);
        }
}


    public class Message
    {
        public Guid Id { get; set; }
        public string Type { get; set; }
        public SupportedType[] Data { get; set; }
    }

    public class SupportedType
    {
        public string VerbType { get; set; }
        public string Message { get; set; }

    }
