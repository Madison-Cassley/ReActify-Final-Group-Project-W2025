using ReActify.Models;
using ReActify.Views;

namespace ReActify
{
    public partial class MainPage : ContentPage
    {
        int count = 0;

        public MainPage()
        {
            InitializeComponent();

            try
            {                
                //Navigation.PushAsync(new FireAirView());
            }
            catch (Exception ex)
            {
                DisplayAlert("Error",ex.Message,"Ok");
            }
        }

        private void OnCounterClicked(object sender, EventArgs e)
        {
            count++;

            if (count == 1)
                CounterBtn.Text = $"Clicked {count} time";
            else
                CounterBtn.Text = $"Clicked {count} times";

            SemanticScreenReader.Announce(CounterBtn.Text);
        }
    }

}
