using Newtonsoft.Json.Linq;
using ReActify.Services;
using System;

namespace ReActify.DataRepo
{
    public class EarthquakeSubsystem
    {
        public event EventHandler VibrationUpdated;
        public event EventHandler MotionUpdated;
        public event EventHandler SoundUpdated;
        public event EventHandler LightUpdated;

        private readonly AzureIoTService _iotService;

        private decimal _vibration;
        private bool _movement;
        private decimal _soundLevel;
        private bool _emergencyLight;

        public EarthquakeSubsystem(AzureIoTService iotService)
        {
            _iotService = iotService;
            _iotService.MessageReceived += OnMessageReceived;
        }

        private void OnMessageReceived(object? sender, EventArgs e)
        {
            try
            {
                var json = _iotService.GetD2CMessageInJSON();
                string? measurement = json["measurement"]?.ToObject<string>();
                var value = json["value"]?.ToObject<decimal>() ?? 0;

                switch (measurement)
                {
                    case "VIBRATION":
                        _vibration = value;
                        VibrationUpdated?.Invoke(this, EventArgs.Empty);
                        break;
                    case "SOUND":
                        _soundLevel = value;
                        SoundUpdated?.Invoke(this, EventArgs.Empty);
                        break;
                    case "MOTION":
                        _movement = value == 1;
                        MotionUpdated?.Invoke(this, EventArgs.Empty);
                        break;
                    case "EMERGENCY":
                        _emergencyLight = value == 1;
                        LightUpdated?.Invoke(this, EventArgs.Empty);
                        break;
                }
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"[EarthquakeSubsystem] Error: {ex.Message}");
            }
        }

        public decimal GetVibration() => _vibration;
        public bool GetMovement() => _movement;
        public decimal GetSoundLevel() => _soundLevel;
        public bool IsEmergencyLightOn() => _emergencyLight;
    }
}
