using ReActify.DataRepo;
using System.ComponentModel;
using System.Windows.Input;
using Microsoft.Maui.Controls;

namespace ReActify.ViewModels
{
    /// <summary>
    /// Team ReActify
    /// Winter 2025, April 9
    /// ViewModel for login functionality and credential validation.
    /// </summary>
    public class LoginViewModel : INotifyPropertyChanged
    {
        private string _username;
        private string _password;
        private string _securityCode;

        public string Username
        {
            get => _username;
            set { _username = value; OnPropertyChanged(nameof(Username)); }
        }

        public string Password
        {
            get => _password;
            set { _password = value; OnPropertyChanged(nameof(Password)); }
        }

        public string SecurityCode
        {
            get => _securityCode;
            set { _securityCode = value; OnPropertyChanged(nameof(SecurityCode)); }
        }

        public ICommand LoginCommand { get; }
        public ICommand CreateAccountCommand { get; }

        private readonly UserDatabase _database;

        public static bool IsResponder { get; private set; }
        public static string LoggedInUsername { get; private set; }

        /// <summary>
        /// Initializes a new instance of the <see cref="LoginViewModel"/> class.
        /// </summary>
        public LoginViewModel()
        {
            _database = App.Services.GetService<UserDatabase>();

            LoginCommand = new Command(async () => await OnLogin());
            CreateAccountCommand = new Command(OnCreateAccount);
        }

        /// <summary>
        /// Handles the login logic and validation.
        /// </summary>
        private async Task OnLogin()
        {
            if (string.IsNullOrWhiteSpace(Username) || string.IsNullOrWhiteSpace(Password))
            {
                await Shell.Current.DisplayAlert("Error", "Username and password cannot be empty.", "OK");
                return;
            }

            var user = await _database.GetUserAsync(Username, Password);
            if (user == null)
            {
                await Shell.Current.DisplayAlert("Login Failed", "Invalid username or password.", "OK");
                return;
            }

            LoggedInUsername = Username;
            IsResponder = (SecurityCode == "admin123");
            await Shell.Current.GoToAsync("//HomePage");
        }

        /// <summary>
        /// Navigates to the account creation page.
        /// </summary>
        private async void OnCreateAccount()
        {
            await Shell.Current.GoToAsync("//CreateAccountPage");
        }

        public event PropertyChangedEventHandler PropertyChanged;
        protected virtual void OnPropertyChanged(string name) =>
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
    }
}