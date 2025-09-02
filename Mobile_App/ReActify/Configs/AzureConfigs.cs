using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ReActify.Configs
{
    public class AzureConfigs
    {
        //Events info
        public string EventHubName { get; set; }
        public string EventHubCompatibleName { get; set; }
        public string EventHubConnectionString { get; set; }

        //Service info
        public string ServiceConnectionString { get; set; }

        //Device info
        public string DeviceConnectionString { get; set; }
        public string DeviceId { get; set; }       
        public string DeviceKey { get; set; }

        
        //Blob info
        public string BlobContainerName { get; set; }
        public string ConsumerGroup { get; set; }
        public string SharedAccessKeyName { get; set; }
        public string SharedAccessKey { get; set; }

        //Storage info
        public string StorageConnectionString { get; set; }
    }
}
