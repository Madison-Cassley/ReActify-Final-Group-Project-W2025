using Microsoft.ServiceBus.Messaging;
using Newtonsoft.Json.Linq;
using ReActify.Configs;
using ReActify.Services;
using Renci.SshNet;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ReActify.DataRepo
{
    /// <summary>
    /// Team ReActify
    /// Winter 2025, April 9
    /// Represents the Fire and Air Subsystem.
    /// </summary>
    public class Fire_AirSubSystem
    {
        /// <summary>
        /// Relay event for CO2 level readings.
        /// </summary>
        public event EventHandler RelayCO2Level;       
        private AzureIoTService iotServiceClient;
        private string CO2Level { get; set; }
        private enum FanState
        {
            ON,
            OFF
        }


        /// <summary>
        /// Initializes a new instance of the <see cref="Fire_AirSubSystem"/> class.
        /// </summary>
        /// <exception cref="Exception">Thrown when any error occurs</exception>
        public Fire_AirSubSystem(AzureIoTService azureIoTService)
        {
            try
            {
                iotServiceClient = azureIoTService;
                iotServiceClient.MessageReceived += MessageReceived;
            }
            catch (Exception ex)
            {
                throw new Exception($"Error connecting to ReTerminal 3: {ex.Message}. Please make sure that tail scale is active on your PC or ReTerminal.");
            }
        }

        /// <summary>
        /// Gets the CO2 level readings.
        /// </summary>
        /// <returns>String representing Azure D2C readings</returns>
        public string GetCO2Readings()
        {
            return CO2Level;
        }

        /// <summary>
        /// Turns the fan on using CD2 on Azure.
        /// </summary>
        public async Task FanOn()
        {
            try
            {
                string payLoad = "{\"FanState\":\"ON\"}";
                await iotServiceClient.InvokeC2DMethod(payLoad,"ToggleFan");
            }
            catch (Exception ex)
            {
                throw new Exception($"Error turning on the fan: {ex.Message}");
            }
        }
        
        /// <summary>
        /// Turns the fan off using CD2 on Azure.
        /// </summary>
        public async Task FanOff()
        {
            try
            {
                string payLoad = "{\"FanState\":\"OFF\"}";
                await iotServiceClient.InvokeC2DMethod(payLoad, "ToggleFan");
            }
            catch (Exception ex)
            {
                throw new Exception($"Error turning on the fan: {ex.Message}");
            }
        }

        /// <summary>
        /// Turns the LED on using CD2 on Azure.
        /// </summary>
        /// <returns></returns>
        /// <exception cref="Exception">Thrown when any errors occur</exception>
        public async Task LEDON()
        {
            try
            {
                string payLoad = "{\"LEDState\":\"ON\"}";
                await iotServiceClient.InvokeC2DMethod(payLoad, "ToggleLED");
            }
            catch (Exception ex)
            {
                throw new Exception($"Error turning on the led: {ex.Message}");
            }
        }

        /// <summary>
        /// Turns the LED red using CD2 on Azure.
        /// </summary>
        /// <returns></returns>
        /// <exception cref="Exception">Thrown when any errors occur</exception>
        public async Task LEDRED()
        {
            try
            {
                string payLoad = "{\"LEDState\":\"RED\"}";
                await iotServiceClient.InvokeC2DMethod(payLoad, "ToggleLED");
            }
            catch (Exception ex)
            {
                throw new Exception($"Error turning on the led: {ex.Message}");
            }
        }

        /// <summary>
        /// Turns the LED yellow using CD2 on Azure.
        /// </summary>
        /// <returns></returns>
        /// <exception cref="Exception">Thrown when any errors occur</exception>
        public async Task LEDYELLOW()
        {
            try
            {
                string payLoad = "{\"LEDState\":\"YELLOW\"}";
                await iotServiceClient.InvokeC2DMethod(payLoad, "ToggleLED");
            }
            catch (Exception ex)
            {
                throw new Exception($"Error turning on the led: {ex.Message}");
            }
        }

        /// <summary>
        /// Turns the LED green using CD2 on Azure.
        /// </summary>
        /// <returns></returns>
        /// <exception cref="Exception">Thrown when any errors occur</exception>
        public async Task LEDGREEN()
        {
            try
            {
                string payLoad = "{\"LEDState\":\"GREEN\"}";
                await iotServiceClient.InvokeC2DMethod(payLoad, "ToggleLED");
            }
            catch (Exception ex)
            {
                throw new Exception($"Error turning on the led: {ex.Message}");
            }
        }

        /// <summary>
        /// Turns the LED off using CD2 on Azure.
        /// </summary>
        /// <returns></returns>
        /// <exception cref="Exception">Thrown when any errors occur</exception>
        public async Task LEDOFF()
        {
            try
            {
                string payLoad = "{\"LEDState\":\"OFF\"}";
                await iotServiceClient.InvokeC2DMethod(payLoad, "ToggleLED");
            }
            catch (Exception ex)
            {
                throw new Exception($"Error turning on the led: {ex.Message}");
            }
        }

        private void MessageReceived(object? sender, EventArgs args)
        {
            //JObject json = iotServiceClient.GetD2CMessageInJSON();
            //string msg = json["Measurement.CO2LEVEL"].ToString();
            //CO2Level = msg;
            //RelayCO2Level?.Invoke(this, new EventArgs());

            var json = iotServiceClient.GetD2CMessageInJSON();
            var m = json["measurement"]?.ToString();
            var v = json["value"]?.ToObject<decimal>() ?? 0m;
            CO2Level = v.ToString("0.00");
            RelayCO2Level?.Invoke(this, EventArgs.Empty);
        }
    }
}
