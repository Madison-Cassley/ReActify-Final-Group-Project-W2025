using System;
using System.Diagnostics;
using Newtonsoft.Json.Linq;
using ReActify.Services;

namespace ReActify.DataRepo
{
    /// <summary>
    /// Handles incoming Water & Soil moisture telemetry from the Azure IoT Hub.
    /// </summary>
    public class Water_Floods_SubSystem
    {
        public event EventHandler WaterLevelUpdated;
        public event EventHandler MoistureLevelUpdated;

        private readonly AzureIoTService _iotService;
        private decimal _lastWaterLevel;
        private decimal _lastMoistureLevel;

        public Water_Floods_SubSystem(AzureIoTService iotService)
        {
            _iotService = iotService;
            _iotService.MessageReceived += OnMessageReceived;
        }

        private void OnMessageReceived(object? sender, EventArgs e)
        {
            try
            {
                var json = _iotService.GetD2CMessageInJSON();

                // 1) measurement is a simple string
                var measurement = json["measurement"]?.ToString() ?? "";

                // 2) value comes through as a JSON string, so parse it manually
                var valueToken = json["value"];
                decimal v = 0m;
                if (valueToken != null)
                {
                    var s = valueToken.ToString();
                    decimal.TryParse(s, out v);
                }

                if (measurement == "WATER_LEVEL")
                {
                    _lastWaterLevel = v;
                    WaterLevelUpdated?.Invoke(this, EventArgs.Empty);
                }
                else if (measurement == "SOIL_MOISTURE")
                {
                    _lastMoistureLevel = v;
                    MoistureLevelUpdated?.Invoke(this, EventArgs.Empty);
                }
            }
            catch (Exception ex)
            {
                Debug.WriteLine($"[WaterSubSystem] parse error: {ex.Message}");
            }
        }

        public decimal GetCurrentWaterLevel() => _lastWaterLevel;
        public decimal GetCurrentMoistureLevel() => _lastMoistureLevel;
    }
}