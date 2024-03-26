using System.Net.NetworkInformation;
using Blazorise.Extensions;
using PCAANN.Data;

namespace PCAANN.Api;

public static class DataExchange
{

    private static HttpClient client = new HttpClient();
    public static async Task<List<string>?> GetRawDataFiles()
    {
        var response = await client.GetAsync($"{UriBase.Uri()}/raw-data/files");
        List<string>? retval = await response.Content.ReadFromJsonAsync<List<string>>();
        return retval;
    }
    public static async Task<List<string>?> GetScoresFiles()
    {
        var response = await client.GetAsync($"{UriBase.Uri()}/scores/files");
        List<string>? retval = await response.Content.ReadFromJsonAsync<List<string>>();
        return retval;
    }
    public static async Task<List<string>?> GetResultsFiles()
    {
        var response = await client.GetAsync($"{UriBase.Uri()}/results/files");
        List<string>? retval = await response.Content.ReadFromJsonAsync<List<string>>();
        return retval;
    }

    public static async Task<bool> TestConnection()
    {
        try
        {
            var response = await client.GetAsync($"{UriBase.Uri()}");
        }
        catch (HttpRequestException)
        {
            return false;
        }
        return true;
    }

    public static async Task<List<string>> GetProfiles()
    {
        try
        {
            var response = await client.GetAsync($"{UriBase.Uri()}/profiles");
            List<string>? retval = await response.Content.ReadFromJsonAsync<List<string>>();
            return retval == null ? new List<string>() : retval;
        }
        catch (Exception)
        {
            return new List<string>();
        }
    }

    public static async Task<string?> GetProfileAsJsonStr(string name)
    {
        try
        {
            var response = await client.GetAsync($"{UriBase.Uri()}/profile/{name}");
            string retval = await response.Content.ReadAsStringAsync();
            if (retval.IsNullOrEmpty())
            {
                return null;
            }
            return retval;
        }
        catch (Exception)
        {
            return null;
        }
    }

    public static async Task<string> SaveProfile(OptionProfile Profile, string name)
    {
        try
        {
            var response = await client.PostAsJsonAsync($"{UriBase.Uri()}/saveprofile/{name}", Profile.ToJson());
            string content = await response.Content.ReadAsStringAsync();
            return content;
        }
        catch (Exception)
        {
            return "error in data transfer";
        }
    }

}
