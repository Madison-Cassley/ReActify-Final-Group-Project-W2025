using CommunityToolkit.Mvvm.ComponentModel;
using ReActify.Models;
using ReActify.Services;
using System.Windows.Input;
using Microsoft.Maui.Controls;
using System.Threading.Tasks;

namespace ReActify.ViewModels
{
    public partial class EarthquakeViewModel : ObservableObject
    {
        private readonly AzureIoTService _iotService;

        public Earthquake Earthquake { get; }

        public ICommand BackCommand { get; }
        public ICommand ToggleEmergencyCommand { get; }

        public EarthquakeViewModel(Earthquake model, AzureIoTService iotService)
        {
            Earthquake = model;
            _iotService = iotService;

            BackCommand = new Command(async () => await Shell.Current.GoToAsync("//HomePage"));

            ToggleEmergencyCommand = new Command(async () => await ToggleEmergencyLED());
        }

        private async Task ToggleEmergencyLED()
        {
            try
            {
                await Application.Current.MainPage.DisplayAlert(
                    "Emergency Protocol Activated",
                    "Warning: High sound and movement detected. Emergency lights toggled. Seek shelter or await assistance.",
                    "Understood");

                string payload = "{\"LEDState\":\"ON\"}";
                await _iotService.InvokeC2DMethod(payload, "ToggleLEDStick");
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"[EmergencyToggle] Error: {ex.Message}");
            }
        }
    }
}
