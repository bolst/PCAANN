using System.Net.NetworkInformation;

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

}
