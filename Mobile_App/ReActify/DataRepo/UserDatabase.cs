using SQLite;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ReActify.DataRepo
{
    public class UserDatabase
    {
        private readonly SQLiteAsyncConnection _database;

        public UserDatabase(string dbPath)
        {
            _database = new SQLiteAsyncConnection(dbPath);
            _database.CreateTableAsync<UserData>().Wait();
        }

        public Task<int> SaveUserAsync(UserData user)
        {
            return _database.InsertAsync(user);
        }

        public Task<UserData> GetUserAsync(string username, string password)
        {
            return _database.Table<UserData>()
                            .Where(u => u.Username == username && u.Password == password)
                            .FirstOrDefaultAsync();
        }

        public Task<UserData> GetUserByUsernameAsync(string username)
        {
            return _database.Table<UserData>()
                            .Where(u => u.Username == username)
                            .FirstOrDefaultAsync();
        }
    }
}
