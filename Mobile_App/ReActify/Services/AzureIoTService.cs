using Azure.Messaging.EventHubs;
using Azure.Messaging.EventHubs.Processor;
using Azure.Storage.Blobs;
using Microsoft.Azure.Devices;
using Newtonsoft.Json.Linq;
using ReActify.Configs;
using System;
using System.Diagnostics;
using System.Threading.Tasks;

namespace ReActify.Services
{
    public class AzureIoTService
    {
        private AzureConfigs azureConfigs;
        private JObject JSON { get; set; }

        /// <summary>
        /// Invoked when a message is received from the Azure IoT Hub.
        /// </summary>
        public event EventHandler MessageReceived;

        /// <summary>
        /// Default constructor for the Azure IoT Service.
        /// </summary>
        /// <param name="settings">Represents current settings from appsettings.json</param>
        public AzureIoTService(AzureConfigs settings)
        {
            azureConfigs = settings;

            // Initialize the Azure IoT service
            var storageClient = new BlobContainerClient(azureConfigs.StorageConnectionString, azureConfigs.BlobContainerName);
            var processor = new EventProcessorClient(storageClient, azureConfigs.ConsumerGroup, azureConfigs.EventHubConnectionString);

            processor.ProcessEventAsync += ProcessEventHandler;
            processor.ProcessErrorAsync += ProcessErrorHandler;

            try
            {
                processor.StartProcessingAsync();
                // The processor performs its work in the background;
                // to allow processing to take place.

                Task.Delay(Timeout.Infinite);
            }
            catch (Exception e)
            {
                Debug.WriteLine($"ERROR while processing event: {e.Message}");
            }
        }

        /// <summary>
        /// Invokes a Cloud-to-Device (C2D) method on the connected device.
        /// </summary>
        /// <param name="payLoad">Method payload to provide</param>
        /// <param name="methodName">Method name to invoke on the python code</param>
        /// <returns></returns>
        /// <exception cref="Exception">Thrown when any errors occur</exception>
        public async Task InvokeC2DMethod(string payLoad, string methodName)
        {
            try
            {
                // Send a message to the connected device
                var serviceClient = ServiceClient.CreateFromConnectionString(azureConfigs.ServiceConnectionString);

                // Ensure the following line is present in your file to resolve the CS0246 error.
                var methodInvocation = new CloudToDeviceMethod(methodName)
                {
                    ResponseTimeout = TimeSpan.FromSeconds(30)                                     
                };

                // Set the JSON payload
                methodInvocation.SetPayloadJson(payLoad);

                CloudToDeviceMethodResult response = await serviceClient.InvokeDeviceMethodAsync(azureConfigs.DeviceId, methodInvocation);
            }
            catch (Exception e)
            {
                throw new Exception(e.Message);
            }
        }

        /// <summary>
        /// Gets Device-to-Cloud (D2C) message in JSON format.
        /// </summary>
        /// <returns></returns>
        public JObject GetD2CMessageInJSON()
        {
            return JSON;
        }

        /// <summary>
        /// Processes the event received from the Event Hub.
        /// </summary>
        /// <param name="args"></param>
        /// <returns></returns>
        public async Task ProcessEventHandler(ProcessEventArgs args)
        {
            // Process the event received from the Event Hub
            Console.WriteLine($"Event received: {args.Data.EventBody}");           

            try
            { 
                await args.UpdateCheckpointAsync();
                // This is where the repo parsing the data should come into place. 
                // or a helper method which helps route the data to the appropriate repo.

                //RouteData(args.Data.EventBody);
                JSON = JObject.Parse(args.Data.EventBody.ToString());
                MessageReceived?.Invoke(this, EventArgs.Empty);

            }
            catch (Exception e)
            {
                Debug.WriteLine($"ERROR while processing event: {e.Message}");                
            }
        }

        /// <summary>
        /// Processes any errors that occur during event processing.
        /// </summary>
        /// <param name="args"></param>
        /// <returns></returns>
        public async Task ProcessErrorHandler(ProcessErrorEventArgs args)
        {
            Debug.WriteLine($"ERROR: {args}");
        }
    }
}