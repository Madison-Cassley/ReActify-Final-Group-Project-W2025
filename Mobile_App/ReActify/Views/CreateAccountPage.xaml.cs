using ReActify.ViewModels;

namespace ReActify.Views
{
    public partial class CreateAccountPage : ContentPage
    {
        public CreateAccountPage()
        {
            InitializeComponent();
            BindingContext = new CreateAccountViewModel();
        }
    }
}