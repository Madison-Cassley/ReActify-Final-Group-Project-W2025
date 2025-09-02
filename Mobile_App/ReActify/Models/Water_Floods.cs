using ReActify.Configs;
using ReActify.Models;
using ReActify.DataRepo;
using ReActify.Interfaces;
using System.Diagnostics;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using CommunityToolkit.Mvvm.ComponentModel;

namespace ReActify.Models
{
    /// <summary>
    /// Observable model for Water & Flood data.
    /// </summary>
    public partial class Water_Floods : ObservableObject
    {
        [ObservableProperty]
        private decimal waterLevel;

        [ObservableProperty]
        private decimal moistureLevels;

        public Water_Floods(Water_Floods_SubSystem subsystem)
        {
            try
            {
                subsystem.WaterLevelUpdated += OnWaterLevelUpdated;
                subsystem.MoistureLevelUpdated += OnMoistureLevelUpdated;
            }
            catch (Exception ex)
            {
                Debug.WriteLine($"[WaterModel] connection error: {ex.Message}");
            }
        }

        private void OnWaterLevelUpdated(object? sender, EventArgs e)
        {
            if (sender is Water_Floods_SubSystem sub)
                WaterLevel = Math.Round(sub.GetCurrentWaterLevel(), 1);
        }

        private void OnMoistureLevelUpdated(object? sender, EventArgs e)
        {
            if (sender is Water_Floods_SubSystem sub)
                MoistureLevels = Math.Round(sub.GetCurrentMoistureLevel(), 1);
        }
    }
}