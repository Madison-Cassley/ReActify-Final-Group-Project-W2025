using CommunityToolkit.Mvvm.ComponentModel;
using Newtonsoft.Json.Linq;
using ReActify.Configs;
using ReActify.DataRepo;
using ReActify.Enums;
using ReActify.Interfaces;
using ReActify.Services;
using ReActify.Views;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ReActify.Models
{
    /// <summary>
    /// Team ReActify
    /// Winter 2025, April 9
    /// Represents the Fire and Air Quality information.
    /// </summary>
    public partial class Fire_AirQualityModel : ObservableObject
    {
        const int FAIR = 400, MODERATE = 1100, UNHEALTHY = 1600;

        /// <summary>
        /// Indicates the CO2 level in the air.
        /// </summary>
        [ObservableProperty]
        public decimal co2level;

        /// <summary>
        /// Gets or sets the smoke probability level.
        /// </summary>
        [ObservableProperty]
        public SmokeProbabilityEnum smokeProbability;

        /// <summary>
        /// Indicates the air quality based on CO2 levels.
        /// </summary>
        [ObservableProperty]
        private AirQualityEnum airQuality;

        private FanState fanState;

        /// <summary>
        /// Gets or sets a value indicating whether the fan is currently overridden.
        /// </summary>
        public bool FanIsOverriden { get; set; }

        private Fire_AirSubSystem Fire_AirSubSystem { get; set; }

        /// <summary>
        /// Occurs when a connection error is encountered.
        /// </summary>
        public event EventHandler ConnectionError;


        /// <summary>
        /// Initializes a new instance of the <see cref="Fire_AirQualityModel"/> class.
        /// </summary>
        public Fire_AirQualityModel(Fire_AirSubSystem fire_AirSubSystem)
        {
            try
            {
                Fire_AirSubSystem = fire_AirSubSystem;
                Fire_AirSubSystem.RelayCO2Level += GetCurrentCO2Level;
                AirQuality = AirQualityEnum.GOOD;
                SmokeProbability = SmokeProbabilityEnum.VeryLow;
                fanState = FanState.OFF;
            }
            catch (Exception e)
            {
                ConnectionError?.Invoke(this, EventArgs.Empty);
            }
        }

        /// <summary>
        /// Measures CO2 level using the Fire_AirSubSystem
        /// </summary>
        public async void GetCurrentCO2Level(object? sender, EventArgs args)
        {
            try
            {
                decimal value = Decimal.Parse(Fire_AirSubSystem.GetCO2Readings());

                if(value < FAIR)
                {
                    AirQuality = AirQualityEnum.GOOD;
                    SmokeProbability = SmokeProbabilityEnum.VeryLow;

                    if (!FanIsOverriden)
                    {
                        fanState = FanState.OFF;
                        await Fire_AirSubSystem.FanOff();
                    }

                    await Fire_AirSubSystem.LEDGREEN();
                }
                else if (value < MODERATE)
                {
                    AirQuality = AirQualityEnum.FAIR;
                    SmokeProbability = SmokeProbabilityEnum.Low;

                    if (!FanIsOverriden)
                    {
                        fanState = FanState.OFF;
                        await Fire_AirSubSystem.FanOff();
                    }
                    
                
                    await Fire_AirSubSystem.LEDGREEN();
                }
                else if (value < UNHEALTHY)
                {
                    AirQuality = AirQualityEnum.MODERATE;
                    SmokeProbability = SmokeProbabilityEnum.Medium;

                    if (!FanIsOverriden)
                    {
                        fanState = FanState.OFF;
                        await Fire_AirSubSystem.FanOff();                    
                    }
                    
                
                    await Fire_AirSubSystem.LEDYELLOW();
                }
                else
                {
                    AirQuality = AirQualityEnum.UNHEALTHY;
                    SmokeProbability = SmokeProbabilityEnum.High;

                    if (!FanIsOverriden)
                    {
                        fanState = FanState.ON;
                        await Fire_AirSubSystem.FanOn();
                    }
                    

                    await Fire_AirSubSystem.LEDRED();
                }

                Co2level = Math.Round(value, 1);     
            }
            catch (Exception e)
            {
                ConnectionError.Invoke(this, EventArgs.Empty);
            }
        }

        /// <summary>
        /// Activates the fan.
        /// </summary>
        public async Task ToggleFan()
        {
            try
            {
                if (FanIsOverriden)
                {
                    if (fanState == FanState.OFF)
                        return;
                                        
                    FanIsOverriden = false;
                    fanState = FanState.OFF;
                    await Fire_AirSubSystem.FanOff();
                }
                else
                {
                    if (fanState == FanState.ON)
                        return;
                    
                    FanIsOverriden = true;
                    fanState = FanState.ON;
                    await Fire_AirSubSystem.FanOn();
                }
            }
            catch(Exception e)
            {
                ConnectionError.Invoke(this, EventArgs.Empty);
            }
        }
    }
}
