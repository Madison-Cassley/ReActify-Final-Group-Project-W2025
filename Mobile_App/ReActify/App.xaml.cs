using Microsoft.Extensions.DependencyInjection;
using ReActify.Views;

namespace ReActify
{
    public partial class App : Application
    {
        public static IServiceProvider Services { get; private set; }

        public App(IServiceProvider serviceProvider)
        {
            InitializeComponent();

            Services = serviceProvider;

            MainPage = new AppShell();
        }
    }
}
