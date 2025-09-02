using ReActify.DataRepo;
using System.ComponentModel;
using System.Windows.Input;
using Microsoft.Maui.Controls;

namespace ReActify.ViewModels
{
    /// <summary>
    /// Team ReActify
    /// Winter 2025, April 9
    /// ViewModel for creating a new account.
    /// </summary>
    public class CreateAccountViewModel : INotifyPropertyChanged
    {
        private string _newUsername;
        private string _newPassword;

        /// <summary>
        /// The new username entered by the user.
        /// </summary>
        public string NewUsername
        {
            get => _newUsername;
            set { _newUsername = value; OnPropertyChanged(nameof(NewUsername)); }
        }

        /// <summary>
        /// The new password entered by the user.
        /// </summary>
        public string NewPassword
        {
            get => _newPassword;
            set { _newPassword = value; OnPropertyChanged(nameof(NewPassword)); }
        }

        /// <summary>
        /// Command to navigate back to the login page.
        /// </summary>
        public ICommand BackToLoginCommand { get; }

        /// <summary>
        /// Command to create a new account.
        /// </summary>
        public ICommand CreateAccountCommand { get; }

        private readonly UserDatabase _database;

        /// <summary>
        /// Initializes a new instance of the <see cref="CreateAccountViewModel"/> class.
        /// </summary>
        public CreateAccountViewModel()
        {
            _database = App.Services.GetService<UserDatabase>();

            BackToLoginCommand = new Command(OnBackToLogin);
            CreateAccountCommand = new Command(async () => await OnCreateAccount());
        }

        /// <summary>
        /// Attempts to create a new account in the local database.
        /// </summary>
        private async Task OnCreateAccount()
        {
            if (string.IsNullOrWhiteSpace(NewUsername) || string.IsNullOrWhiteSpace(NewPassword))
            {
                await Shell.Current.DisplayAlert("Error", "Username and password cannot be empty.", "OK");
                return;
            }

            var existingUser = await _database.GetUserByUsernameAsync(NewUsername);
            if (existingUser != null)
            {
                await Shell.Current.DisplayAlert("Error", "Username already exists.", "OK");
                return;
            }

            await _database.SaveUserAsync(new UserData
            {
                Username = NewUsername,
                Password = NewPassword
            });

            await Shell.Current.DisplayAlert("Success", "Account created! You may now log in.", "OK");
            await Shell.Current.GoToAsync("//LoginPage");
        }

        /// <summary>
        /// Navigates the user back to the login page.
        /// </summary>
        private async void OnBackToLogin()
        {
            await Shell.Current.GoToAsync("//LoginPage");
        }

        public event PropertyChangedEventHandler PropertyChanged;
        protected virtual void OnPropertyChanged(string name) =>
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
    }
}