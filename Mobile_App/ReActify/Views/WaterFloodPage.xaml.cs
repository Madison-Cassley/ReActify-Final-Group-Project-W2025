using ReActify.ViewModels;
using Microsoft.Maui.Controls;

namespace ReActify.Views
{
    public partial class WaterFloodPage : ContentPage
    {
        public WaterFloodPage(WaterFloodViewModel vm)
        {
            InitializeComponent();
            BindingContext = vm;
        }
    }
}
