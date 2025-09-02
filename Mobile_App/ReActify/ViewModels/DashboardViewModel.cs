using System.ComponentModel;

namespace ReActify.ViewModels
{
    public class DashboardViewModel : INotifyPropertyChanged
    {
        public string Username => LoginViewModel.LoggedInUsername;
        public string FireDanger => "High";
        public string EarthquakeDanger => "Medium";
        public string FloodDanger => "Low";

        public int IncidentsToday => 5;
        public int InProgress => 2;
        public string AvgResponseTime => "12 min";
        public string LastUpdated => DateTime.Now.ToShortTimeString();

        public event PropertyChangedEventHandler PropertyChanged;
    }
}