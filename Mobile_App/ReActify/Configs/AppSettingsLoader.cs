using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using ReActify.Configs;
using System.IO;
using Microsoft.Maui.Storage;

namespace ReActify.Configs
{
    class AppSettingsLoader
    {
        public static class AppSettingsLoaders
        {
            public static AzureConfigs Load()
            {
                // Reads appsettings.json from the packaged app folder
                var path = Path.Combine(FileSystem.AppPackageDirectory, "appsettings.json");
                var json = File.ReadAllText(path);
                var root = JsonSerializer.Deserialize<AppSettings>(json);
                return root.AzureConfigs;
            }
        }
    }
}
