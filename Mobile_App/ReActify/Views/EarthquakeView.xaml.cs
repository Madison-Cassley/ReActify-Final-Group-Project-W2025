using ReActify.ViewModels;

namespace ReActify.Views;

public partial class EarthquakeView : ContentPage
{
	public EarthquakeView(EarthquakeViewModel viewModel)
	{
		InitializeComponent();
        BindingContext = viewModel;
    }
}