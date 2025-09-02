using CommunityToolkit.Mvvm.ComponentModel;
using ReActify.DataRepo;
using System;
using System.Diagnostics;

namespace ReActify.Models
{
    public partial class Earthquake : ObservableObject
    {
        [ObservableProperty]
        private string movementStatus;

        [ObservableProperty]
        private string soundLevel;

        [ObservableProperty]
        private string emergencyMessage;

        [ObservableProperty]
        private bool showToggle;

        public Earthquake(EarthquakeSubsystem subsystem)
        {
            try
            {
                subsystem.MotionUpdated += OnMotionUpdated;
                subsystem.SoundUpdated += OnSoundUpdated;
            }
            catch (Exception ex)
            {
                Debug.WriteLine($"[EarthquakeModel] Connection error: {ex.Message}");
            }
        }

        private bool _movement;
        private string _sound = "QUIET";

        private void OnMotionUpdated(object? sender, EventArgs e)
        {
            if (sender is EarthquakeSubsystem sub)
            {
                _movement = sub.GetMovement();
                MovementStatus = _movement ? "Movement Detected" : "No Movement";
                UpdateEmergencyState();
            }
        }

        private void OnSoundUpdated(object? sender, EventArgs e)
        {
            if (sender is EarthquakeSubsystem sub)
            {
                var decibel = sub.GetSoundLevel();
                _sound = decibel switch
                {
                    >= 110 => "LOUD",
                    >= 100 => "MEDIUM",
                    _ => "QUIET"
                };
                SoundLevel = _sound;
                UpdateEmergencyState();
            }
        }

        private void UpdateEmergencyState()
        {
            if (_movement && _sound == "LOUD")
            {
                EmergencyMessage = "SEVERE EARTHQUAKE RISK";
                ShowToggle = true;
            }
            else
            {
                EmergencyMessage = "Normal";
                ShowToggle = false;
            }
        }
    }
}
