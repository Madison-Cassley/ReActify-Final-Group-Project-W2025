
﻿using ReActify.DataRepo;
using ReActify.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Input;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using System.ComponentModel;

namespace ReActify.ViewModels
{
    /// <summary>
    /// Team ReActify
    /// Winter 2025, April 9
    /// ViewModel for displaying Fire and Air Quality data.
    /// </summary>
    public partial class FireAirViewModel: ObservableObject, INotifyPropertyChanged
    {
        /// <summary>
        /// ReTerminal connection error event.
        /// </summary>
        public event EventHandler ReTerminalConnectionError;

        /// <summary>
        /// C2D error event, triggered when there is an issue toggling the fan on or off.
        /// </summary>
        public event EventHandler C2DError;

        /// <summary>
        /// The Fire and Air Quality model containing sensor readings.
        /// </summary>       
        [ObservableProperty]
        private Fire_AirQualityModel fireAirQualityModel;

        /// <summary>
        /// Command to return to the Home Page.
        /// </summary>  
        public ICommand BackCommand { get; }

        /// <summary>
        /// Initializes a new instance of the <see cref="FireAirViewModel"/> class.
        /// </summary>
        public FireAirViewModel(Fire_AirQualityModel fire_AirQuality)
        {
            try
            {                
                fireAirQualityModel = fire_AirQuality;
                fireAirQualityModel.ConnectionError += RelayError;

                BackCommand = new Command(async () => await Shell.Current.GoToAsync("//HomePage"));
            }
            catch (Exception e)
            {
                ReTerminalConnectionError?.Invoke(this, EventArgs.Empty);
            }
        }

        /// <summary>
        /// Toggles the fan on or off.
        /// </summary>
        [RelayCommand]
        public async void ToggleFan()
        {
            try
            {
                await FireAirQualityModel.ToggleFan();
            }
            catch (Exception e)
            {
                C2DError?.Invoke(this, EventArgs.Empty);
            }            
        }

        /// <summary>
        /// Invokes ReTerminal connection error event.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        public async void RelayError(object? sender, EventArgs e)
        {
            ReTerminalConnectionError?.Invoke(this, EventArgs.Empty);
        }
    }
}
