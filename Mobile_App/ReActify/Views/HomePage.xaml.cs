using ReActify.ViewModels;

namespace ReActify.Views
{
    public partial class HomePage : ContentPage
    {
        public HomePage()
        {
            InitializeComponent();
            BindingContext = new HomeViewModel();
            ResponderButton.IsVisible = LoginViewModel.IsResponder;
        }
    }
}
