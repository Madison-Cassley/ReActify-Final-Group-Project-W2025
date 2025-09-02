using System;
using System.ComponentModel;
using System.Threading.Tasks;
using System.Windows.Input;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Microsoft.Maui.Controls;
using ReActify.Models;
using ReActify.Services;

namespace ReActify.ViewModels
{
    public partial class WaterFloodViewModel : ObservableObject
    {
        private readonly AzureIoTService _iotService;

        public Water_Floods WaterFloods { get; }

        public ICommand BackCommand { get; }
        public ICommand OpenServoCommand { get; }
        public ICommand CloseServoCommand { get; }
        public ICommand BuzzerCommand { get; }

        public WaterFloodViewModel(AzureIoTService iotService,Water_Floods waterFloods)
        {
            _iotService = iotService;
            WaterFloods = waterFloods;

            // navigation
            BackCommand = new Command(async () => await Shell.Current.GoToAsync("//HomePage"));

            // servo
            OpenServoCommand = new AsyncRelayCommand(() => SendServoAngleAsync(180));
            CloseServoCommand = new AsyncRelayCommand(() => SendServoAngleAsync(0));

            // buzzer
            BuzzerCommand = new AsyncRelayCommand(SendBuzzer3SecAsync);

            // update IsDanger whenever sensors change
            WaterFloods.PropertyChanged += OnSensorPropertyChanged;
        }

        public bool IsDanger => WaterFloods.WaterLevel >= 3.5m || WaterFloods.MoistureLevels >= 80m;

        private void OnSensorPropertyChanged(object sender, PropertyChangedEventArgs e)
        {
            if (e.PropertyName == nameof(WaterFloods.WaterLevel)
             || e.PropertyName == nameof(WaterFloods.MoistureLevels))
            {
                OnPropertyChanged(nameof(IsDanger));
            }
        }

        private Task SendServoAngleAsync(int angle)
        {
            var payload = $"{{ \"data\": {angle} }}";
            return _iotService.InvokeC2DMethod(payload, "SetServoAngle");
        }

        private async Task SendBuzzer3SecAsync()
        {
            //turn on
            var onPayload = "{ \"data\": 1 }";
            await _iotService.InvokeC2DMethod(onPayload, "ToggleBuzzer");

            //wait 3 seconds
            await Task.Delay(TimeSpan.FromSeconds(3));

            //turn off
            var offPayload = "{ \"data\": 0 }";
            await _iotService.InvokeC2DMethod(offPayload, "ToggleBuzzer");
        }
    }
}
