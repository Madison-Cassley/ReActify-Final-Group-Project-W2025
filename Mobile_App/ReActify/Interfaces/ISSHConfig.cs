using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ReActify.Interfaces
{
    public interface ISSHConfig
    {
        string IPAddress { get; set; }
        string Username { get; set; }
        string Password { get; set; }
    }
}
