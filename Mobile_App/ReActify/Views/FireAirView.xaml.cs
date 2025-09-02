using ReActify.Models;
using ReActify.ViewModels;

namespace ReActify.Views;

/// <summary>
/// Displays the Fire and Air Quality information.
/// </summary>
public partial class FireAirView : ContentPage
{
    /// <summary>
    /// Initializes a new instance of the <see cref="FireAirView"/> class.
    /// </summary>
    public FireAirView(FireAirViewModel vm)
	{
		try
		{
			InitializeComponent();
			BindingContext = vm;
            vm.ReTerminalConnectionError += DisplayReTerminalConnectionError;
            vm.C2DError += DisplayC2DError;
        }
		catch (Exception e)
		{
			DisplayAlert("ReTerminal Error", "There was an error connecting to this reTerminal. Please try again.", "Ok");
		}
	}

    /// <summary>
    /// Displays an alert when there is a ReTerminal connection error.
    /// </summary>
    /// <param name="sender"></param>
    /// <param name="e"></param>
	public async void DisplayReTerminalConnectionError(object? sender, EventArgs e)
    {
        try
        {
            await DisplayAlert("ReTerminal Error", "There was an error with receiving data from the reTerminal. Please try again.", "Ok");
        }
        catch (Exception ex)
        {            
            Console.WriteLine("An error occurred while displaying messsage");
        }
    }

    /// <summary>
    /// Displays an alert when there is a C2D error.
    /// </summary>
    /// <param name="sender"></param>
    /// <param name="e"></param>
	public async void DisplayC2DError(object? sender, EventArgs e)
    {
        try
        {
            await DisplayAlert("CD2 Error", "Unable to toggle fan on or off. Please try again.", "Ok");
        }
        catch (Exception ex)
        {
            Console.WriteLine("An error occurred while displaying messsage");
        }
    }
}