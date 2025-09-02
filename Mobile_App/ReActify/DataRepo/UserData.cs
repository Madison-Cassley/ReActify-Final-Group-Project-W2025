using SQLite;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ReActify.DataRepo
{
    /// <summary>
    /// Represents the User data model used for login and account creation.
    /// </summary>
    public class UserData
    {
        [PrimaryKey, AutoIncrement]
        public int Id { get; set; }

        [Unique]
        public string Username { get; set; }

        public string Password { get; set; }

        public string SecurityCode { get; set; }
    }
}