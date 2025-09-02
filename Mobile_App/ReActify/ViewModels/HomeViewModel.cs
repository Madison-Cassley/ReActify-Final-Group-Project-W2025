using System.ComponentModel;
using System.Windows.Input;
using Microsoft.Maui.Controls;
using ReActify.Views;

namespace ReActify.ViewModels
{
    /// <summary>
    /// Team ReActify
    /// Winter 2025, April 9
    /// ViewModel for navigation options on the Home Page.
    /// </summary>
    public class HomeViewModel : INotifyPropertyChanged
    {
        public ICommand GoToWaterFloodsCommand { get; }
        public ICommand GoToEarthquakeCommand { get; }
        public ICommand GoToFireCommand { get; }
        public ICommand GoToDashboardCommand { get; }
        public ICommand LogoutCommand { get; }

        /// <summary>
        /// Initializes a new instance of the <see cref="HomeViewModel"/> class.
        /// </summary>
        public HomeViewModel()
        {
            GoToWaterFloodsCommand = new Command(OnGoToWaterFloods);
            GoToEarthquakeCommand = new Command(OnGoToEarthquake);
            GoToFireCommand = new Command(OnGoToFire);
            GoToDashboardCommand = new Command(OnGoToDashboard);
            LogoutCommand = new Command(OnLogout);
        }

        private async void OnGoToWaterFloods()
        {
            //navigate to WaterFloodPage
            await Shell.Current.GoToAsync("//WaterFloodPage");
        }

        private async void OnGoToEarthquake()
        {
            await Shell.Current.GoToAsync("//EarthquakeView");
        }

        private async void OnGoToFire()
        {
            await Shell.Current.GoToAsync("//FireAirView");
            //await Shell.Current.GoToAsync($"{nameof(FireAirView)}");
        }

        private async void OnGoToDashboard()
        {
            await Shell.Current.GoToAsync("//DashboardPage");
        }

        private async void OnLogout() =>
            await Shell.Current.GoToAsync("//LoginPage");

        public event PropertyChangedEventHandler PropertyChanged;
        protected void OnPropertyChanged(string propertyName) =>
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
}
