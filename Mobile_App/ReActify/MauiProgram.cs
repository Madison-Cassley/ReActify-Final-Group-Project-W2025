using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Microsoft.Maui.Storage;
using ReActify.Configs;
using ReActify.DataRepo;
using ReActify.Models;
using ReActify.Services;
using ReActify.ViewModels;
using ReActify.Views;
using System;
using System.IO;
using System.Reflection;

namespace ReActify
{
    public static class MauiProgram
    {
        public static MauiApp CreateMauiApp()
        {
            var builder = MauiApp.CreateBuilder()
                                 .UseMauiApp<App>()
                                 .ConfigureFonts(fonts =>
                                 {
                                     fonts.AddFont("OpenSans-Regular.ttf", "OpenSansRegular");
                                     fonts.AddFont("OpenSans-Semibold.ttf", "OpenSansSemibold");
                                 });

            //Load embedded appsettings.json
            var assembly = Assembly.GetExecutingAssembly();
            using var stream = assembly.GetManifestResourceStream("ReActify.appsettings.json")
                         ?? throw new InvalidOperationException(
                                "Could not find embedded resource 'ReActify.appsettings.json'");
            builder.Configuration.AddJsonStream(stream);

            //Pull down the AzureConfigs section
            var settings = builder.Configuration
                                  .GetSection(nameof(AzureConfigs))
                                  .Get<AzureConfigs>();
            builder.Services.AddSingleton(settings);

            //Register IoT service
            builder.Services.AddSingleton<AzureIoTService>();

            //local database
            string dbPath = Path.Combine(FileSystem.AppDataDirectory, "UserData.db");
            builder.Services.AddSingleton(new UserDatabase(dbPath));

            //Fire & Air registrations
            builder.Services.AddSingleton<Fire_AirSubSystem>();
            builder.Services.AddSingleton<Fire_AirQualityModel>();
            builder.Services.AddSingleton<FireAirViewModel>();
            builder.Services.AddSingleton<FireAirView>();

            //Earthquake subsystem registrations
            builder.Services.AddSingleton<EarthquakeSubsystem>();
            builder.Services.AddSingleton<Earthquake>();
            builder.Services.AddSingleton<EarthquakeViewModel>(sp =>
            {
                var model = sp.GetRequiredService<Earthquake>();
                var service = sp.GetRequiredService<AzureIoTService>();
                return new EarthquakeViewModel(model, service);
            });

            builder.Services.AddSingleton<EarthquakeView>();


            //Water & Floods registrations
            builder.Services.AddSingleton<Water_Floods_SubSystem>();
            builder.Services.AddSingleton<Water_Floods>(sp =>
                new Water_Floods(sp.GetRequiredService<Water_Floods_SubSystem>()));
            builder.Services.AddSingleton<WaterFloodViewModel>();
            builder.Services.AddSingleton<WaterFloodPage>();

#if DEBUG
            builder.Logging.AddDebug();
#endif

            return builder.Build();
        }
    }
}
