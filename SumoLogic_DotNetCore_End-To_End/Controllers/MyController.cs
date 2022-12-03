using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;

namespace DotNetCoreSumoLogic.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class MyController : ControllerBase
    {
        private static readonly string[] Summaries = new[]
        {
            "Freezing", "Bracing", "Chilly", "Cool", "Mild", "Warm", "Balmy", "Hot", "Sweltering", "Scorching"
        };

        private readonly ILogger<MyController> _logger;

        public MyController(ILogger<MyController> logger)
        {
            _logger = logger;
        }

        [HttpGet]
        public IEnumerable<WeatherForecast> Get()
        {
            _logger.LogInformation("Logging mycontroller index route");
            var rng = new Random();
            return Enumerable.Range(1, 5).Select(index => new WeatherForecast
            {
                Date = DateTime.Now.AddDays(index),
                TemperatureC = rng.Next(-20, 55),
                Summary = Summaries[rng.Next(Summaries.Length)]
            })
            .ToArray();
        }

        [HttpGet]
        [Route("country")]
        public IActionResult Country()
        {
            // Simulate a random delay. So we can get different response time.
            Stopwatch watch = new Stopwatch();
            watch.Start();
            Thread.Sleep(new Random().Next(1000, 10000));
            watch.Stop();

            _logger.LogInformation($"country endpoint took: {watch.ElapsedMilliseconds} to process.");

            return Ok("Australia");
        }

        [HttpGet]
        [Route("city")]
        public IActionResult City()
        {
            var cities = new[] { "Melbourne", "Sydney", "Canberra", "Brisbane" };

            var randomNumber = new Random().Next(0, 4);
            var randomCity = cities[randomNumber];

            _logger.LogInformation($"City endpoint returns {randomCity}.");
            return Ok(randomCity);
        }

        [HttpGet]
        [Route("cityWithDelay")]
        public IActionResult CityWithDelay()
        {
            Stopwatch watch = new Stopwatch();
            watch.Start();
            Thread.Sleep(new Random().Next(1000, 10000));

            var cities = new[] { "Melbourne", "Sydney", "Canberra", "Brisbane" };
            var randomNumber = new Random().Next(0, 4);
            var randomCity = cities[randomNumber];

            watch.Stop();
            _logger.LogInformation($"Delay City endpoint returns {randomCity} took: {watch.ElapsedMilliseconds}");
            return Ok(randomCity);
        }

        [HttpGet]
        [Route("random-error")]
        public IActionResult RandomError()
        {
            var randomNumber = new Random().Next(1, 10);
            try
            {
                switch (randomNumber)
                {
                    case 1:
                        throw new Exception($"my custom error message: {Guid.NewGuid()}");
                    case 2:
                        var ob = new Person();
                        // want to create an exception
                        var street = ob.Address.Street;
                        break;
                    case 3:
                        var listPerson = new List<Person> { new Person() { }, new Person() { } };
                        // want to create an exception
                        var person = listPerson.SingleOrDefault();
                        break;
                    case 4:
                    case 5:
                    case 6:
                    case 7:
                    case 8:
                    case 9:
                        throw new Exception("NOT IMPLEMENTED ERROR");
                }
            }
            catch (Exception ex)
            {
                _logger.LogError($"Error occurred. Exception: {ex}");
            }

            return Ok();
        }
    }

    public class Person
    {
        public Address Address { get; set; }
    }

    public class Address
    {
        public string Street { get; set; }
    }
}
